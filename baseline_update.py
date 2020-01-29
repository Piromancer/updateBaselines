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
CORE_BASELINE_PATH='/home/admin/Server/storage.rpr/www/html/rpr-core/'
CONVERTERS_BASELINE_PATH='/home/admin/Server/storage.rpr/www/html/rpr-tools/'
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
	print("1. Maya")
	print("2. Max")
	print("3. Blender 2.80")
	print("4. Converters")
	print("5. Core")
	print("6. Viewer")
	print("Tool:", end='')
	tool = input()
	while(int(tool) > 6 or int(tool)<=0):
		print("Invalid index")
		tool = input()
	if(tool=='1'):
		tool = "Maya"
	elif(tool=='2'):
		tool = "Max"
	elif(tool=='3'):
		tool = "Blender2.8"
	elif(tool=='4'):
		tool = "Converters"
	elif(tool=='5'):
		tool = "Core"
	elif(tool=='6'):
		tool = "Viewer"


try:
	job = sys.argv[2]
except:	
	stdin, jobs, stderr = ssh.exec_command('ls -1 %s' % JOBS_PATH)
	jobs.channel.recv_exit_status()
	res_jobs = []
	results = jobs.readlines()
	index = 1
	if(tool == "Converters"):
		for job in results:
			if("ConvertTool" in job):
				print(str(index) + ". " + job, end='')
				res_jobs.append(job)
				index += 1
	elif(tool == "Core"):
		for job in results:
			if("RadeonProRenderCore" in job):
				print(str(index) + ". " + job, end='')
				res_jobs.append(job)
				index += 1
	elif(tool == "Viewer"):
		for job in results:
			if("RadeonProViewer" in job):
				print(str(index) + ". " + job, end='')
				res_jobs.append(job)
				index += 1
	elif(tool == "Maya"):
		for job in results:
			if("RadeonProRenderMaya" in job):
				print(str(index) + ". " + job, end='')
				res_jobs.append(job)
				index += 1
	elif(tool == "Max"):
		for job in results:
			if("RadeonProRenderMax" in job):
				print(str(index) + ". " + job, end='')
				res_jobs.append(job)
				index += 1
	else:
		for job in results:
			if("RadeonProRenderBlender2.8P" in job):
				print(str(index) + ". " + job, end='')
				res_jobs.append(job)
				index += 1

	print("Job:", end='')
	tmp = int(input())
	while (tmp > len(results) or tmp<=0):
		print ("Invalid index\nTry again:", end='')
		tmp = int(input())
	job = res_jobs[tmp-1][:-1]

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
	print("Build:", end='')
	tmp = int(input())
	while (tmp > len(results) or tmp<=0):
		print ("Invalid index\nTry again:", end='')
		tmp = int(input())
	build = results[tmp-1][:-1].split('/')[-2]

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
	print("GPU-OS:", end='')
	tmp = int(input())
	while (tmp > len(results) or tmp<=0):
		print ("Invalid index\nTry again:", end='')
		tmp = int(input())
	gpu = results[tmp-1][:-1].split('/')[-2]

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
	print("Group:", end='')
	tmp = int(input())
	while (tmp > len(results) or tmp<=0):
		print ("Invalid index\nTry again:", end='')
		tmp = int(input())
	group = results[tmp-1][:-1].split('/')[-2]

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
	print("Case:", end='')
	tmp = int(input())
	while (tmp > len(results) or tmp<=0):
		print ("Invalid index\nTry again:", end='')
		tmp = int(input())
	case = results[tmp-1][:-1]

scp = SCPClient(ssh.get_transport())

scp.get(JOBS_PATH+job+"/builds/"+build+"/htmlreports/Test_20Report/"+gpu+"/Baseline/"+group+"/Color/"+case, downloadLocation)
print("View image on " + downloadLocation+"\\"+case)
print("Are you sure you want to replace the baseline? (Y/N)")
tmp = input()
while(tmp.strip() != "Y" and tmp.strip() != "N"):
	print("Please write Y or N")
	tmp = input()
if(tmp == "Y"):
	if(tool == "Converters"):
		if(job.endswith("Manual")):
			job = job[:-6]
		else:
			job = job[:-7]
		scp.put(downloadLocation+"\\"+case,CONVERTERS_BASELINE_PATH+job+"/ReferenceImages/testFolder/")
	elif(tool == "Core"):
		scp.put(downloadLocation+"\\"+case,CORE_BASELINE_PATH+"RadeonProRender"+tool+"/ReferenceImages/testFolder/")
	elif(tool == "Viewer"):
		scp.put(downloadLocation+"\\"+case,CORE_BASELINE_PATH+"RadeonPro"+tool+"/ReferenceImages/testFolder/")
	else:
		scp.put(downloadLocation+"\\"+case,BASELINE_PATH+"RadeonProRender"+tool+"Plugin/ReferenceImages/testFolder/")
else:
	print("Replacement canceled")

print("Removing a picture from your computer...")
os.remove(downloadLocation+"\\"+case)
# scp.put(downloadLocation+"\\"+case,BASELINE_PATH+"RadeonProRender"+tool+"Plugin/ReferenceImages/"+gpu+"/"+group+"/Color/")
