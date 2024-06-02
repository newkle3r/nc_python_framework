import shutil
from jinja2 import Template


docker_compose_template = """
version: '3.7'
services:
  webserver:
    image: 'ghcr.io/paperless-ngx/paperless-ngx:latest'
    restart: 'unless-stopped'
    networks: 
      - paperless-net
    environment:
      PAPERLESS_REDIS: '{{REDIS_SOCK_URL}}'
      PAPERLESS_DBHOST: '{{POSTGRESHOST}}'
      PAPERLESS_DBNAME: '{{POSTGRESDB}}'
      PAPERLESS_DBUSER: '{{POSTGRESUSER}}'
      PAPERLESS_DBPASS: '{{POSTGRESPASSWORD}}'
      PAPERLESS_TIME_ZONE: '{{PAPERLESS_TIME_ZONE}}'
      PAPERLESS_ALLOWED_HOSTS: '{{PAPERLESS_ALLOWED_HOSTS}}'
      PAPERLESS_CORS_ALLOWED_HOSTS: '{{PAPERLESS_CORS_ALLOWED_HOSTS}}'
      USERMAPUID: '{{USERMAPUID}}'
      USERMAPGID: '{{USERMAPGID}}'
      DATABASEBACKEND: '{{DATABASEBACKEND}}'
      TIKAENABLED: '{{TIKAENABLED}}'
      OCRLANGUAGE: '{{OCRLANGUAGE}}'
      PAPERLESS_STATICDIR: '{{PAPERLESS_STATICDIR}}'
      PAPERLESS_MEDIA_ROOT: '{{PAPERLESS_MEDIA_ROOT}}'
      PAPERLESS_CONSUME_DIR: '{{PAPERLESS_CONSUME_DIR}}'
      PAPERLESS_DATA_DIR: '{{PAPERLESS_DATA_DIR}}'
      PAPERLESS_TRASH_DIR: '{{PAPERLESS_TRASH_DIR}}'
      PAPERLESS_USERNAME: '{{PAPERLESS_USERNAME}}'
      PAPERLESS_PASSWORD: '{{PAPERLESS_PASSWORD}}'
      PAPERLESS_EMAIL: '{{PAPERLESS_EMAIL}}'
      DOCKERCOMPOSEVERSION: '{{DOCKERCOMPOSEVERSION}}'
      SECRETKEY: '{{SECRETKEY}}'
      PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY: '{{PAPERLESS_OCR_COLOR_CONVERSION_STRATEGY}}'
      PAPERLESS_OCR_USER_ARGS: '{{PAPERLESS_OCR_USER_ARGS}}'
      PAPERLESS_TASK_WORKERS: '{{PAPERLESS_TASK_WORKERS}}'
      PAPERLESS_THREADS_PER_WORKER: '{{PAPERLESS_THREADS_PER_WORKER}}'
      PAPERLESS_WORKER_TIMEOUT: '{{PAPERLESS_WORKER_TIMEOUT}}'
      PAPERLESS_ENABLE_NLTK: '{{PAPERLESS_ENABLE_NLTK}}'
      PAPERLESS_EMAIL_TASK_CRON: '{{PAPERLESS_EMAIL_TASK_CRON}}'
      PAPERLESS_TRAIN_TASK_CRON: '{{PAPERLESS_TRAIN_TASK_CRON}}'
      PAPERLESS_INDEX_TASK_CRON: '{{PAPERLESS_INDEX_TASK_CRON}}'
      PAPERLESS_SANITY_TASK_CRON: '{{PAPERLESS_SANITY_TASK_CRON}}'
      PAPERLESS_ENABLE_COMPRESSION: '{{PAPERLESS_ENABLE_COMPRESSION}}'
      PAPERLESS_CONVERT_MEMORY_LIMIT: '{{PAPERLESS_CONVERT_MEMORY_LIMIT}}'
      PAPERLESS_CONVERT_TMPDIR: '{{PAPERLESS_CONVERT_TMPDIR}}'
      PAPERLESS_APPS: '{{PAPERLESS_APPS}}'
      PAPERLESS_MAX_IMAGE_PIXELS: '{{PAPERLESS_MAX_IMAGE_PIXELS}}'
      PAPERLESS_CONSUMER_DELETE_DUPLICATES: '{{PAPERLESS_CONSUMER_DELETE_DUPLICATES}}'
      PAPERLESS_CONSUMER_RECURSIVE: '{{PAPERLESS_CONSUMER_RECURSIVE}}'
      PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS: '{{PAPERLESS_CONSUMER_SUBDIRS_AS_TAGS}}'
      PAPERLESS_CONSUMER_IGNORE_PATTERNS: '{{PAPERLESS_CONSUMER_IGNORE_PATTERNS}}'
      PAPERLESS_CONSUMER_BARCODE_SCANNER: '{{PAPERLESS_CONSUMER_BARCODE_SCANNER}}'
      PAPERLESS_FILENAME_DATE_ORDER: '{{PAPERLESS_FILENAME_DATE_ORDER}}'
      PAPERLESS_NUMBER_OF_SUGGESTED_DATES: '{{PAPERLESS_NUMBER_OF_SUGGESTED_DATES}}'
      PAPERLESS_THUMBNAIL_FONT_NAME: '{{PAPERLESS_THUMBNAIL_FONT_NAME}}'
      PAPERLESS_IGNORE_DATES: '{{PAPERLESS_IGNORE_DATES}}'
      PAPERLESS_DATE_ORDER: '{{PAPERLESS_DATE_ORDER}}'
      PAPERLESS_CONSUMER_POLLING: '{{PAPERLESS_CONSUMER_POLLING}}'
      PAPERLESS_CONSUMER_POLLING_RETRY_COUNT: '{{PAPERLESS_CONSUMER_POLLING_RETRY_COUNT}}'
      PAPERLESS_CONSUMER_POLLING_DELAY: '{{PAPERLESS_CONSUMER_POLLING_DELAY}}'
      PAPERLESS_CONSUMER_INOTIFY_DELAY: '{{PAPERLESS_CONSUMER_INOTIFY_DELAY}}'
      PAPERLESS_CONSUMER_ENABLE_BARCODES: '{{PAPERLESS_CONSUMER_ENABLE_BARCODES}}'
      PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT: '{{PAPERLESS_CONSUMER_BARCODE_TIFF_SUPPORT}}'
      PAPERLESS_CONSUMER_BARCODE_STRING: '{{PAPERLESS_CONSUMER_BARCODE_STRING}}'
      PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE: '{{PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE}}'
      PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX: '{{PAPERLESS_CONSUMER_ASN_BARCODE_PREFIX}}'
      PAPERLESS_CONSUMER_BARCODE_UPSCALE: '{{PAPERLESS_CONSUMER_BARCODE_UPSCALE}}'
      PAPERLESS_CONSUMER_BARCODE_DPI: '{{PAPERLESS_CONSUMER_BARCODE_DPI}}'
      PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE: '{{PAPERLESS_CONSUMER_ENABLE_TAG_BARCODE}}'
      PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING: '{{PAPERLESS_CONSUMER_TAG_BARCODE_MAPPING}}'
      PAPERLESS_AUDIT_LOG_ENABLED: '{{PAPERLESS_AUDIT_LOG_ENABLED}}'
      PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED: '{{PAPERLESS_CONSUMER_ENABLE_COLLATE_DOUBLE_SIDED}}'
      PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME: '{{PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_SUBDIR_NAME}}'
      PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_TIFF_SUPPORT: '{{PAPERLESS_CONSUMER_COLLATE_DOUBLE_SIDED_TIFF_SUPPORT}}'
      PAPERLESS_CONVERT_BINARY: '{{PAPERLESS_CONVERT_BINARY}}'
      PAPERLESS_GS_BINARY: '{{PAPERLESS_GS_BINARY}}'
      PAPERLESS_WEBSERVER_WORKERS: '{{PAPERLESS_WEBSERVER_WORKERS}}'
      PAPERLESS_BIND_ADDR: '{{PAPERLESS_BIND_ADDR}}'
      PAPERLESS_PORT: '{{PAPERLESS_PORT}}'
      PAPERLESS_OCR_LANGUAGES: '{{PAPERLESS_OCR_LANGUAGES}}'
      PAPERLESS_ENABLE_FLOWER: '{{PAPERLESS_ENABLE_FLOWER}}'
      PAPERLESS_SUPERVISORD_WORKING_DIR: '{{PAPERLESS_SUPERVISORD_WORKING_DIR}}'
      PAPERLESS_APP_TITLE: '{{PAPERLESS_APP_TITLE}}'
      PAPERLESS_APP_LOGO: '{{PAPERLESS_APP_LOGO}}'
      PAPERLESS_ENABLE_UPDATE_CHECK: '{{PAPERLESS_ENABLE_UPDATE_CHECK}}'
      PAPERLESS_EMAIL_HOST: '{{PAPERLESS_EMAIL_HOST}}'
      PAPERLESS_EMAIL_PORT: '{{PAPERLESS_EMAIL_PORT}}'
      PAPERLESS_EMAIL_HOST_USER: '{{PAPERLESS_EMAIL_HOST_USER}}'
      PAPERLESS_EMAIL_FROM: '{{PAPERLESS_EMAIL_FROM}}'
      PAPERLESS_EMAIL_HOST_PASSWORD: '{{PAPERLESS_EMAIL_HOST_PASSWORD}}'
      PAPERLESS_EMAIL_USE_TLS: '{{PAPERLESS_EMAIL_USE_TLS}}'
      PAPERLESS_EMAIL_USE_SSL: '{{PAPERLESS_EMAIL_USE_SSL}}'
      PAPERLESS_REDIS_URL: '{{PAPERLESS_REDIS_URL}}'
      PAPERLESS_REDIS_PREFIX: '{{PAPERLESS_REDIS_PREFIX}}'
      PAPERLESS_DBENGINE: '{{PAPERLESS_DBENGINE}}'
      PAPERLESS_DBSSLMODE: '{{PAPERLESS_DBSSLMODE}}'
      PAPERLESS_DBSSLROOTCERT: '{{PAPERLESS_DBSSLROOTCERT}}'
      PAPERLESS_DBSSLCERT: '{{PAPERLESS_DBSSLCERT}}'
    volumes:
      - {{PAPERLESS_DATA_DIR}}:/usr/src/paperless/data
      - {{PAPERLESS_MEDIA_ROOT}}:/usr/src/paperless/media
      - {{PAPERLESS_STATICDIR}}:/usr/src/paperless/static
      - {{PAPERLESS_CONSUME_DIR}}:/usr/src/paperless/consume
      - {{PAPERLESS_TRASH_DIR}}:/usr/src/paperless/trash
      - {{REDIS_SOCK}}:/var/run/redis/redis-server.sock
    ports:
      - '{{PORT}}:8000'
networks:
  paperless-net:
    driver: bridge
volumes:
  paperless-data: {}
  paperless-media: {}
  paperless-static: {}
  paperless-consume: {}
  paperless-trash: {}
"""

