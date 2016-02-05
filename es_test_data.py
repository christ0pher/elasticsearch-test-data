#!/usr/bin/python

import json
import time
import logging
import uuid

import numpy
import tornado.gen
import tornado.httpclient
import tornado.options
from tornado.httpclient import HTTPRequest, HTTPError

from parser.format_parser import get_data_for_format
import value_generator
from value_generator.default_value_generator import set_dict_data

async_http_client = tornado.httpclient.AsyncHTTPClient()
id_counter = 0
batch_upload_took = []
upload_data_count = 0


def delete_index(idx_name):
    try:
        url = "%s/%s?refresh=true" % (tornado.options.options.es_url, idx_name)
        request = tornado.httpclient.HTTPRequest(url, method="DELETE", request_timeout=240)
        response = tornado.httpclient.HTTPClient().fetch(request)
        logging.info('Deleting index  "%s" done   %s' % (idx_name, response.body))
    except tornado.httpclient.HTTPError:
        pass


def create_index(idx_name):
    schema = {
        "settings": {
            "number_of_shards": tornado.options.options.num_of_shards, "number_of_replicas": tornado.options.options.num_of_replicas
        },
        "refresh": True
    }

    body = json.dumps(schema)
    url = "%s/%s" % (tornado.options.options.es_url, idx_name)
    try:
        logging.info('Trying to create index %s' % (url))
        request = tornado.httpclient.HTTPRequest(url, method="PUT", body=body, request_timeout=240)
        response = tornado.httpclient.HTTPClient().fetch(request)
        logging.info('Creating index "%s" done   %s' % (idx_name, response.body))
    except tornado.httpclient.HTTPError:
        logging.info('Guess the index exists already')
        pass


@tornado.gen.coroutine
def upload_batch(upload_data_txt):

    request = tornado.httpclient.HTTPRequest(tornado.options.options.es_url + "/_bulk", method="POST", body=upload_data_txt, request_timeout=60 )
    response = yield async_http_client.fetch(request)

    result = json.loads(response.body.decode())
    res_txt = "OK" if not result['errors'] else "FAILED"
    took = int(result['took'])
    batch_upload_took.append(took)

    logging.info("Upload: %s - upload took: %5dms, total docs uploaded: %7d" % (res_txt, took, upload_data_count))


def generate_random_doc(format):
    global id_counter

    res = {}

    for f in format:
        f_key, f_val = get_data_for_format(f)
        if f_key:
            res[f_key] = f_val

    if not tornado.options.options.id_type:
        return res

    if tornado.options.options.id_type == 'int':
        res['_id'] = id_counter
        id_counter += 1
    elif tornado.options.options.id_type == 'uuid4':
        res['_id'] = str(uuid.uuid4())

    return res


def set_index_refresh(val):

    params = {"index": {"refresh_interval": val}}
    body = json.dumps(params)
    url = "%s/%s/_settings" % (tornado.options.options.es_url, tornado.options.options.index_name)
    try:
        request = HTTPRequest(url, method="PUT", body=body, request_timeout=240)
        async_http_client.fetch(request)
        logging.info('Set index refresh to %s' % val)
    except HTTPError:
        pass


@tornado.gen.coroutine
def generate_test_data():

    global upload_data_count

    if tornado.options.options.force_init_index:
        delete_index(tornado.options.options.index_name)

    if tornado.options.options.create_index:
        create_index(tornado.options.options.index_name)

    # todo: query what refresh is set to, then restore later
    if tornado.options.options.set_refresh:
        set_index_refresh("-1")

    if tornado.options.options.out_file:
        out_file = open(tornado.options.options.out_file, "w")
    else:
        out_file = None

    if tornado.options.options.dict_file:
        files = tornado.options.options.dict_file.split(",")
        dicts = {}
        for file in files:
            _dict_data = None
            with open(file, 'r') as f:
                _dict_data = f.readlines()
            dicts[file] = _dict_data
            logging.info("Loaded %d words from the %s" % (len(_dict_data), file))
        set_dict_data(dicts)

    format = tornado.options.options.format.split(',')
    if not format:
        logging.error('invalid format')
        exit(1)

    ts_start = int(time.time())
    upload_data_txt = ""
    total_uploaded = 0

    logging.info("Generating %d docs, upload batch size is %d" % (tornado.options.options.count, tornado.options.options.batch_size))
    for num in range(0, tornado.options.options.count):

        item = generate_random_doc(format)

        if out_file:
            out_file.write("%s\n" % json.dumps(item))

        cmd = {'index': {'_index': tornado.options.options.index_name, '_type': tornado.options.options.index_type}}
        if '_id' in item:
            cmd['index']['_id'] = item['_id']

        upload_data_txt += json.dumps(cmd) + "\n"
        upload_data_txt += json.dumps(item) + "\n"
        upload_data_count += 1

        if upload_data_count % tornado.options.options.batch_size == 0:
            yield upload_batch(upload_data_txt)
            upload_data_txt = ""

    # upload remaining items in `upload_data_txt`
    if upload_data_txt:
        yield upload_batch(upload_data_txt)

    if tornado.options.options.set_refresh:
        set_index_refresh("1s")

    if out_file:
        out_file.close()

    took_secs = int(time.time() - ts_start)
    logging.info("Done - total docs uploaded: %d, took %d seconds" % (tornado.options.options.count, took_secs))
    logging.info("Bulk upload average:         %4d ms" % int(numpy.mean(batch_upload_took)))
    logging.info("Bulk upload median:          %4d ms" % int(numpy.percentile(batch_upload_took, 50)))
    logging.info("Bulk upload 95th percentile: %4d ms" % int(numpy.percentile(batch_upload_took, 95)))


if __name__ == '__main__':
    tornado.options.define("es_url", type=str, default='http://localhost:9200/', help="URL of your Elasticsearch node")
    tornado.options.define("index_name", type=str, default='test_data', help="Name of the index to store your messages")
    tornado.options.define("index_type", type=str, default='test_type', help="Type")
    tornado.options.define("batch_size", type=int, default=1000, help="Elasticsearch bulk index batch size")
    tornado.options.define("num_of_shards", type=int, default=2, help="Number of shards for ES index")
    tornado.options.define("count", type=int, default=10000, help="Number of docs to generate")
    tornado.options.define("format", type=str, default='name:str,age:int,last_updated:ts,name:no:', help="message format")
    tornado.options.define("num_of_replicas", type=int, default=0, help="Number of replicas for ES index")
    tornado.options.define("force_init_index", type=bool, default=False, help="Force deleting and re-initializing the Elasticsearch index")
    tornado.options.define("set_refresh", type=bool, default=False, help="Set refresh rate to -1 before starting the upload")
    tornado.options.define("out_file", type=str, default=False, help="If set, write test data to out_file as well.")
    tornado.options.define("id_type", type=str, default=None, help="Type of 'id' to use for the docs, valid settings are int and uuid4, None is default")
    tornado.options.define("dict_file", type=str, default=None, help="Name of dictionary file to use")
    tornado.options.define("create_index", type=bool, default=True, help="If an index should be created")

    tornado.options.parse_command_line()

    tornado.ioloop.IOLoop.instance().run_sync(generate_test_data)
