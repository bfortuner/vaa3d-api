import boto3
from boto3.dynamodb.conditions import Key, Attr

from bigneuron_app.clients.constants import AWS_REGION, AWS_ACCESS_KEY, AWS_SECRET_KEY
from bigneuron_app.clients.constants import DYNAMO_READS_PER_SEC, DYNAMO_WRITES_PER_SEC
from bigneuron_app.utils import id_generator


def get_connection():
	return boto3.resource('dynamodb', region_name=AWS_REGION, 
		aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY)

def get_table(conn, table_name):
	return conn.Table(table_name)

def create_table(conn, table_name, primary_key, key_type):
	table = conn.create_table(
	    TableName=table_name,
	    KeySchema=[
	        {
	            'AttributeName': primary_key,
	            'KeyType': 'HASH'
	        }
	    ],
	    AttributeDefinitions=[
	        {
	            'AttributeName': primary_key,
	            'AttributeType': key_type # boto3.readthedocs.org/en/latest/reference/customizations/dynamodb.html
	        }

	    ],
	    ProvisionedThroughput={
	        'ReadCapacityUnits': DYNAMO_READS_PER_SEC,
	        'WriteCapacityUnits': DYNAMO_WRITES_PER_SEC
	    }
	)
	table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
	return table

def insert(table, data_dict):
	table.put_item(Item=data_dict)

def get(table, key):
	key_column = get_primary_key(table)
	response = table.get_item(Key={key_column : key})
	return response['Item']

def delete(table, key):
	key_column = get_primary_key(table)
	table.delete_item(Key={key_column : key})

def get_primary_key(table):
	return table.key_schema[0]['AttributeName']

def query_all(table, name, value):
	# boto3.readthedocs.org/en/latest/reference/customizations/dynamodb.html#dynamodb-conditions
	response = table.scan(FilterExpression=Attr(name).eq(value))
	items = response['Items']
	return items

def query_first(table, name, value):
	items = query_all(table, name, value)
	return items[0]

def drop_table(conn, table_name):
	if table_exists(conn, table_name):
		print "Dropping table: " + table_name
		table = get_table(conn, table_name)
		table.delete()
		table.meta.client.get_waiter('table_not_exists').wait(TableName=table_name)

def table_exists(conn, table_name):
	tables = conn.tables.all()
	for table in tables:
		if table.name == table_name:
			return True
	return False


## Unit Tests ##

def test_all():
	import random
	TABLE_NAME = id_generator.generate_job_item_id()[:10] + "_table"
	conn = get_connection()
	table = create_table(conn, TABLE_NAME, 'job_item_id', 'N')
	table = get_table(conn, TABLE_NAME)
	table.meta.client.get_waiter('table_exists').wait(TableName=TABLE_NAME)
	print dir(table)
	print table.key_schema
	print table.item_count	
	print table.creation_date_time

	record_id = random.randint(1, 1000)
	item1 = { 	
		"job_item_id" : record_id, 
		"job_id" : "9",
		"fourth_param" : "OINoin",
		"third_param" : { 
			"mynested" : "value",
			"nested2" : "value2" 
		}
	}
	insert(table, item1)

	i1 = get(table, record_id)
	print i1['job_item_id'], i1['third_param']

	print get_primary_key(table)
	print query_all(table, "fourth_param", "OINoin")
	print query_first(table, "fourth_param", "OINoin")
	delete(table, record_id)

	print table_exists(conn, TABLE_NAME) == True
	print table_exists(conn, "fake_table") == False

	drop_table(conn, TABLE_NAME)
	drop_table(conn, "fake_table")