def generate_docker_compose(env_vars):
    template = Template(docker_compose_template)
    docker_compose = template.render(env_vars)
    with open('docker-compose.yaml', 'w') as file:
        file.write(docker_compose)

def generate_docker_env(env_vars):
    with open('docker-compose.env', 'w') as file:
        for key, value in env_vars.items():
            file.write(f"{key}={value}\n")

def verify_installed_packages():
    if not shutil.which("docker-compose"):
        print("docker-compose is not installed.")
        return False
    if not shutil.which("docker"):
        print("docker is not installed.")
        return False
    if not shutil.which("redis-cli"):
        print("redis-cli is not installed.")
        return False
    if not shutil.which("psql"):
        print("psql is not installed.")
        return False
    if not shutil.which("python3"):
        print("python3 is not installed.")
        return False
    if not shutil.which("pip3"):
        print("pip3 is not installed.")
        return False
    if not shutil.which("git"):
        print("git is not installed.")
        return False
    if not shutil.which("curl"):
        print("curl is not installed.")
        return False
    if not shutil.which("wget"):
        print("wget is not installed.")
        return False
    if not shutil.which("unzip"):
        print("unzip is not installed.")
        return False
    if not shutil.which("tar"):
        print("tar is not installed.")
        return False
    if not shutil.which("make"):
        print("make is not installed.")
        return False
    if not shutil.which("gcc"):
        print("gcc is not installed.")
        return False
    if not shutil.which("g++"):
        print("g++ is not installed.")
        return False
    
    return True



