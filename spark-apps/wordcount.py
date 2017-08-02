#
# Adapted from wordcount.py from spark example
#
from __future__ import print_function

import sys, logging, os
from operator import add

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stderr))

if os.environ.has_key("PYTHON_PATH"):
    sys.path.extend(os.getenv("PYTHON_PATH").split(';'))
    logger.debug("Added to system path")
else:
    logger.debug("Did not add to system path")

from pyspark.sql import SparkSession


if __name__ == "__main__":
    read_input_path = "s3://hail-data-sse/texas-data/texas_data_dictionary.csv"
    save_output_path = "s3://hail-dickm-emr/data/output01.txt"
    msg = ""
    if len(sys.argv) < 2:
        print("Usage: wordcount <in path> <save path>", file=sys.stderr)
        msg = "We're using defaults of <in path>: '{}' and <save path>: '{}'.".format(read_input_path, save_output_path)
        logger.warning(msg)
    elif len(sys.argv) < 3:
        read_input_path = sys.argv[0]
        print("Usage: wordcount <in path> <save path>", file=sys.stderr)
        msg = "We're using defaults for <save path>: '{}'.".format(save_output_path)
        logger.warning(msg)        
    else:
        read_input_path = sys.argv[1]
        save_output_path = sys.argv[2]
        logger.debug("Input path: {}.\Output path: {}".format(read_input_path, save_output_path))

    spark = SparkSession\
        .builder\
        .appName("PySparkWordCountEMR")\
        .getOrCreate()

    msg = "Spark context created" + \
        ".\nStarting processing with input file" + \
        "'{}' and save location '{}'".format(
            read_input_path, save_output_path)

    logger.info(msg)
    print("From print: " + msg, file=sys.stderr)

    lines = spark.read.text(read_input_path).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    counts.saveAsTextFile(save_output_path)

    msg = "Processing completed. Shutting down ..."
    print("From print: " + msg, file=sys.stderr)
    logger.info(msg)

    spark.stop()
