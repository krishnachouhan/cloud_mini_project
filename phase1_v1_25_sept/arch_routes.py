from flask import request, render_template, url_for, jsonify
#global_objects_definition:
dir_path = "/home/bhanu/academics/third_sem/cloud/mini_project/development/phase1/files/";
xml_string1
instance_types
######################################################################	
def listVmNames(connection):
	return connection.listDefinedDomains()
def listVmIds(connection):
	print connection.listDomainsID()
def connect(ip):
def xml_string(a, b, c)
def vmidExists(vmid):
	temp_path = dir_path + "vmids.txt"
def add_vmid(vmid):
	f = open(dir_path+"vmids.txt")
def nameFromVmid(vmid):
def pmidFromVmid(vmid):
def instanceFromVmid(vmid):
def unique_elem(pm_list):	
	sort(pm_list)
def populate_pm_data():
	f1 = open(dir_path+"ip_pmid.txt")
	f2 = open(dir_path+"temp.txt", 'a')
def assign_pmid():
	f0 = open(dir_path + "pmids.txt")
	pmid = f0.readline()
	f1 = open(dir_path + "ip_list.txt")
	f2 = open(dir_path + "ip_pmid.txt", 'a')
######################################################################
assign_pmid() #do not add duplicate ips
populate_pm_data()
######################################################################	
app= flask.Flask(__name__)
@app.route('/')
def home():
@app.route('/welcome')
def welcome():
####################################################################
@app.route('/vm/create')
def vmCreate():
@app.route('/vm/query')
def vmQuery():
@app.route('/vm/destroy')
def vmDestroy():
@app.route('/vm/types')
def vmTypes():
####################################################################
@app.route('/pm/list')
def pmList():
@app.route('/pm/pmid/listvms')
def vmList():
@app.route('/pm/pmid/listvms')
######################################################################
if __name__ == '__main__':
######################################################################
	
	
#DOCUMENTATION:
#ALGORITHMS:
####################################################################
# VM APIs:
#1> VM_Creation:
#	URL:http://server/vm/create?name=test_vm&instance_type=type 
#	Args: 	Name, Instance_type
#	Return:	vmid or '0' if failed
####################################################################
#2> VM_Query 
#	Argument: vmid 
#	Return: instance_type, name, id, pmid 
#	URL:http://server/vm/query?vmid=vmid 
####################################################################
#3>VM_Destroy 
#	Argument: vmid 
#	Return: 1 for success and 0 for failure. 	
#	url: http://server/vm/destroy?vmid=vmid
#ALGO:
	#check if given id exists:
		#YES, exists
			#check if given id is running:
				#yes, running: 
					#Stop it:
						#yes, return 1
						#no, return 0
				#no,  not running:
					#return 1
		#NO, doesn't exists
			#return 0;
####################################################################
#4>VM_Type 	*check the output once as "resultzz" is appearing
#	Argument: NA 
#	Return: tid, cpu, ram, disk 
#	URL: http://server/vm/types 
####################################################################
####################################################################
####################################################################
# PM APIs:
#1> List_PM:
#	Argument: NA 
#	Return: pmids 
#		{
#			"pmids":[1,2,3]
#		} 
#	URL: http://server/pm/list
####################################################################
#2>List_VMs 
#	Argument: pmid 
#	Return: vmids 
#	{
#		"vmids":[38201, 38203, 38205]
#	}
#	URL: http://server/pm/pmid/listvms 
#3>PM_Query 
#	Argument: pmid 
#	Return: pmid, capacity, free, no. of VMs running(0 if invalid pmid or otherwise) 
#		{ 
#			“pmid”: 1, 
#			“capacity”:
#				{ 
#					“cpu”: 4, 
#					“ram”: 4096, 
#					“disk”: 160 
#				}, 
#			“free”:
#				{ 
#					“cpu”: 2, 
#					“ram”: 2048, 
#					“disk”: 157 	
#				}, 
#			“vms”: 1 
#		} 
#	URL:http://server/pm/query?pmid​=id 

#ALGO:
#	this_pmid = input
#	check if this_pmid exists in all_pmids:
#		YES:
#			this_vmid = count pmid_vmid occurences for this_pmid
			


'''



