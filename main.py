from functions import check_file_permissions, get_env_variables, get_process_info, get_filesystem_info, updater
from Ledger import Ledger
from paperless import generate_docker_compose


def main():
    check_file_permissions("nextcloud/service-API/debug-nc-config.php")
    ledger = Ledger()



    new_vars = get_env_variables()
    new_procs = get_process_info()
    new_dirs = get_filesystem_info()
    
    updater(ledger.env_vars, new_vars)
    updater(ledger.env_vars, new_procs)
    updater(ledger.env_vars, new_dirs)


    ledger.save_env_variables()
    #ledger.store_in_redis()
    generate_docker_compose(ledger.env_vars)

if __name__ == "__main__":
    ledger = Ledger()
    filesystem_info = get_filesystem_info()


    main()
