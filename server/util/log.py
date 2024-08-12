import logging 
import sys

def init_logger(log_filename = "logs/server.log", stdout=False):
    if stdout:
        logging.basicConfig(
            level=logging.INFO,
            stream=sys.stdout,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            filemode='a',
            filename=log_filename,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )