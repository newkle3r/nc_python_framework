import subprocess
import sys
import json
import os
from typing import Any
from functions import parse_redis_conf, gco, get_nextcloud_config_value, get_three_letter_code, parse_nextcloud_config, generate_strong_password, store_in_redis, save_env_variables, ensure_docker_compose_installed
import subprocess

class Ledger:
    nextcloud_config_path: str
    redis_config_path: str
    REDISHOST: str
    REDISPORT: str
    REDIS_PASSWORD: str
    REDIS_SOCK: str
    REDIS_SOCK_PERM: str
    REDIS_SOCK_URL: str
    POSTGRESHOST: str
    POSTGRESPORT: str
    POSTGRESUSER: str
    POSTGRESDB: str
    POSTGRESPASSWORD: str
    NC_POSTGRESPORT: str
    NC_POSTGRESHOST: str
    NC_POSTGRESUSER: str
    POSTGRESQLV: str
    URL: str
    PORT: int
    DEFAULT_PHONE_REGION: str
    DEFAULTLANGUAGES: list
    OCRLANGUAGESARRAY: list
    PAPERLESS_TIME_ZONE: str
    PAPERLESS_ALLOWED_HOSTS: str
    PAPERLESS_CORS_ALLOWED_HOSTS: str
    USERMAPUID: int
    USERMAPGID: int
    DATABASEBACKEND: str
    TIKAENABLED: str
    OCRLANGUAGE: str
    PAPERLESS_STATICDIR: str
    PAPERLESS_MEDIA_ROOT: str
    PAPERLESS_CONSUME_DIR: str
    PAPERLESS_DATA_DIR: str
    PAPERLESS_TRASH_DIR: str
    PAPERLESS_USERNAME: str
    PAPERLESS_PASSWORD: str
    PAPERLESS_EMAIL: str
    DOCKERCOMPOSEVERSION: str
    SECRETKEY: str
    PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY: str
    PAPERLESS_OCR_USER_ARGS: str
    PAPERLESS_TASK_WORKERS: int
    PAPERLESS_THREADS_PER_WORKER: int
    PAPERLESS_WORKER_TIMEOUT: int
    PAPERLESS_ENABLE_NLTK: bool
    PAPERLESS_EMAIL_TASK_CRON: str
    PAPERLESS_TRAIN_TASK_CRON: str
    PAPERLESS_INDEX_TASK_CRON: str
    PAPERLESS_SANITY_TASK_CRON: str
    PAPERLESS_ENABLE_COMPRESSION: bool
    PAPERLESS_CONVERT_MEMORY_LIMIT: int
    PAPERLESS_CONVERT_TMPDIR: str
    PAPERLESS_APPS: str
    PAPERLESS_MAX_IMAGE_PIXELS: int
    PAPERLESS_CONSUMER_DELETE_DUPLICATES: bool
    PAPERLESS_CONSUMER_RECURSIVE: bool
    PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS: bool
    #PAPERLESS_CONSUMER_IGNORE_PATTERNS: str
    PAPERLESS_CONSUMER_BARCODE_SCANNER: str
    PAPERLESS_PRE_CONSUME_SCRIPT: str
    PAPERLESS_POST_CONSUME_SCRIPT: str
    PAPERLESS_FILENAME_DATE_ORDER: str
    PAPERLESS_NUMBER_OF_SUGGESTED_DATES: int
    PAPERLESS_THUMBNAIL_FONT_NAME: str
    PAPERLESS_IGNORE_DATES: str
    PAPERLESS_DATE_ORDER: str
    PAPERLESS_CONSUMER_POLLING: int
    PAPERLESS_CONSUMER_POLLING_RETRY_COUNT: int
    PAPERLESS_CONSUMER_POLLING_DELAY: int
    PAPERLESS_CONSUMER_INOTIFY_DELAY: float
    PAPERLESS_CONSUMER_ENABLE_BARCODES: bool
    PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT: bool
    PAPERLESS_CONSUMER_BARCODE_STRING: str
    PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE: bool
    PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX: str
    PAPERLESS_CONSUMER_BARCODE_UPSCALE: float
    PAPERLESS_CONSUMER_BARCODE_DPI: int
    PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE: bool
    PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING: str
    PAPERLESS_AUDIT_LOG_ENABLED: bool
    PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED: bool
    PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME: str
    #PAPERLESS_CONVERT_BINARY: str
    #PAPERLESS_GS_BINARY: str
    PAPERLESS_WEBSERVER_WORKERS: int
    PAPERLESS_BIND_ADDR: str
    PAPERLESS_PORT: int
    PAPERLESS_OCR_LANGUAGES: list
    PAPERLESS_ENABLE_FLOWER: bool
    PAPERLESS_SUPERVISORD_WORKING_DIR: str
    PAPERLESS_APP_TITLE: str
    PAPERLESS_APP_LOGO: str
    PAPERLESS_ENABLE_UPDATE_CHECK: bool
    PAPERLESS_EMAIL_HOST: str
    PAPERLESS_EMAIL_PORT: str
    PAPERLESS_EMAIL_HOST_USER: str
    PAPERLESS_EMAIL_FROM: str
    PAPERLESS_EMAIL_HOST_PASSWORD: str
    PAPERLESS_EMAIL_USE_TLS: bool
    PAPERLESS_EMAIL_USE_SSL: bool
    PAPERLESS_REDIS_URL: str
    PAPERLESS_REDIS_PREFIX: str
    PAPERLESS_DBENGINE: str
    env_vars: dict

    def __init__(self):
        nextcloud_config_path = '/var/www/nextcloud/config/config.php'
        redis_config_path = '/etc/redis/redis.conf'

        print(f"Is readable: {os.access(nextcloud_config_path, os.R_OK)}")
        print(f"Is writable: {os.access(nextcloud_config_path, os.W_OK)}")
        print(f"Is executable: {os.access(nextcloud_config_path, os.X_OK)}")

        self.OS_USER = os.getlogin()

        # create new ubuntu user
        username = "paperless"
        try:
            subprocess.run(["id", username], check=True)
        except subprocess.CalledProcessError:
            subprocess.run(["sudo", "useradd", "-m", "-s", "/bin/bash", username])
            subprocess.run(["sudo", "groupadd", "paperless"])
            subprocess.run(["sudo", "usermod", "-aG", "paperless", username])
        

        # Read the Nextcloud config file content
        with open(nextcloud_config_path, 'r') as file:
            config_content = file.read()

        print("in parse_nextcloud_config")
        nextcloud_config = parse_nextcloud_config(config_content)
        if nextcloud_config is None:
            raise ValueError("Failed to parse Nextcloud config.")



        # Parse Redis config
        parsed_redis = parse_redis_conf(redis_config_path)


        self.REDISHOST = parsed_redis.get('bind', '127.0.0.1').split()[0]  # Default to localhost if not specified
        print(f"Redis host: {self.REDISHOST}")
        self.REDISPORT = parsed_redis.get('port', '6379')  # Default to 6379 if not specified
        print(f"Redis port: {self.REDISPORT}")
        self.REDIS_PASSWORD = parsed_redis.get('requirepass')
        print(f"Redis password: {self.REDIS_PASSWORD}")
        self.REDIS_SOCK = parsed_redis.get('unixsocket')
        print(f"Redis socket: {self.REDIS_SOCK}")
        self.REDIS_SOCK_PERM = parsed_redis.get('unixsocketperm')
        print(f"Redis socket permissions: {self.REDIS_SOCK_PERM}")
        if self.REDIS_SOCK is not None:
            self.REDIS_SOCK_URL = f'redis+socket://{self.REDIS_SOCK}'
        else:
            self.REDIS_SOCK_URL = f'redis://{self.REDISHOST}:{self.REDISPORT}'

        # Extract PostgreSQL configuration from Nextcloud config
        self.NC_POSTGRESHOST = nextcloud_config.get('dbhost')
        print(f"Postgres host: {self.NC_POSTGRESHOST}")
        self.NC_POSTGRESPORT = nextcloud_config.get('dbport', '5432')  # Use default port 5432 if not specified
        print(f"Postgres port: {self.NC_POSTGRESPORT}")
        self.NC_POSTGRESUSER = nextcloud_config.get('dbuser')
        print(f"Postgres user: {self.NC_POSTGRESUSER}")
        # Get PostgreSQL version
        self.POSTGRESQLV = gco("psql --version | head -n 1 | awk '{print $3}' | cut -d'.' -f1")
        print(f"PostgreSQL version: {self.POSTGRESQLV}")

        # Get PostgreSQL port from configuration file
        if self.POSTGRESQLV:
            self.POSTGRESPORT = gco(f"sudo grep '^port' /etc/postgresql/{self.POSTGRESQLV}/main/postgresql.conf | awk '{{print $3}}'")
            print(f"PostgreSQL port from config: {self.POSTGRESPORT}")

            # Get PostgreSQL host from configuration file
            self.POSTGRESHOST = gco(f"sudo grep -E '^#?listen_addresses' /etc/postgresql/{self.POSTGRESQLV}/main/postgresql.conf | awk '{{print $3}}' | sed \"s/'//g\"")
            print(f"PostgreSQL host from config: {self.POSTGRESHOST}")
            
            # Check if paperless_user exists and create if it does not
            self.POSTGRESUSER = gco("sudo -u postgres psql -tAc \"SELECT 1 FROM pg_roles WHERE rolname='paperless_user'\"")
            if self.POSTGRESUSER != '1':
                gco("sudo -u postgres psql -c \"CREATE USER paperless_user WITH PASSWORD 'paperless';\"")
                self.POSTGRESUSER = "paperless_user"
                self.POSTGRESPASSWORD = "paperless"
            else:
                print("User already exists")
                self.POSTGRESUSER = "paperless_user"
                self.POSTGRESPASSWORD = "paperless"

        print(f"Postgres user: {self.POSTGRESUSER}")
        print(f"Postgres password: {self.POSTGRESPASSWORD}")

        # Check if the database exists and create if it does not
        self.POSTGRESDB = gco("sudo -u postgres psql -tAc \"SELECT 1 FROM pg_database WHERE datname='paperless_db'\"")
        if self.POSTGRESDB != '1':
            gco("sudo -u postgres psql -c \"CREATE DATABASE paperless_db OWNER paperless_user;\"")
            self.POSTGRESDB = "paperless_db"
        else:
            print("Database already exists")
            self.POSTGRESDB = "paperless_db"

        print(f"Postgres database: {self.POSTGRESDB}")



        # Nextcloud Config
        self.URL = get_nextcloud_config_value('overwrite.cli.url', nextcloud_config_path)
        self.PORT = 8010  # Default port

        # Default Languages and OCR Languages Array
        self.DEFAULT_PHONE_REGION = get_nextcloud_config_value('default_phone_region', nextcloud_config_path)
        if self.DEFAULT_PHONE_REGION:
            self.DEFAULTLANGUAGES = [self.DEFAULT_PHONE_REGION.lower()]
            self.OCRLANGUAGESARRAY = [get_three_letter_code(self.DEFAULT_PHONE_REGION.lower())]
        else:
            self.DEFAULTLANGUAGES = ["en"]
            self.OCRLANGUAGESARRAY = ["eng"]

        self.PAPERLESS_TIME_ZONE = nextcloud_config.get('logtimezone')
        self.PAPERLESS_ALLOWED_HOSTS = ",".join(nextcloud_config.get('trusted_domains', []))
        self.PAPERLESS_CORS_ALLOWED_HOSTS = ",".join(nextcloud_config.get('trusted_domains', []))

        # Ensure docker-compose is installed
        ensure_docker_compose_installed()

        # Other configurations
        self.USERMAPUID = int(gco("id -u"))
        self.USERMAPGID = int(gco("id -g"))
        self.DATABASEBACKEND = "postgresql"
        self.TIKAENABLED = "false"
        self.OCRLANGUAGE = self.OCRLANGUAGESARRAY[0]
        self.PAPERLESS_STATICDIR = "/mnt/paperless/static"
        self.PAPERLESS_MEDIA_ROOT = "/mnt/paperless/media"
        self.PAPERLESS_CONSUME_DIR = "/mnt/paperless/consume"
        self.PAPERLESS_DATA_DIR = "/mnt/paperless/data"
        self.PAPERLESS_TRASH_DIR = "/mnt/paperless/trash"
        self.PAPERLESS_USERNAME = "admin"
        self.PAPERLESS_PASSWORD = "admin"
        self.PAPERLESS_EMAIL = input("Enter your email for paperless admin: ")

        try:
            self.DOCKERCOMPOSEVERSION = gco("docker-compose --version | awk '{print $3}' | sed 's/,//'")
        except subprocess.CalledProcessError as e:
            print(f"Error executing docker-compose command: {e}")
            self.DOCKERCOMPOSEVERSION = "docker-compose not found"

        self.SECRETKEY = generate_strong_password()

        # Default values for remaining variables
        self.PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY = "RGB"
        self.PAPERLESS_OCR_USER_ARGS = '{"deskew": true, "optimize": 3}'
        self.PAPERLESS_TASK_WORKERS = int(gco("echo 4"))
        self.PAPERLESS_THREADS_PER_WORKER = int(gco("echo 2"))
        self.PAPERLESS_WORKER_TIMEOUT = int(gco("echo 1800"))
        self.PAPERLESS_ENABLE_NLTK = gco("echo true").lower() == 'true'
        self.PAPERLESS_EMAIL_TASK_CRON = gco("echo '*/10 * * * *'")
        self.PAPERLESS_TRAIN_TASK_CRON = gco("echo '5 */1 * * *'")
        self.PAPERLESS_INDEX_TASK_CRON = gco("echo '0 0 * * *'")
        self.PAPERLESS_SANITY_TASK_CRON = gco("echo '30 0 * * sun'")
        self.PAPERLESS_ENABLE_COMPRESSION = gco("echo true").lower() == 'true'
        self.PAPERLESS_CONVERT_MEMORY_LIMIT = int(gco("echo 32"))
        self.PAPERLESS_CONVERT_TMPDIR = f"/home/{self.OS_USER}/tmp"
        self.PAPERLESS_APPS = gco("echo 'app1,app2'")
        self.PAPERLESS_MAX_IMAGE_PIXELS = int(gco("echo 10000000"))
        self.PAPERLESS_CONSUMER_DELETE_DUPLICATES = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_RECURSIVE = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS = gco("echo false").lower() == 'false'


        self.PAPERLESS_CONSUMER_BARCODE_SCANNER = gco("echo 'PYZBAR'")
        #self.PAPERLESS_PRE_CONSUME_SCRIPT = gco("echo '/path/to/pre_consume.sh'")
        #self.PAPERLESS_POST_CONSUME_SCRIPT = gco("echo '/path/to/post_consume.sh'")
        self.PAPERLESS_FILENAME_DATE_ORDER = gco("echo 'DMY'")
        self.PAPERLESS_NUMBER_OF_SUGGESTED_DATES = int(gco("echo 3"))
        self.PAPERLESS_THUMBNAIL_FONT_NAME = gco("echo '/usr/share/fonts/liberation/LiberationSerif-Regular.ttf'")
        self.PAPERLESS_IGNORE_DATES = gco("echo '01-01-1970'")
        self.PAPERLESS_DATE_ORDER = gco("echo 'DMY'")
        self.PAPERLESS_CONSUMER_POLLING = 0
        self.PAPERLESS_CONSUMER_POLLING_RETRY_COUNT = 5
        self.PAPERLESS_CONSUMER_POLLING_DELAY = 5
        self.PAPERLESS_CONSUMER_INOTIFY_DELAY = float(0.5)
        self.PAPERLESS_CONSUMER_ENABLE_BARCODES = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_BARCODE_STRING = gco("echo 'PATCHT'")
        self.PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX = gco("echo 'ASN'")
        self.PAPERLESS_CONSUMER_BARCODE_UPSCALE = float(1.0)
        self.PAPERLESS_CONSUMER_BARCODE_DPI = 300
        self.PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING = gco("echo '{\"TAG:(.*)\": \"\\g<1>\"}'")
        self.PAPERLESS_AUDIT_LOG_ENABLED = gco("echo true").lower() == 'true'
        self.PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED = gco("echo false").lower() == 'false'
        self.PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME = gco("echo 'double-sided'")
        self.PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_TIFF_SUPPORT = gco("echo false").lower() == 'false'
        #self.PAPERLESS_CONVERT_BINARY = gco("which convert")
        #self.PAPERLESS_GS_BINARY = gco("which gs")
        self.PAPERLESS_WEBSERVER_WORKERS = 1
        self.PAPERLESS_BIND_ADDR = gco("echo '[::]'")
        self.PAPERLESS_PORT = 8010
        self.PAPERLESS_OCR_LANGUAGES = self.OCRLANGUAGESARRAY
        self.PAPERLESS_ENABLE_FLOWER = gco("echo false").lower() == 'false'
        self.PAPERLESS_SUPERVISORD_WORKING_DIR = gco("echo '/tmp'")
        self.PAPERLESS_APP_TITLE = gco("echo 'Paperless-ngx'")
        self.PAPERLESS_APP_LOGO = gco("echo '/media/logo/logo.png'")
        self.PAPERLESS_ENABLE_UPDATE_CHECK = gco("echo false").lower() == 'false'

        postfix_main_cf = '/etc/postfix/main.cf'
        if os.path.exists(postfix_main_cf):
            self.PAPERLESS_EMAIL_HOST = gco('grep relayhost /etc/postfix/main.cf').split()[1]
            self.PAPERLESS_EMAIL_PORT = '25'
            self.PAPERLESS_EMAIL_HOST_USER = input("Enter SMTP host user: ")
            self.PAPERLESS_EMAIL_FROM = input("Enter SMTP host email address: ")
            self.PAPERLESS_EMAIL_HOST_PASSWORD = input("Enter SMTP host password: ")
            self.PAPERLESS_EMAIL_USE_TLS = input("Use TLS? (y/n): ").lower() == 'y'
            self.PAPERLESS_EMAIL_USE_SSL = input("Use SSL? (y/n): ").lower() == 'y'
        else:
            self.PAPERLESS_EMAIL_HOST = 'localhost'
            self.PAPERLESS_EMAIL_PORT = ''
            self.PAPERLESS_EMAIL_HOST_USER = ''
            self.PAPERLESS_EMAIL_FROM = ''
            self.PAPERLESS_EMAIL_HOST_PASSWORD = ''
            self.PAPERLESS_EMAIL_USE_TLS = False
            self.PAPERLESS_EMAIL_USE_SSL = False
        self.PAPERLESS_REDIS_URL = f"redis://{self.REDISHOST}:{self.REDISPORT}"
        self.PAPERLESS_REDIS_PREFIX = "paperless"
        self.PAPERLESS_DBENGINE = self.DATABASEBACKEND
        self.PAPERLESS_DBHOST = self.POSTGRESHOST
        self.PAPERLESS_DBPORT = self.POSTGRESPORT
        self.PAPERLESS_DBNAME = gco("echo 'paperless_db'")
        self.PAPERLESS_DBUSER = gco("echo 'paperless'")
        self.PAPERLESS_DBPASS = gco("echo 'paperless'")
        self.PAPERLESS_DBSSLMODE = gco("echo 'prefer'")
        self.PAPERLESS_DBSSLROOTCERT = gco("echo '/etc/ssl/certs/ca-certificates.crt'")
        self.PAPERLESS_DBSSLCERT = gco("echo '/etc/ssl/client-cert'")

        self.env_vars = {
            "URL": self.URL,
            "PORT": self.PORT,
            "DEFAULTLANGUAGES": self.DEFAULTLANGUAGES,
            "OCRLANGUAGESARRAY": self.OCRLANGUAGESARRAY,
            "REDISHOST": self.REDISHOST,
            "REDISPORT": self.REDISPORT,
            "REDIS_SOCK": self.REDIS_SOCK,
            "REDIS_SOCK_PERM": self.REDIS_SOCK_PERM,
            "REDIS_SOCK_URL": self.REDIS_SOCK_URL,
            "REDIS_PASSWORD": self.REDIS_PASSWORD,
            "POSTGRESHOST": self.POSTGRESHOST,
            "POSTGRESUSER": self.POSTGRESUSER,
            "POSTGRESDB": self.DATABASEBACKEND,
            "POSTGRESPASSWORD": self.POSTGRESPASSWORD,
            "PAPERLESS_TIME_ZONE": self.PAPERLESS_TIME_ZONE,
            "PAPERLESS_ALLOWED_HOSTS": self.PAPERLESS_ALLOWED_HOSTS,
            "PAPERLESS_CORS_ALLOWED_HOSTS": self.PAPERLESS_CORS_ALLOWED_HOSTS,
            "USERMAPUID": self.USERMAPUID,
            "USERMAPGID": self.USERMAPGID,
            "DATABASEBACKEND": self.DATABASEBACKEND,
            "TIKAENABLED": self.TIKAENABLED,
            "OCRLANGUAGE": self.OCRLANGUAGE,
            "PAPERLESS_STATICDIR": self.PAPERLESS_STATICDIR,
            "PAPERLESS_MEDIA_ROOT": self.PAPERLESS_MEDIA_ROOT,
            "PAPERLESS_CONSUME_DIR": self.PAPERLESS_CONSUME_DIR,
            "PAPERLESS_DATA_DIR": self.PAPERLESS_DATA_DIR,
            "PAPERLESS_TRASH_DIR": self.PAPERLESS_TRASH_DIR,
            "PAPERLESS_USERNAME": self.PAPERLESS_USERNAME,
            "PAPERLESS_PASSWORD": self.PAPERLESS_PASSWORD,
            "PAPERLESS_EMAIL": self.PAPERLESS_EMAIL,
            "DOCKERCOMPOSEVERSION": self.DOCKERCOMPOSEVERSION,
            "SECRETKEY": self.SECRETKEY,
            "PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY": self.PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY,
            "PAPERLESS_OCR_USER_ARGS": self.PAPERLESS_OCR_USER_ARGS,
            "PAPERLESS_TASK_WORKERS": self.PAPERLESS_TASK_WORKERS,
            "PAPERLESS_THREADS_PER_WORKER": self.PAPERLESS_THREADS_PER_WORKER,
            "PAPERLESS_WORKER_TIMEOUT": self.PAPERLESS_WORKER_TIMEOUT,
            "PAPERLESS_ENABLE_NLTK": self.PAPERLESS_ENABLE_NLTK,
            "PAPERLESS_EMAIL_TASK_CRON": self.PAPERLESS_EMAIL_TASK_CRON,
            "PAPERLESS_TRAIN_TASK_CRON": self.PAPERLESS_TRAIN_TASK_CRON,
            "PAPERLESS_INDEX_TASK_CRON": self.PAPERLESS_INDEX_TASK_CRON,
            "PAPERLESS_SANITY_TASK_CRON": self.PAPERLESS_SANITY_TASK_CRON,
            "PAPERLESS_ENABLE_COMPRESSION": self.PAPERLESS_ENABLE_COMPRESSION,
            "PAPERLESS_CONVERT_MEMORY_LIMIT": self.PAPERLESS_CONVERT_MEMORY_LIMIT,
            "PAPERLESS_CONVERT_TMPDIR": self.PAPERLESS_CONVERT_TMPDIR,
            "PAPERLESS_APPS": self.PAPERLESS_APPS,
            "PAPERLESS_MAX_IMAGE_PIXELS": self.PAPERLESS_MAX_IMAGE_PIXELS,
            "PAPERLESS_CONSUMER_DELETE_DUPLICATES": self.PAPERLESS_CONSUMER_DELETE_DUPLICATES,
            "PAPERLESS_CONSUMER_RECURSIVE": self.PAPERLESS_CONSUMER_RECURSIVE,
            "PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS": self.PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS,
            #"PAPERLESS_CONSUMER_IGNORE_PATTERNS": self.PAPERLESS_CONSUMER_IGNORE_PATTERNS,
            "PAPERLESS_CONSUMER_BARCODE_SCANNER": self.PAPERLESS_CONSUMER_BARCODE_SCANNER,
            #"PAPERLESS_PRE_CONSUME_SCRIPT": self.PAPERLESS_PRE_CONSUME_SCRIPT,
            #"PAPERLESS_POST_CONSUME_SCRIPT": self.PAPERLESS_POST_CONSUME_SCRIPT,
            "PAPERLESS_FILENAME_DATE_ORDER": self.PAPERLESS_FILENAME_DATE_ORDER,
            "PAPERLESS_NUMBER_OF_SUGGESTED_DATES": self.PAPERLESS_NUMBER_OF_SUGGESTED_DATES,
            "PAPERLESS_THUMBNAIL_FONT_NAME": self.PAPERLESS_THUMBNAIL_FONT_NAME,
            "PAPERLESS_IGNORE_DATES": self.PAPERLESS_IGNORE_DATES,
            "PAPERLESS_DATE_ORDER": self.PAPERLESS_DATE_ORDER,
            "PAPERLESS_CONSUMER_POLLING": self.PAPERLESS_CONSUMER_POLLING,
            "PAPERLESS_CONSUMER_POLLING_RETRY_COUNT": self.PAPERLESS_CONSUMER_POLLING_RETRY_COUNT,
            "PAPERLESS_CONSUMER_POLLING_DELAY": self.PAPERLESS_CONSUMER_POLLING_DELAY,
            "PAPERLESS_CONSUMER_INOTIFY_DELAY": self.PAPERLESS_CONSUMER_INOTIFY_DELAY,
            "PAPERLESS_CONSUMER_ENABLE_BARCODES": self.PAPERLESS_CONSUMER_ENABLE_BARCODES,
            "PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT": self.PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT,
            "PAPERLESS_CONSUMER_BARCODE_STRING": self.PAPERLESS_CONSUMER_BARCODE_STRING,
            "PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE": self.PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE,
            "PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX": self.PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX,
            "PAPERLESS_CONSUMER_BARCODE_UPSCALE": self.PAPERLESS_CONSUMER_BARCODE_UPSCALE,
            "PAPERLESS_CONSUMER_BARCODE_DPI": self.PAPERLESS_CONSUMER_BARCODE_DPI,
            "PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE": self.PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE,
            "PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING": self.PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING,
            "PAPERLESS_AUDIT_LOG_ENABLED": self.PAPERLESS_AUDIT_LOG_ENABLED,
            "PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED": self.PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED,
            "PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME": self.PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME,
            "PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_TIFF_SUPPORT": self.PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_TIFF_SUPPORT,
            #"PAPERLESS_CONVERT_BINARY": self.PAPERLESS_CONVERT_BINARY,
            #"PAPERLESS_GS_BINARY": self.PAPERLESS_GS_BINARY,
            "PAPERLESS_WEBSERVER_WORKERS": self.PAPERLESS_WEBSERVER_WORKERS,
            "PAPERLESS_BIND_ADDR": self.PAPERLESS_BIND_ADDR,
            "PAPERLESS_PORT": self.PAPERLESS_PORT,
            "PAPERLESS_OCR_LANGUAGES": self.OCRLANGUAGESARRAY,
            "PAPERLESS_ENABLE_FLOWER": self.PAPERLESS_ENABLE_FLOWER,
            "PAPERLESS_SUPERVISORD_WORKING_DIR": self.PAPERLESS_SUPERVISORD_WORKING_DIR,
            "PAPERLESS_APP_TITLE": self.PAPERLESS_APP_TITLE,
            "PAPERLESS_APP_LOGO": self.PAPERLESS_APP_LOGO,
            "PAPERLESS_ENABLE_UPDATE_CHECK": self.PAPERLESS_ENABLE_UPDATE_CHECK,
            "PAPERLESS_EMAIL_HOST": self.PAPERLESS_EMAIL_HOST,
            "PAPERLESS_EMAIL_PORT": self.PAPERLESS_EMAIL_PORT,
            "PAPERLESS_EMAIL_HOST_USER": self.PAPERLESS_EMAIL_HOST_USER,
            "PAPERLESS_EMAIL_FROM": self.PAPERLESS_EMAIL_FROM,
            "PAPERLESS_EMAIL_HOST_PASSWORD": self.PAPERLESS_EMAIL_HOST_PASSWORD,
            "PAPERLESS_EMAIL_USE_TLS": self.PAPERLESS_EMAIL_USE_TLS,
            "PAPERLESS_EMAIL_USE_SSL": self.PAPERLESS_EMAIL_USE_SSL,
            "PAPERLESS_REDIS_URL": self.PAPERLESS_REDIS_URL,
            "PAPERLESS_REDIS_PREFIX": self.PAPERLESS_REDIS_PREFIX,
            "PAPERLESS_DBENGINE": self.PAPERLESS_DBENGINE,
            "PAPERLESS_DBHOST": self.POSTGRESHOST,
            "PAPERLESS_DBPORT": self.POSTGRESPORT,
            "PAPERLESS_DBNAME": self.POSTGRESDB,
            "PAPERLESS_DBUSER": self.POSTGRESUSER,
            "PAPERLESS_DBPASS": self.POSTGRESPASSWORD,
            "PAPERLESS_DBSSLMODE": self.PAPERLESS_DBSSLMODE,
            "PAPERLESS_DBSSLROOTCERT": self.PAPERLESS_DBSSLROOTCERT,
            "PAPERLESS_DBSSLCERT": self.PAPERLESS_DBSSLCERT
        }

    def save_env_variables(self):
        with open('env_vars.json', 'w') as file:
            json.dump(self.env_vars, file, indent=4)

