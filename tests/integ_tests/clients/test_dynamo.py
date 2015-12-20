import random
import time
from bigneuron_app.clients.dynamo import *
from bigneuron_app.utils import id_generator

def test_scan_by_time():
	current_time_sec = int(time.time())
	timestr = time.strftime('%m/%d/%Y %H:%M:%S',  time.gmtime(current_time_sec))
	print timestr
	conn = get_connection()
	table = get_table(conn, "test_job_items")
	name = "creation_time"
	items = scan_by_time(table, name, 10005, "gt")
	print items
	items = scan_by_time(table, name, 10005, "lt")
	print len(items) == 0
	items = scan_by_time(table, name, 1449359215, "eq")
	print items

def test_all():
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