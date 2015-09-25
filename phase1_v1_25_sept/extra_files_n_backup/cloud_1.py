import libvirt 
import flask
import libvirt
import os


from flask import Flask
'''app = Flask(__name__)

@app.route("/")
def main():
	showSignUp()	
	connect()
	return "Hello World!"

@app.route('/showSignUp')
def showSignUp():
	return "krishna"
	
if __name__ == "__main__":
    app.run()
'''
def connect(ip):
	if ip !="system":
		#st= "qemu+tcp://"+ip+"/system"  
    		st= "qemu:///system"  
    		connection = libvirt.open(st)    		
    	return connection
def listVmNames(connection):
	print "NAMES:\n", connection.listDefinedDomains()
	#return connection.listDefinedDomains()
def listVmIds(connection):
	print "IDs:\n", connection.listDomainsID()
#connection = connect("10.1.132.113")

connection = connect("127.0.0.1")
vm_names = listVmNames(connection)
'''dir_path = "/home/bhanu/academics/third_sem/cloud/mini_project/development/phase1/files/";
file_path = dir_path + "temp.txt"
ff=open(file_path, 'w+')
for lines in vm_names:
	ff.write(lines+"\n")
	ff.write(lines+"\n")
	ff.write(lines+"\n")
ff.close()
ff=open(file_path, 'r')
for line in ff.readlines():
	print line,
os.remove(file_path);
print vm_names'''
listVmIds(connection)
#listVmNames(connection)
virtual_machine = connection.lookupByName('test_ubuntu_12.10')
#virtual_machine.create()
try:
	if virtual_machine.destroy() == 0:
		print "NOOOO"
except:
	print "YESS"

