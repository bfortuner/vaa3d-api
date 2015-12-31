import time
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
	response = table.get_item(
		Key={key_column : key},
		ConsistentRead=True) #waits until prior write operations have completed 
	return response['Item']

def delete(table, key):
	key_column = get_primary_key(table)
	table.delete_item(Key={key_column : key})

def get_primary_key(table):
	return table.key_schema[0]['AttributeName']

def query_all(table, index, name, value, select='ALL_ATTRIBUTES'):
	# boto3.readthedocs.org/en/latest/reference/customizations/dynamodb.html#dynamodb-conditions
	response = table.query(
		IndexName=index,
		KeyConditionExpression=Key(name).eq(value),
		Select=select)
	if select == 'COUNT':
		return response['Count']
	return response['Items']

def scan_all(table, name, value, select='ALL_ATTRIBUTES'):
	response = table.scan(
		FilterExpression=Attr(name).eq(value), 
		ConsistentRead=False,
		Select=select)
	if select == 'COUNT':
		return response['Count']
	return response['Items']

def query_first(table, name, value):
	items = scan_all(table, name, value)
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

def scan_by_time(table, time_field, time_sec, operator):
	if operator == "lt":
		response = table.scan(
			FilterExpression=Attr(time_field).lt(time_sec),
			ConsistentRead=False)
	elif operator == "gt":
		response = table.scan(
			FilterExpression=Attr(time_field).gt(time_sec),
			ConsistentRead=False)
	else:
		response = table.scan(
			FilterExpression=Attr(time_field).eq(time_sec),
			ConsistentRead=False)		
	return response['Items']


def create_table_w_index(conn, table_name, primary_key, key_type,
		index_name, secondary_key, secondary_key_type):
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
	        },
	        {
	            'AttributeName': secondary_key,
	            'AttributeType': secondary_key_type
	        }

	    ],
	    ProvisionedThroughput={
	        'ReadCapacityUnits': DYNAMO_READS_PER_SEC,
	        'WriteCapacityUnits': DYNAMO_WRITES_PER_SEC
	    },
	    GlobalSecondaryIndexes=[
			{
				'IndexName': index_name,
				'KeySchema': [
					{
						'AttributeName': secondary_key,
						'KeyType': 'HASH'
					},
				],
				'Projection': {
					'ProjectionType': 'ALL' #'KEYS_ONLY'
				},
				'ProvisionedThroughput': {
					'ReadCapacityUnits': DYNAMO_READS_PER_SEC,
					'WriteCapacityUnits': DYNAMO_WRITES_PER_SEC
				}
			}
		]
	)
	table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
	return table


