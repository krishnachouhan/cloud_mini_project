import libvirt
import os
import flask
from flask import request, render_template, url_for, jsonify
import sys



#global_objects_definition:
dir_path = "/home/bhanu/academics/third_sem/cloud/mini_project/development/phase1/files/";
#pm_path=str(sys.argv[0])
#image_path=str(sys.argv[1])
#flavour_path=str(sys.argv[2])

pm_path=str(dir_path)
image_path=str(dir_path+"im_list.txt")
flavour_path=str(dir_path+"flavour_list.txt")

######################################################################	
xml_string1="""
	<domain type='kvm' id=''>
	  <name>"""
xml_string3="""</name>
	  <uuid></uuid>
	  <memory unit='KiB'>"""
xml_string4="""</memory>
	  <currentMemory unit='KiB'>"""
xml_string5="""</currentMemory>
	  <vcpu placement='static'>"""
xml_string6="""</vcpu>
	  <resource>
	    <partition>/machine</partition>
	  </resource>
	  <os>
	    <type arch='x86_64' machine='pc-i440fx-trusty'>hvm</type>
	    <boot dev='hd'/>
	  </os>
	  <features>
	    <acpi/>
	    <apic/>
	    <pae/>
	  </features>
	  <clock offset='utc'/>
	  <on_poweroff>destroy</on_poweroff>
	  <on_reboot>restart</on_reboot>
	  <on_crash>restart</on_crash>
	  <devices>
	    <emulator>/usr/bin/kvm-spice</emulator>
	    <disk type='file' device='disk'>
	      <driver name='qemu' type='raw'/>
	      <source file='/var/lib/libvirt/images/"""
xml_string7="""/>
	      <target dev='vda' bus='virtio'/>
	      <alias name='virtio-disk0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
	    </disk>
	    <disk type='block' device='cdrom'>
	      <driver name='qemu' type='raw'/>
	      <target dev='hdc' bus='ide'/>
	      <readonly/>
	      <alias name='ide0-1-0'/>
	      <address type='drive' controller='0' bus='1' target='0' unit='0'/>
	    </disk>
	    <controller type='usb' index='0'>
	      <alias name='usb0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>
	    </controller>
	    <controller type='pci' index='0' model='pci-root'>
	      <alias name='pci.0'/>
	    </controller>
	    <controller type='ide' index='0'>
	      <alias name='ide0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
	    </controller>
	    <interface type='network'>
	      <mac address='52:54:00:ae:dc:f4'/>
	      <source network='default'/>
	      <target dev='vnet0'/>
	      <model type='virtio'/>
	      <alias name='net0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
	    </interface>
	    <serial type='pty'>
	      <source path='/dev/pts/5'/>
	      <target port='0'/>
	      <alias name='serial0'/>
	    </serial>
	    <console type='pty' tty='/dev/pts/5'>
	      <source path='/dev/pts/5'/>
	      <target type='serial' port='0'/>
	      <alias name='serial0'/>
	    </console>
	    <input type='mouse' bus='ps2'/>
	    <input type='keyboard' bus='ps2'/>
	    <graphics type='vnc' port='5900' autoport='yes' listen='127.0.0.1'>
	      <listen type='address' address='127.0.0.1'/>
	    </graphics>
	    <sound model='ich6'>
	      <alias name='sound0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
	    </sound>
	    <video>
	      <model type='cirrus' vram='9216' heads='1'/>
	      <alias name='video0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
	    </video>
	    <memballoon model='virtio'>
	      <alias name='balloon0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
	    </memballoon>
	  </devices>
	  <seclabel type='dynamic' model='apparmor' relabel='yes'>
	    <label>libvirt-b0c15936-7ffd-fcb1-299f-3da373352b98</label>
	    <imagelabel>libvirt-b0c15936-7ffd-fcb1-299f-3da373352b98</imagelabel>
	  </seclabel>
	</domain>
	"""

instance_types=[]
image_dictionary={}
######################################################################
#method_definitions
def listVmNames(connection):
	return connection.listDefinedDomains()
######################################################################
def listVmIds(connection):
	print connection.listDomainsID()
######################################################################
def connect(ip):
	if ip !="system":
		st= "qemu+tcp://"+ip+"/system"  
    	else:
    		st= "qemu:///system"  
    	connection = libvirt.open(st)    		
    	return connection
######################################################################
def vmidExists(vmid):
	temp_path = dir_path + "all_vmid.txt"
	ff=open(temp_path, 'r')
	for line in ff:
		if (vmid == line.split('\n')[0]):
			return True
	return False;
