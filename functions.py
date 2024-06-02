import json
import os
import redis
import secrets
import stat
import string
import subprocess
import sys
from typing import Any, Callable, Dict, List, Type, TypeVar, cast



# --------------------------------
# Load/Save Environment Variables
# --------------------------------

nextcloud_config_path = "/var/www/nextcloud/config/config.php"
ledger_config_path = "/var/scripts/service-API/env_variables.json"
with open(ledger_config_path, 'r') as file:
    env_vars = json.load(file)


def save_env_variables(env_vars):
    with open('/var/scripts/service-API/env_variables.json', 'w') as file:
        json.dump(env_vars, file, indent=4)

def get_env_variables():
    if os.path.exists('/var/scripts/service-API/env_variables.json'):
        with open('/var/scripts/service-API/env_variables.json', 'r') as file:
            return json.load(file)
    return {}

def store_in_redis(env_vars):
    print(f"env_vars: {env_vars}")
    
    try:
        r = redis.Redis(host=env_vars['REDISHOST'], port=env_vars['REDISPORT'], db=0)
        r.ping()
        for key, value in env_vars.items():
            r.set(key, value)
        print("Redis is running and data stored successfully.")
    except redis.ConnectionError:
        print("Redis is not running. Unable to store data.")

# --------------------------------
# Data Processing Functions
# --------------------------------

T = TypeVar("T")

def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x

def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]

def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()

def check_file_permissions(file_path):
    st = os.stat(file_path)
    print(f"Is readable: {bool(st.st_mode & stat.S_IRUSR)}")
    print(f"Is writable: {bool(st.st_mode & stat.S_IWUSR)}")
    print(f"Is executable: {bool(st.st_mode & stat.S_IXUSR)}")

#def gco(command: str) -> str:
#    return subprocess.check_output(command, shell=True).decode('utf-8').strip()

