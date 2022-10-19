######################################################
# python3.4 send_show_cisco.py 'command' 'device.txt'#
######################################################

import getpass
import sys
import textfsm
import os
from netmiko import ConnectHandler

#delete old files
if os.path.exists('error.txt'):
    os.remove('error.txt')
if os.path.exists('outfile.csv'):
    os.remove('outfile.csv')
if os.path.exists('show_inventory.txt'):
    os.remove('show_inventory.txt')

COMMAND = sys.argv[1]
USER = input('Username: ')
PASSWORD = getpass.getpass()
with open(sys.argv[2], 'r') as sf:
    DEVICES_IP = sf.readlines()

for IP in DEVICES_IP:
    print('Connection to device {}'.format(IP))
    DEVICE_PARAMS = {'device_type': 'cisco_ios',
                     'ip': IP,
                     'username': USER,
                     'password': PASSWORD}
    try:
        with ConnectHandler(**DEVICE_PARAMS) as ssh:
            ssh.enable()
            result = ssh.send_command(COMMAND)
            hostname = ssh.find_prompt()[:-1]
            with open('show_inventory.txt', 'a') as f:
                f.write(hostname + '#\n')
                f.writelines(result)
                f.write('-'*100 + '\n')
    except:
        print('Error in connection to ', IP)
        with open('error.txt', 'a') as ef:
            ef.write(IP)
        continue


input_file = open("show_inventory.txt", encoding='utf-8')
raw_text_data = input_file.read()
input_file.close()


template = open('cisco_show_inv.template')
re_table = textfsm.TextFSM(template)
fsm_results = re_table.ParseText(raw_text_data)
outfile_name = open('outfile.csv', 'w')
outfile = outfile_name
for s in re_table.header:
    outfile.write('%s;' % s)
outfile.write('\n')
for row in fsm_results:
    for s in row:
        outfile.write('%s;' % s)
    outfile.write('\n')