######################################################################
def add_vmid(vmid):
	id_array=[]
	f = open(dir_path+"all_vmid.txt")
	for i in f:
		id_array.append(i)
	f.close()
	if vmid in id_array:
		return 0
	else:
		id_array.append(vmid)
		for i in id_array:
			f2 = open(dir_path + "all_vmid.txt", 'w+')
			f2.write(i)
		f2.close()
		return 1
######################################################################
def get_node_info(ip):
	temp_str =""
	con = connect(ip)
	node_info = con.getInfo()
	if len(node_info)>3 :
		temp_str = str(node_info[1])+":"
		temp_str += str(node_info[2])+":"
		#temp_str += line.split(':')[1]
	return temp_str
######################################################################
def get_xml(new_name, new_ram, new_cpu):
	xml_string = xml_string1
	#xml_string += new_id;
	#xml_string += xml_string2
	xml_string += str(new_name)
	xml_string += xml_string3
	xml_string += str(new_ram)
	xml_string += xml_string4
	xml_string += str(new_ram)
	xml_string += xml_string5
	xml_string += str(new_cpu)
	xml_string += xml_string6
	xml_string += str(image_dictionary[image_id])
	xml_string += xml_string7
	return xml_string
######################################################################
def isVmNameExists(new_name):
	f = open(dir_path + "name_vmid.txt")
	for i in f:
		if str(new_name) == str(i.split(':')[0]):
			return True
	f.close()
	return False
######################################################################
def findPossiblePm(new_ram, new_cpu):
	ram = int (new_ram)
	cpu = int (new_cpu)
	f = open( dir_path + "temp.txt")
	for i in f:
		if int (i.split(':')[0])>ram and int(i.split(':')[1])>cpu:
			ret = i.split(':')[2].split('\n')[0]
			f.close()
			return ret
	f.close()
	return '0'
######################################################################
def ipFromPmid(pmid):
	f = open(dir_path + "ip_pmid.txt")
	for i in f:
		if str(pmid) == str(i.split(':')[1].split('\n')[0]):
			ret = i.split(':')[0]
			f.close()
			return ret
	else:
		return '0';
######################################################################
def nameFromVmid(vmid):
	temp_path = dir_path + "name_vmid.txt"
	ff=open(temp_path, 'r')
	for line in ff:
		print "name:", vmid
		print "line.split(':')[0].split('\n')[0]:", line.split(':')[0].split('\n')[0] 
		if (vmid == line.split(':')[1].split('\n')[0]):
			return (line.split(':')[0]).split('\n')[0]
	return "NONEnameFromVmid";
######################################################################
def vmidFromName(name):
	temp_path = dir_path + "name_vmid.txt"
	ff=open(temp_path, 'r')
	for line in ff:

		if (name == line.split(':')[0].split('\n')[0]):
			return (line.split(':')[1]).split('\n')[0]
	return "NONEvmidFromName";
######################################################################
def pmidFromVmid(vmid):
	temp_path = dir_path + "pmid_vmid.txt"
	ff=open(temp_path, 'r')
	for line in ff:
		if (vmid == line.split(':')[0]):
			return line.split(':')[1].split('\n')[0]
	return "NONEpmidFromVmid";
######################################################################
def instanceFromVmid(vmid):
	temp_path = dir_path + "instance_vmid.txt"
	ff=open(temp_path, 'r')
	for line in ff:
		if (str(vmid) == str(line.split(':')[1].split('\n')[0])):
			return str(line.split(':')[0])
	return "NONEinstanceFromVmid";
######################################################################
def removeVmidFromAllVmid(vmid):
	lis=[]
	f = open(dir_path + "all_vmid.txt")
	for i in f:
		if str(i) != str(vmid):
			lis.append(i)
	f.close()
	f1 = open(dir_path + "all_vmid.txt", 'w+')
	for i in lis:
		f1.write(i)
	f1.close()
######################################################################
def removeVmidFromNameVmid(vmid):
	lis=[]
	f = open(dir_path + "name_vmid.txt")
	for i in f:
		if str(i.split(':')[1].split('\n')[0]) != str(vmid):
			lis.append(i)
	f.close()
	f1 = open(dir_path + "name_vmid.txt", 'w+')
	for i in lis:
		f1.write(i)
	f1.close()
