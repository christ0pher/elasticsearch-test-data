#!/usr/bin/dumb-init /bin/bash
set -e

function usage () {
	echo <<"EOF"
Usage: $0 [ES_URL ES_COUNT ES_BATCH_SIZE]
 ES_URL : URL to the Elasticsearch host with port and protocol (http://ES:9200).
 ES_COUNT : Define the number of generated docs for the test (100000).
 ES_BATCH_SIZE : Define the size of the batches to upload (1000).
EOF
  exit 1
}

# Get and process arguments
while getopts ":ES_URL:ES_COUNT:ES_BATCH_SIZE:" opt; do
  case $opt in
    ES_URL) ES_URL+=("$OPTARG") ;;
    ES_COUNT) ES_COUNT+=("$OPTARG") ;;
    ES_BATCH_SIZE) ES_BATCH_SIZE+=("$OPTARG") ;;
    \?)
      echo "Invalid option: $OPTARG" >&2
      usage
      ;;
    :)
      echo "Option $OPTARG requires an argument." >&2
      usage
      ;;
  esac
done

# Bad arguments
if [ $? -ne 0 ];
then
  usage
fi

# Strip out all the arguments that have been processed
shift $((OPTIND-1))

ES_URL="${ES_URL:=http://ES:9200}"
ES_COUNT="${ES_COUNT:=1000000}"
ES_BATCH_SIZE="${ES_BATCH_SIZE:=1000}"

python3 /datadrivers/es_test_data.py --es-url=${ES_URL} --count=${ES_COUNT} --batch-size=${ES_BATCH_SIZE}

exit 0

# EOF