def gco(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {result.stderr}")
        return result.stdout.strip()
    except Exception as e:
        print(f"An error occurred: {e}")


def check_docker_daemon():
    try:
        subprocess.run("docker info", shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return True
    except subprocess.CalledProcessError:
        print("Docker daemon is not running. Attempting to start Docker...")

        # Start Docker daemon
        try:
            gco("sudo systemctl start docker")
            print("Docker daemon started.")
        except RuntimeError:
            print("Failed to start Docker daemon.")
            return False

        # Enable Docker daemon at boot
        try:
            gco("sudo systemctl enable docker")
            print("Docker daemon enabled to start at boot.")
        except RuntimeError:
            print("Failed to enable Docker daemon at boot.")
            return False

        # Check if user is in the docker group
        user = os.getenv("USER")
        groups = gco(f"groups {user}")
        if "docker" not in groups:
            try:
                gco(f"sudo usermod -aG docker {user}")
                print(f"User {user} added to docker group. Please log out and log back in for the changes to take effect.")
                return False  # Ask user to log out and log back in
            except RuntimeError:
                print(f"Failed to add user {user} to docker group.")
                return False

        # Set permissions for Docker socket
        try:
            gco("sudo chown root:docker /var/run/docker.sock")
            gco("sudo chmod 660 /var/run/docker.sock")
            print("Docker socket permissions set.")
        except RuntimeError:
            print("Failed to set Docker socket permissions.")
            return False

        # Restart Docker daemon
        try:
            gco("sudo systemctl restart docker")
            print("Docker daemon restarted.")
        except RuntimeError:
            print("Failed to restart Docker daemon.")
            return False

        # Check and set DOCKER_HOST environment variable
        docker_host = os.getenv("DOCKER_HOST")
        if docker_host != "unix:///var/run/docker.sock":
            os.environ["DOCKER_HOST"] = "unix:///var/run/docker.sock"
            print("DOCKER_HOST environment variable set to unix:///var/run/docker.sock")

        # Verify Docker daemon status
        try:
            gco("sudo systemctl status docker")
            print("Docker daemon is running.")
            return True
        except RuntimeError:
            print("Docker daemon is not running.")
            return False
        
def generate_strong_password(length: int = 16) -> str:
    # Exclude single quote (') and double quote (") for the docker-compose template so that the password can be used as an environment variable
    characters = string.ascii_letters + string.digits + "!#$%&()*+,-./:;<=>?@[\\]^_`{|}~"
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password.replace('$', '$$')  # Escape the $ character for docker-compose

def get_default_time_zone():
    return gco("timedatectl show -p Timezone --value")

def locate(search_term: str, arg_type: str) -> dict:
    try:
        result = subprocess.run(['plocate', search_term, arg_type], capture_output=True, text=True).stdout
        path, arg = result.split()
        return {"path": path, "arg_type": arg_type, "arg": arg}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}

def ensure_docker_compose_installed():
    try:
        subprocess.check_output("docker-compose --version", shell=True).decode('utf-8').strip()
        print("docker-compose is already installed.")
    except subprocess.CalledProcessError:
        print("docker-compose not found. Installing...")
        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                subprocess.check_call("sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose", shell=True)
                subprocess.check_call("sudo chmod +x /usr/local/bin/docker-compose", shell=True)
            print("docker-compose installed successfully.")
        except Exception as e:
            print(f"Failed to install docker-compose: {e}")
            sys.exit(1)

def get_nextcloud_config_value(key: str, file_path: str = nextcloud_config_path) -> str:
    with open(file_path, 'r') as file:
        for line in file:
            if f"'{key}'" in line:
                return line.split("=>")[1].strip().strip("',")
    return None

def get_redis_conf_value(key: str, file_path: str) -> str:
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(key):
                return line.split()[1]
    return None

def get_postgres_version() -> str:
    version_output = gco("psql --version")
    return version_output.split()[2]

def get_three_letter_code(language: str) -> str:
    country_code_map = {
        "en": "eng",
        "fr": "fra",
        "de": "deu",
        "es": "spa",
        "it": "ita",
    }
    return country_code_map.get(language, "eng")

# --------------------------------------
# Tools for establishing system state
# --------------------------------------

def updater(old, new):
    if old != new:
        old = new
        save_env_variables(new)
        #store_in_redis(new)

def get_process_info():
    processes = gco("ps aux").splitlines()
    process_list = []
    for process in processes[1:]:
        process_info = process.split()
        process_list.append({
            "user": process_info[0],
            "pid": process_info[1],
            "cpu": process_info[2],
            "mem": process_info[3],
            "command": " ".join(process_info[10:])
        })
    return process_list

def get_filesystem_info():
    try:
        # Run the tree command
        result = subprocess.run(
            ["sudo", "tree", "-dJTC", "--prune", "--inodes", "-guhpL", "3", "/var"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the JSON output
        filesystem_info = json.loads(result.stdout)
        
        # Save to a JSON file
        with open("filesystem.json", "w") as file:
            json.dump(filesystem_info, file, indent=4)
        
        return filesystem_info
    
    except subprocess.CalledProcessError as e:
        print(f"Error running tree command: {e}")
        return {}


def get_permissions_info():
    permissions_info = []
    for root, dirs, files in os.walk('/'):
        for name in dirs + files:
            path = os.path.join(root, name)
            try:
                stat_info = os.stat(path)
                permissions_info.append({
                    "path": path,
                    "owner": stat_info.st_uid,
                    "group": stat_info.st_gid,
                    "permissions": oct(stat_info.st_mode)[-3:]
                })
            except FileNotFoundError:
                continue
    return permissions_info

def parse_nextcloud_config(config_content: str) -> dict:
    def parse_value(value):
        value = value.strip().strip("',")
        if value == 'true':
            return True
        elif value == 'false':
            return False
        elif value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)
        return value
    
    def parse_array(lines, index):
        config_dict = {}
        key = None
        while index < len(lines):
            line = lines[index].strip()
            if line.startswith(")"):
                return config_dict, index
            elif "=>" in line:
                parts = line.split("=>", 1)
                if len(parts) != 2:
                    index += 1
                    continue
                key, value = map(str.strip, parts)
                key = key.strip("'")
                if value == "array (":
                    nested_array, index = parse_array(lines, index + 1)
                    config_dict[key] = nested_array
                elif value.startswith("array ("):
                    nested_array, index = parse_array(lines, index)
                    config_dict[key] = nested_array
                else:
                    config_dict[key] = parse_value(value)
            elif key and line.startswith('array ('):
                nested_array, index = parse_array(lines, index)
                config_dict[key] = nested_array
            else:
                if key:
                    config_dict[key] = parse_value(line)
            index += 1
        return config_dict, index

    lines = config_content.splitlines()
    config_dict, _ = parse_array(lines, 2)
    return config_dict




def parse_redis_conf(redis_conf_path: str) -> dict:
    config_dict = {}
    with open(redis_conf_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        if line.startswith('#') or not line.strip():
            continue
        parts = line.split(maxsplit=1)  # Split only on the first whitespace
        if len(parts) != 2:
            print(f"Warning: Unexpected line in config: {line}")
            continue
        key, value = parts
        config_dict[key] = value.strip()
    return config_dict
