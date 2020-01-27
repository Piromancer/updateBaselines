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
BASELINE_POSTFIX='/htmlreports/Test_20Report/'
downloadLocation = os.getcwd()
username="admin"

try:
	tool = sys.argv[1]
except:	
	print("Tool:")
	tool = input()

try:
	job = sys.argv[2]
except:	
	print("Job:")
	job = input()

try:
	build = sys.argv[3]
except:	
	print("Build:")
	build = input()

try:
	gpu = sys.argv[4]
except:	
	print("[\{GPU\}-\{OS\}]:")
	gpu = input()

try:
	group = sys.argv[5]
except:	
	print("Group:")
	group = input()

try:
	case = sys.argv[6]
except:	
	print("Case:")
	case = input()

ssh = SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
print("Username: ")
username = input()
password = getpass.getpass("Password: ")
ssh.connect(hostname="172.30.23.112", username="admin", password=password)

scp = SCPClient(ssh.get_transport())
print(downloadLocation+"\\"+case+".jpg",BASELINE_PATH+"RadeonProRender"+tool+"Plugin/ReferenceImages/testFolder/")
try:
	scp.get(JOBS_PATH+job+"/builds/"+build+BASELINE_POSTFIX+gpu+"-"+group+"/Baseline/"+group+"/Color/"+case+".jpg", downloadLocation)
except:
	scp.get(JOBS_PATH+job+"/builds/"+build+BASELINE_POSTFIX+gpu+"/Baseline/"+group+"/Color/"+case+".jpg", downloadLocation)
scp.put(downloadLocation+"\\"+case+".jpg",BASELINE_PATH+"RadeonProRender"+tool+"Plugin/ReferenceImages/testFolder/")
