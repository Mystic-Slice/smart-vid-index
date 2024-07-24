import logging 
import sys

def init_logger():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)