######################################################################
def removeVmidFromPmidVmid(vmid):
	lis=[]
	f = open(dir_path + "pmid_vmid.txt")
	for i in f:
		if str(i.split(':')[1].split('\n')[0]) != str(vmid):
			lis.append(i)
	f.close()
	f1 = open(dir_path + "pmid_vmid.txt", 'w+')
	for i in lis:
		f1.write(i)
	f1.close()
######################################################################
def removeVmidFromInstanceVmid(vmid):
	lis=[]
	f = open(dir_path + "instance_vmid.txt")
	for i in f:
		if str(i.split(':')[1].split('\n')[0]) != str(vmid):
			lis.append(i)
	f.close()
	f1 = open(dir_path + "instance_vmid.txt", 'w+')
	for i in lis:
		f1.write(i)
	f1.close()
######################################################################
def updateInfoOnTemp(vmid):
	lis=[]
	f = open(dir_path + "temp.txt")
	for i in f:
		if str(i.split(':')[2].split('\n')[0]) != str(vmid):
			lis.append(i)
		else:
			a = int(instanceFromVmid(vmid))
			cpu = int(instance_types[a-1]['cpu'])+int(i.split(':')[1])
			ram = int(instance_types[a-1]['ram'])+int(i.split(':')[0])
			temp_str = str(ram)+':'+str(cpu)+':'+str(vmid)
			lis.append()
	f.close()
	f1 = open(dir_path + "text.txt", 'w+')
	for i in lis:
		f1.write(i)
	f1.close()
######################################################################
def unique_elem(pm_list):	
	sort(pm_list)
	ans=[]
	for i in range(len(pm_list)):
		if pm_list[i] == pm_list[i+1]:
			i+=1
		else:
			ans.append(pm_list[i])
			i+=1
	print ans
######################################################################
def populate_pm_data():
	list_pmid=[]
	f1 = open(dir_path+"temp.txt")
	for i in f1:
		list_pmid.append(str(i.split(':')[2].split('\n')[0]))
	f1.close()
	
	f2 = open(dir_path+"ip_pmid.txt")
	f3 = open(dir_path+"temp.txt", 'a')
	for line in f2:	
		if str(line.split(':')[1].split('\n')[0]) not in list_pmid:
			connection_ip = line.split(':')[0]
			#connection_link="qemu://"+connection_ip
			connection = libvirt.open("qemu:///system")
			node_info = connection.getInfo()
			#print node_info
			if len(node_info)>3 :
				temp_str = str(node_info[1])+":"
				temp_str += str(node_info[2])+":"
				temp_str += line.split(':')[1]
				f3.write(temp_str)
	f3.close()
	f2.close()
######################################################################
def assign_pmid():
	f0 = open(dir_path + "pmid.txt")
	pmid = int(f0.readline().split('\n')[0])
	f0.close()
	pmid = pmid
	lis=[]
	ip_list=[]
	f2 = open(dir_path + "ip_pmid.txt")
	for i in f2:
		lis.append(i)
		ip_list.append(str(i.split(':')[0]))
	f2.close()

	f4 = open(dir_path + "ip_pmid.txt", 'a')

	f1 = open(dir_path + "ip_list.txt")
	for ip in f1:
		if str(ip.split('\n')[0]) not in ip_list:
			print "IP:"+ip+"ip_list:",ip_list 
			temp_pmid=int(pmid)+1
			pmid=str(temp_pmid)
			temp=ip.split('\n')[0]+":"+pmid+"\n"
			f4.write(temp)
			print "writing : "+temp
	f1.close()
	f3 = open(dir_path + "pmid.txt", 'w+')
	f3.write(str(pmid))
	f3.close()
######################################################################
def populate_instance_file():
	count = 1
	dictn={}
	img_name=""
	img_id=""
	f = open(flavour_path)
	for i in f:
		if '{' in i:
			dictn.clear()
			dictn['tid']=str(count)
			count+1
		elif '}' in i:
			instance_types.append(dictn)
		elif ':' in i:
			dictn[str(i.split(':')[0].split('"')[1]).strip()]=str(i.split(':')[1].split('\n')[0].strip().split(',')[0])
	f.close()
	f1 = open(dir_path+"instance_list.txt", 'w+')
	for dictn in instance_types:
		for i in dictn:
			f1.write( str(i)+":"+dictn[i]+'\n')
	f1.close()
######################################################################
def populate_image_dictionary():
	f = open(dir_path+"image_list.txt")
	for i in f:
		image_dictionary[ i.split(':')[0] ] = i.split(':')[1].split('\n')[0]
	f.close()
