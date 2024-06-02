from functions import check_docker_daemon, check_file_permissions, get_env_variables, get_process_info, get_filesystem_info, updater, gco
from Ledger import Ledger
from paperless import generate_docker_compose, generate_docker_env, verify_installed_packages
import os

def main():
    check_file_permissions("/var/www/nextcloud/config/config.php")
    ledger = Ledger()

    new_vars = get_env_variables()
    new_procs = get_process_info()
    new_dirs = get_filesystem_info()
    
    updater(ledger.env_vars, new_vars)
    updater(ledger.env_vars, new_procs)
    updater(ledger.env_vars, new_dirs)

    ledger.save_env_variables()

    def delete_docker_files():
        file_extensions = ['.yaml', '.env']
        file_names = ['docker-compose' + ext for ext in file_extensions]

        for file_name in file_names:
            file_path = os.path.join('/var/scripts/service-API', file_name)
            if os.path.exists(file_path):
                os.remove(file_path)

    # Call the function to delete the files
    delete_docker_files()

    # Generate Docker Compose and Env files
    print("Generating Docker Compose YAML file...")
    generate_docker_compose(ledger.env_vars)
    print("Generating Docker environment file...")
    generate_docker_env(ledger.env_vars)

    # Verify installed packages
    verify_installed_packages()
    print("Done.")

    gco('docker-compose up -d')

if __name__ == "__main__":
    main()
