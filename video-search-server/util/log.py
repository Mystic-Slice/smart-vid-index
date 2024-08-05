import logging 
import sys

def init_logger(log_filename = "logs/server.log"):
    logging.basicConfig(
        level=logging.INFO,
        # stream=sys.stdout,
        filemode='a',
        filename=log_filename,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )