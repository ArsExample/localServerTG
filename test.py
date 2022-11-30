import subprocess

command = 'path'
ipconfig_res = subprocess.Popen('ipconfig', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in ipconfig_res.stdout.readlines():
    line = line.strip()
    if line:
        print(line.decode('cp866'))


process = subprocess.Popen(command, universal_newlines=True, shell=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)