######################################################################	
def populate_image_file():
	count = 1
	image_name=[]
	image_id=[]
	dictn={}
	img_name=""
	img_id=""
	f = open(image_path)
	for i in f:
		image_name=i.split('/')
		img_name=image_name[len(image_name)-1]
		img_name=img_name.split('\n')[0]
		img_id=count
		count = count + 1
		dictn[img_id] = img_name
	f.close()
	f1 = open(dir_path+"image_list.txt", 'w+')
	for i in dictn:
		f1.write( str(i)+":"+dictn[i]+'\n')
	f1.close()
######################################################################
assign_pmid()
populate_pm_data()
populate_instance_file()
#populate_instance_variable()
populate_image_file()
populate_image_dictionary()

######################################################################
	
app= flask.Flask(__name__)

@app.route('/')
def home():
    	return "\t\t\t\tCLOUD COMPUTING\n\t\t Mini Project Phase One"

@app.route('/welcome')
def welcome():
	return "WELCOME you are on welocme!"
####################################################################
@app.route('/vm/create')
def vmCreate():
	new_name=request.args['name']
	instance_type=request.args.get('instance_type')
	image_id = request.args.get('image_id')
	if isVmNameExists(new_name):
		ip1 = ipFromPmid(str(pmidFromVmid(str(vmidFromName(str(new_name))))))
		con = connect(ip1)
		vm = con.lookupByName(new_name)
		vm.create()
		print "vm exists and started" 
		return '1'
	else:
		f1 = open(dir_path + "vmid.txt", 'r')
		new_id = f1.readline().split('\n')[0]
		new_id = int(new_id) + 1
		f1.close()
		for i in instance_types:
			print "checking ", i['tid'], " with ", instance_type
			if str(i['tid']) == instance_type:
				new_ram = i['ram']
				new_cpu = i['cpu']

				xml_string=get_xml(str(new_name),str(new_ram),str(new_cpu),str(image_id))
				pmid=""
				ip=""
				pmid = findPossiblePm(new_ram, new_cpu)
				if str(pmid) == '0':
					print "no pmid returned. Possible no resources available"
					return "-1"
				else:
					ip = ipFromPmid(pmid)
				con = connect(ip)
				con.defineXML(xml_string)
				vm = con.lookupByName(new_name)
				vm.create()
			
				sys_info=[]
				f2 = open(dir_path + "temp.txt")
				for i in f2:
					sys_info.append(i)
				f2.close()
				for i in range(len(sys_info)):
					sys_ram = int(sys_info[i].split(':')[0])
					sys_cpu = int(sys_info[i].split(':')[1])
					sys_id  = int(sys_info[i].split(':')[2].split('\n')[0])
					if( sys_ram > int(new_ram) and sys_cpu > int(new_cpu) ):
						sys_ram = int(sys_ram) - int(new_ram)
						sys_cpu = int(sys_cpu) - int(new_cpu)
						sys_info[i] = str(sys_ram)+":"+str(sys_cpu)+":"+str(sys_id)+'\n'
					
						f3 = open(dir_path + "pmid_vmid.txt", 'a')
						f3.write(str(sys_id)+":"+str(new_id)+'\n')
						f3.close()
					
						f4 = open(dir_path + "name_vmid.txt", 'a')
						f4.write(str(new_name)+":"+str(new_id)+'\n')
						f4.close()

						break
				print "322"
				f2 = open(dir_path + "temp.txt", 'w+')
				for i in sys_info:
					f2.write(i)
				f2.close()
				print len(sys_info)
				f5 = open(dir_path + "all_vmid.txt", 'a')
				f5.write(str(new_id))
				f5.close()
				f6 = open(dir_path + "instance_vmid.txt" + 'a')
				f6.write(str(instance_type)+":"+str(new_id))
				f6.close()
				f1 = open(dir_path + "vmid.txt", 'w+')
				f1.write(str(new_id))
				f1.close()
				return str(new_id) 

	
	#print jsonify(i)
	return "0"

@app.route('/vm/query')
def vmQuery():
	vmid = request.args['vmid']
	if vmidExists(str(vmid)) :
		ans=[{'vmid':'0', 'name':'0', 'instance_type':'0', 'pmid':'0'}]
		ans[0]['vmid'] 			=vmid
		ans[0]['name'] 			=nameFromVmid(vmid)
		ans[0]['instance_type'] 	=instanceFromVmid(vmid)
		ans[0]['pmid'] 			=pmidFromVmid(vmid)
		return flask.jsonify(ans[0]) 
	else:
		return '0'
