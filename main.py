import json
import device_list as list
from paramiko import SSHClient, AutoAddPolicy

def get_credentials():
    username = input('Enter username: ')
    password = input('Enter password: ')
    return username, password

def main():
    # [x] get_credentials
    username, password = get_credentials()
    # [x] create file
    file = open("output.txt", "w")

    # [x] loop througt devicese
    client = SSHClient()
    client.load_host_keys('/home/knapiers/.ssh/known_hosts')
    #client.load_host_keys('C:/Users/knapiers/.ssh/known_hosts')
    client.set_missing_host_key_policy(AutoAddPolicy())

    for nuc_name, nuc_ip in list.device_list.items():
    # [x] ssh connection
        print((f"Connecting=={nuc_name}=={nuc_ip}"))
        client.connect(nuc_ip, username=username, password= password)
        print((f"Connected=={nuc_name}=={nuc_ip}"))
        file.write(f"======{nuc_name}=={nuc_ip}======\n")
    # [x] run commands
        file.write("===DOCKER STATUS===\n")
        stdin1, stdout1, stderr1 = client.exec_command("sudo systemctl status docker | head -4 | grep 'Active'")
        file.write(f"{stdout1.read().decode('utf8')}\n")
        stdin2, stdout2, stderr2 = client.exec_command("sudo docker ps -a | awk '{print $1}' | awk 'length($1) >10'")
        container = stdout2.read().decode('utf8')
        file.write(f"{container}\n")
        file.write("===DISK STATUS===\n")
        stdin3, stdout3, stderr3 = client.exec_command("df -h")
        file.write(f"{stdout3.read().decode('utf8')}\n")
        file.write("===LINKING STATUS===\n")
        #TODO debug piping in docekr inspect
        stdin4, stdout4, stderr4 = client.exec_command(f"sudo docker inspect {container} | head -n 188 | tail -n 12")
        file.write(f"{stdout4.read().decode('utf8')}\n")
        print((f"Done=={nuc_name}=={nuc_ip}"))
    # [x] save output to file
    file.close()

#main()

if __name__ == "__main__":
    main()