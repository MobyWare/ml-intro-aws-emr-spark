import sys, os, logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

## Allow running locally if valid
if os.environ.has_key("PYTHON_PATH"):
    sys.path.extend(os.getenv("PYTHON_PATH").split(';'))
    logger.info("Added to system path")
else:
    logger.info("Did not add to system path")

try:
    import pyspark    
    logger.info("Successfully imported Spark modules.")

except ImportError as e:
    logger.info("Could not import Spark modules.\nDetails:\n".format(str(e)))
    sys.exit(1)