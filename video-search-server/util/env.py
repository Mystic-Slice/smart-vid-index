# load api key from .env file
import dotenv
import logging

def load_env(config_file_path):
    if dotenv.load_dotenv(config_file_path):
        logging.info(f"[Env] Loaded environment variables from {config_file_path}")