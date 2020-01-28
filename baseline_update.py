import sys
import subprocess
import io
import os
import paramiko
import getpass
from paramiko import SSHClient
from scp import SCPClient

REMOTE_HOST='admin@172.30.23.112'
BASELINE_PATH='/home/admin/Server/storage.rpr/www/html/rpr-plugins/'
JOBS_PATH='/home/admin/Server/RPRServers/jenkins_server/data/jobs/'
downloadLocation = os.getcwd()
username="admin"

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
password = getpass.getpass("Password: ")
ssh.connect(hostname="172.30.23.112", username="admin", password=password)

try:
	tool = sys.argv[1]
except:	
	print("Tool:")
	print("1. Maya")
	print("2. Max")
	print("3. Blender 2.80")
	tool = input()
	if(tool=='1'):
		tool = 'Maya'
	elif(tool=='2'):
		tool = 'Max'
	elif(tool=='3'):
		tool = "Blender2.8"
	else:
		sys.exit("Invalid index")


try:
	job = sys.argv[2]
except:	
	stdin, jobs, stderr = ssh.exec_command('ls -1 %s' % JOBS_PATH)
	jobs.channel.recv_exit_status()
	results = jobs.readlines()
	index = 1
	for job in results:
		print(str(index) + ". " + job, end='')
		index += 1
	print("Job:")
	job = results[int(input())-1][:-1]

try:
	build = sys.argv[3]
except:	
	stdin, builds, stderr = ssh.exec_command('ls -1d %s' % JOBS_PATH+job+"/builds/*/")
	builds.channel.recv_exit_status()
	results = builds.readlines()
	index = 1
	for build in results:
		print(str(index) + ". " + build.split('/')[-2])
		index += 1
	print("Build:")
	build = results[int(input())-1][:-1].split('/')[-2]

try:
	gpu = sys.argv[4]
except:	
	stdin, gpu, stderr = ssh.exec_command('ls -1d %s' % JOBS_PATH+job+"/builds/"+build+"/htmlreports/Test_20Report/*/")
	builds.channel.recv_exit_status()
	results = gpu.readlines()
	index = 1
	for gpu in results:
		if(gpu.split('/')[-2][0].isupper()):
			print(str(index) + ". " + gpu.split('/')[-2])
			index += 1
	print("GPU-OS:")
	gpu = results[int(input())-1][:-1].split('/')[-2]

try:
	group = sys.argv[5]
except:	
	stdin, groups, stderr = ssh.exec_command('ls -1d %s' % JOBS_PATH+job+"/builds/"+build+"/htmlreports/Test_20Report/"+gpu+"/Baseline/*/")
	groups.channel.recv_exit_status()
	results = groups.readlines()
	index = 1
	for group in results:
		print(str(index) + ". " + group.split('/')[-2])
		index += 1
	print("Group:")
	group = results[int(input())-1][:-1].split('/')[-2]

try:
	case = sys.argv[6]
except:	
	stdin, cases, stderr = ssh.exec_command('ls -1 %s' % JOBS_PATH+job+"/builds/"+build+"/htmlreports/Test_20Report/"+gpu+"/Baseline/"+group+"/Color/")
	cases.channel.recv_exit_status()
	results = cases.readlines()
	index = 1
	for case in results:
		if(case[0].isupper()):
			print(str(index) + ". " + case, end='')
			index += 1
	print("Case:")
	case = results[int(input())-1][:-1]

scp = SCPClient(ssh.get_transport())
print(downloadLocation+"\\"+case+".jpg",BASELINE_PATH+"RadeonProRender"+tool+"Plugin/ReferenceImages/testFolder/")

scp.get(JOBS_PATH+job+"/builds/"+build+"/htmlreports/Test_20Report/"+gpu+"/Baseline/"+group+"/Color/"+case, downloadLocation)
scp.put(downloadLocation+"\\"+case,BASELINE_PATH+"RadeonProRender"+tool+"Plugin/ReferenceImages/"+gpu+"/"+group+"/Color/")