####################################################################
@app.route('/vm/destroy')
def vmDestroy():
	vmid = request.args['vmid']
	if vmidExists(str(vmid)) :
		pmid 			= pmidFromVmid(vmid)
		vm_name 		= nameFromVmid(vmid)
		ip 			= ipFromPmid(pmid)
		connection 		= connect(ip)
		virtual_machine 	= connection.lookupByName(str(vm_name))
	 
		if virtual_machine.destroy() == 0:
			removeVmidFromAllVmid	(str(vmid))
			removeVmidFromNameVmid	(str(vmid))
			removeVmidFromPmidVmid	(str(vmid))
			removeVmidFromInstanceVmid(str(vmid))
			updateInfoOnTemp	(str(vmid))
			virtual_machine.undefine()
			return 'Destroyed and Undefined'
		else:
			return 'not okay'
	else:
	 	print "wrong id given; id not in file; false on vmidExists(vmid)"
	 	return 'not okay'
	return "create over"
####################################################################
@app.route('/vm/types')
def vmTypes():
	dictn={}
	count=1;
	for i in instance_types:
		dictn["Instance "+str(count)+""]=i
		count+=1
	return jsonify(dictn)
####################################################################
@app.route('/pm/list')
def pmList():
	pm_list=[]
	temp_path=dir_path+"ip_pmid.txt"
	f = open(temp_path)
	for i in f:
		pm_list.append(i.split(':')[1].split('\n')[0])
	print pm_list
	dictn={}
	for i in range(len(pm_list)):
		dictn[str(i+1)] = str(pm_list[i])
	return jsonify(dictn)
####################################################################
@app.route('/pm/pmid/listvms')
def vmList():
	pmid = request.args['pmid']
	pm_list = []
	vm_list=[]
	temp_path=dir_path+"pmid_vmid.txt"
	f = open(temp_path)
	for i in f:
		if pmid == i.split(':')[0]:
			vm_list.append(i.split(':')[1].split('\n')[0])
	#print vm_list
	dictn={}
	for i in vm_list:
		dictn["vmid="+str(i)]="pmid="+str(pmid)
	return jsonify(dictn)
####################################################################
@app.route('/pm/query')
def pmQuery():
	this_pmid = request.args['pmid']
	pmid_array=[]
	capacity_str=""
	capacity=[]
	free=[]
	count=0
	f0 = open(dir_path+"all_pmids.txt")
	for i in f0:
		pmid_array.append(str(i.split('\n')[0]))
	f0.close()
	print "pmid_array", pmid_array[0], "hello"
	if str(this_pmid) in pmid_array:
		print "440"
		f1 = open(dir_path+"pmid_vmid.txt")
		for i in f1:
			if this_pmid == i.split(':')[0]:
				count += 1
		f1.close()
		f2 = open(dir_path+"ip_pmid.txt")
		for i in f2:
			print this_pmid, i.split(':')[1].split('\n')[0]
			if this_pmid == i.split(':')[1].split('\n')[0]:
				ip = i.split(':')[0]
		f2.close()
		capacity_str = get_node_info(ip)
		capacity.append(capacity_str.split(':')[0])
		capacity.append(capacity_str.split(':')[1])
		#capacity.append(capacity_str.split(':')[2])
		f3 = open(dir_path+"temp.txt")
		for i in f3:
			if this_pmid == i.split(':')[2].split('\n')[0]:
				free.append(i.split(':')[0])
				free.append(i.split(':')[1])
				free.append(i.split(':')[2].split('\n')[0])
		
		print this_pmid, capacity, free, count
		dictn={}
		capacity_dictn={}
		capacity_dictn['RAM']=capacity[0]
		capacity_dictn['CPU']=capacity[1]
		free_dictn={}
		free_dictn['RAM']=free[0]
		free_dictn['CPU']=free[1]
		dictn['PMID']=str(this_pmid)
		dictn['CAPACITY']=capacity_dictn
		dictn['FREE']=free_dictn
		dictn['VMs']=str(count)
		return jsonify(dictn)
	
	return '0'		
	
@app.route('/image/list') 
def imageList():
	return jsonify(image_dictionary)

if __name__ == '__main__':
	app.run(debug=True)
	



print "\t\t\t\t LINE 371"
print "\n\nI am the last lnine\n\n checking for id.txt updation at last of the program" 	
	
