################################################### Connecting to AWS
import boto3

import json
################################################### Create random name for things
import random
import string

################################################### Parameters for Thing
thingArn = ''
thingId = ''
thingName = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(15)])
defaultPolicyName = 'iotPolicy'
###################################################

n=0
def createThing():
  global thingClient
  thingResponse = thingClient.create_thing(
      thingName = thingName + str(n)
  )
  data = json.loads(json.dumps(thingResponse, sort_keys=False, indent=4))

  for element in data: 
    if element == 'thingArn':
        thingArn = data['thingArn']
    elif element == 'thingId':
        thingId = data['thingId']
	
    createCertificate()

def createCertificate():
	global thingClient
	certResponse = thingClient.create_keys_and_certificate(
			setAsActive = True
	)
	data = json.loads(json.dumps(certResponse, sort_keys=False, indent=4))
	for element in data: 
			if element == 'certificateArn':
					certificateArn = data['certificateArn']
			elif element == 'keyPair':
					PublicKey = data['keyPair']['PublicKey']
					PrivateKey = data['keyPair']['PrivateKey']
			elif element == 'certificatePem':
					certificatePem = data['certificatePem']
			elif element == 'certificateId':
					certificateId = data['certificateId']
							
	with open('device'+str(n)+'/'+'device'+str(n)+'_'+'public.key', 'w') as outfile:
			outfile.write(PublicKey)
	with open('device'+str(n)+'/'+'device'+str(n)+'_'+'private.key', 'w') as outfile:
			outfile.write(PrivateKey)
	with open('device'+str(n)+'/'+'device'+str(n)+'_'+'cert.pem', 'w') as outfile:
			outfile.write(certificatePem)

	response = thingClient.attach_policy(
			policyName = defaultPolicyName,
			target = certificateArn
	)
	response = thingClient.attach_thing_principal(
			thingName = thingName,
			principal = certificateArn
	)
	response = thingClient.add_thing_to_group(
            thingGroupName = "iot_thang_groop",
            thingName = thingName + str(n)
    )

thingClient = boto3.client(
    'iot',
    region_name='us-east-2',
    aws_access_key_id='######'
    aws_secret_access_key='#####'

)
createThing()
