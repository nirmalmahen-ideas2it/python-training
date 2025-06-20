import logging
import os
import requests
import functools
import time



def load_env_file():
    """Load environment variables from .env file"""
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

# Load environment variables
load_env_file()

# Vault configuration
VAULT_ADDR = os.environ.get('VAULT_ADDR', 'http://localhost:8100')
VAULT_TOKEN = os.environ.get('VAULT_TOKEN')
VAULT_DB_PATH = os.environ.get('VAULT_DB_PATH', 'secret/data/db-creds')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'postgres')


def fetch_db_credentials_from_vault():
    """Fetch DB username and password from Vault using token auth"""
    if not VAULT_TOKEN:
        raise RuntimeError("VAULT_TOKEN not set in environment.")
    url = f"{VAULT_ADDR}/v1/{VAULT_DB_PATH}"
    headers = {"X-Vault-Token": VAULT_TOKEN}
    try:
        resp = requests.get(url, headers=headers, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Vault KV v2: credentials are under data.data
        creds = data.get('data', {}).get('data', {})
        username = creds.get('username')
        password = creds.get('password')
        if not username or not password:
            raise RuntimeError("Username or password not found in Vault secret.")
        return username, password
    except Exception as e:
        raise RuntimeError(f"Failed to fetch DB credentials from Vault: {e}")

try:
    DB_USERNAME, DB_PASSWORD = fetch_db_credentials_from_vault()
    DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
except Exception as e:
    logging.error(str(e))
    DATABASE_URL = None

# Logging configuration
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')


def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            start=time.time()
            print(f"Entered the following method {func.__name__}")
            setup_logging()
            return func(*args, **kwargs)
        finally:
            end=time.time()
            print(f"The time taken for function: {func.__name__} is {end-start:.5f} seconds")
    return wrapper

def setup_logging():
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    ) 