#DOCUMENTATION:
'''
#VARIABLES:
	Instance types used:
	[
		{ 
		    "tid": 1, 
		    "cpu": 1, 
		    "ram": 512, 
		    "disk": 1 
		}, 
		{ 
		    "tid": 2, 
		    "cpu": 2, 
		    "ram": 1024, 
		    "disk": 2 
		}, 
		{ 
		    "tid": 3, 
		    "cpu": 4, 
		    "ram": 2048, 
		    "disk": 3 
		} 
	]

	xml_string="""
	<domain type='kvm' id='2'>
	  <name>test_ubuntu_12.10_2</name>
	  <uuid>b0c15936-7ffd-fcb1-299f-3da373352b99</uuid>
	  <memory unit='KiB'>548576</memory>
	  <currentMemory unit='KiB'>548576</currentMemory>
	  <vcpu placement='static'>1</vcpu>
	  <resource>
	    <partition>/machine</partition>
	  </resource>
	  <os>
	    <type arch='x86_64' machine='pc-i440fx-trusty'>hvm</type>
	    <boot dev='hd'/>
	  </os>
	  <features>
	    <acpi/>
	    <apic/>
	    <pae/>
	  </features>
	  <clock offset='utc'/>
	  <on_poweroff>destroy</on_poweroff>
	  <on_reboot>restart</on_reboot>
	  <on_crash>restart</on_crash>
	  <devices>
	    <emulator>/usr/bin/kvm-spice</emulator>
	    <disk type='file' device='disk'>
	      <driver name='qemu' type='raw'/>
	      <source file='/var/lib/libvirt/images/test_ubuntu_12.10.img'/>
	      <target dev='vda' bus='virtio'/>
	      <alias name='virtio-disk0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
	    </disk>
	    <disk type='block' device='cdrom'>
	      <driver name='qemu' type='raw'/>
	      <target dev='hdc' bus='ide'/>
	      <readonly/>
	      <alias name='ide0-1-0'/>
	      <address type='drive' controller='0' bus='1' target='0' unit='0'/>
	    </disk>
	    <controller type='usb' index='0'>
	      <alias name='usb0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x2'/>
	    </controller>
	    <controller type='pci' index='0' model='pci-root'>
	      <alias name='pci.0'/>
	    </controller>
	    <controller type='ide' index='0'>
	      <alias name='ide0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x01' function='0x1'/>
	    </controller>
	    <interface type='network'>
	      <mac address='52:54:00:ae:dc:f4'/>
	      <source network='default'/>
	      <target dev='vnet0'/>
	      <model type='virtio'/>
	      <alias name='net0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
	    </interface>
	    <serial type='pty'>
	      <source path='/dev/pts/5'/>
	      <target port='0'/>
	      <alias name='serial0'/>
	    </serial>
	    <console type='pty' tty='/dev/pts/5'>
	      <source path='/dev/pts/5'/>
	      <target type='serial' port='0'/>
	      <alias name='serial0'/>
	    </console>
	    <input type='mouse' bus='ps2'/>
	    <input type='keyboard' bus='ps2'/>
	    <graphics type='vnc' port='5900' autoport='yes' listen='127.0.0.1'>
	      <listen type='address' address='127.0.0.1'/>
	    </graphics>
	    <sound model='ich6'>
	      <alias name='sound0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x04' function='0x0'/>
	    </sound>
	    <video>
	      <model type='cirrus' vram='9216' heads='1'/>
	      <alias name='video0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x02' function='0x0'/>
	    </video>
	    <memballoon model='virtio'>
	      <alias name='balloon0'/>
	      <address type='pci' domain='0x0000' bus='0x00' slot='0x06' function='0x0'/>
	    </memballoon>
	  </devices>
	  <seclabel type='dynamic' model='apparmor' relabel='yes'>
	    <label>libvirt-b0c15936-7ffd-fcb1-299f-3da373352b98</label>
	    <imagelabel>libvirt-b0c15936-7ffd-fcb1-299f-3da373352b98</imagelabel>
	  </seclabel>
	</domain>
	"""


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
#			pmid: 1
#			capacity:
#				{ 
#					cpu: 4, 
#					ram: 4096, 
#					disk: 160 
#				}, 
#			free:
#				{ 
#					cpu: 2, 
#					ram: 2048, 
#					disk: 157 	
#				}, 
#			vms: 1 
#		} 
#	URL: http://server/pm/query?pmid=id

#ALGO:
	this_pmid = input
	check if this_pmid exists in all_pmids:
		YES:
			cpunts = count pmid_vmid occurences for this_pmid
			CAPACITY:	extract node info from pmid
			FREE:		print info from temp.txt for given this_pmid
			return above information.
		NO:	
			return 0
			



























'''



