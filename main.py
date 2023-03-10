import json
from getpass import getpass
import sys
import device_list as list
from paramiko import SSHClient, AutoAddPolicy


def get_credentials():
    username = input('Enter username: ')
    password = getpass('Enter password: ')
    return username, password


def main():
    username, password = get_credentials()

    client = SSHClient()
    client.load_host_keys('/home/knapiers/.ssh/known_hosts')
    # client.load_host_keys('C:/Users/knapiers/.ssh/known_hosts')
    client.set_missing_host_key_policy(AutoAddPolicy())

    with open("output.txt", "w") as file:
        for nuc_name, nuc_ip in list.device_list.items():
            print(f"Connecting=={nuc_name}=={nuc_ip}")
            client.connect(nuc_ip, username=username, password=password)
            print(f"Connected=={nuc_name}=={nuc_ip}")

            file.write(f"\n\n======{nuc_name}=={nuc_ip}======")

            file.write("\n===DOCKER STATUS===\n")
            stdout1 = client.exec_command("sudo systemctl status docker | head -4 | grep 'Active'")[1]
            file.write(stdout1.read().decode('utf8'))


            file.write("\n===DISK STATUS===\n")
            stdout2 = client.exec_command("df -h")[1]
            file.write(stdout2.read().decode('utf8'))

            file.write("\n===LINKING STATUS===\n")
            stdout3 = client.exec_command("sudo docker ps -a | awk '{print $1}' | awk 'length($1) >10'")[1]
            container = stdout3.read().decode('utf8')
            stdout4 = client.exec_command(f"sudo docker inspect {container}")[1]
            inspect_string = stdout4.read().decode('utf8')
            json_object = json.loads(inspect_string)
            file.write(json.dumps(json_object[0]['Args'], indent=3))

            print(f"Done=={nuc_name}=={nuc_ip}")


if __name__ == "__main__":
    main()
    sys.exit()