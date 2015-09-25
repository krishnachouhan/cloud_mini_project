import libvirt
import flask

#global_objects_definition:
instance_types=[
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
'''
instance_types=[
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
'''
app= flask.Flask(__name__)

@app.route('/')
def home():
	return "hello"

@app.route('/welcome')
def welcome():
	return "WELCOME you are on welocme!"

@app.route('/vm/create')
def vmCreate():
	name=request.args['name']
	instance_type=request.args.get('type')
	for i in instance_types:
		print "checking ", i['tid'], " with ", instance_type
		if str(i['tid']) == instance_type:
			print jsonify(i)
			return str(i['ram'])
	return '0'
@app.route('/vm/query')
def vmQuery():
	vmid = request.args['vmid']
	return "HELLO-vmQuery"
@app.route('/vm/destroy')
def vmDestroy():
	vmid = request.args['vmid']
	return "HELLO-vmDestroy"	
















@app.route('/test/test2')
def TASTE():
	u=request.args['u']
    	return u
	#return render_template('test.html')
if __name__ == '__main__':
	app.run(debug=True)
@app.route('/temp1')
def temp1():
	q = flask.request.args.get('q')
	return "q"	
@app.route('/temp1')
def temp1():
	q = flask.request.args.get('q')
	return "q"

	
'''
instance_types=[
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
'''
app= flask.Flask(__name__)
'''
<domain type='kvm' id='2'>
  <name>test_ubuntu_12.10_2</name>
  <uuid>b0c15936-7ffd-fcb1-299f-3da373352b99</uuid>
  <memory unit='KiB'>548576</memory>
function='0x2'/>
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
     </seclabel>
</domain>
'''
