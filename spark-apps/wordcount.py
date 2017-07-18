#
# Adapted from wordcount.py from spark example
#

from __future__ import print_function

import sys, logging
from operator import add

from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    read_input_path = ""
    save_output_path = ""

    if len(sys.argv) < 1:
        print("Usage: wordcount <file>", file=sys.stderr)
        exit(-1)
    elif len(sys.argv) < 2:
        pass
    else:
        pass

    spark = SparkSession\
        .builder\
        .appName("PySparkWordCountEMR")\
        .getOrCreate()

    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])
    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect().saveAsTextFile(save_output_path)

    spark.stop()
