import json
import device_list as list
from paramiko import SSHClient, AutoAddPolicy

def get_credentials():
    username = input('Enter username: ')
    password = input('Enter password: ')
    return username, password


def main():
    username, password = get_credentials()
    file = open("output.txt", "w")

    client = SSHClient()
    client.load_host_keys('/home/knapiers/.ssh/known_hosts')
    #client.load_host_keys('C:/Users/knapiers/.ssh/known_hosts')
    client.set_missing_host_key_policy(AutoAddPolicy())

    for nuc_name, nuc_ip in list.device_list.items():
        print((f"Connecting=={nuc_name}=={nuc_ip}"))
        client.connect(nuc_ip, username=username, password= password)
        print((f"Connected=={nuc_name}=={nuc_ip}"))
        file.write(f"\n\n======{nuc_name}=={nuc_ip}======\n")
        file.write("===DOCKER STATUS===\n")
        stdin1, stdout1, stderr1 = client.exec_command("sudo systemctl status docker | head -4 | grep 'Active'")
        file.write(f"{stdout1.read().decode('utf8')}\n")
        stdin2, stdout2, stderr2 = client.exec_command("sudo docker ps -a | awk '{print $1}' | awk 'length($1) >10'")
        container = stdout2.read().decode('utf8')
        file.write("===DISK STATUS===\n")
        stdin3, stdout3, stderr3 = client.exec_command("df -h")
        file.write(f"{stdout3.read().decode('utf8')}\n")
        file.write("===LINKING STATUS===\n")
        stdin4, stdout4, stderr4 = client.exec_command(f"sudo docker inspect {container}")
        inspect_string = stdout4.read().decode('utf8')
        json_object = json.loads(inspect_string)
        file.write(json.dumps(json_object[0]['Args'], indent=3))
        print((f"Done=={nuc_name}=={nuc_ip}"))
    file.close()


if __name__ == "__main__":
    main()