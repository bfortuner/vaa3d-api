import pytest
from bigneuron_app.utils.timeout import get_timeout


def test_get_timeout__returns_max_time():
	max_time = 50 #seconds
	min_time = 10 #seconds
	file_bytes = 10
	sec_per_byte = 5
	buffer_multiplier = 2
	time_w_buffer = 10 * 5 * 2 #100 > max_time
	runtime = get_timeout(file_bytes, sec_per_byte, max_time, 
		min_time, buffer_multiplier)
	assert runtime == max_time

def test_get_timeout__returns_min_time():
	max_time = 50 #seconds
	min_time = 20 #seconds
	file_bytes = 100
	sec_per_byte = .05
	buffer_multiplier = 2
	time_w_buffer = 100 * .05 * 2 #10 < min_time
	runtime = get_timeout(file_bytes, sec_per_byte, max_time, 
		min_time, buffer_multiplier)
	assert runtime == min_time

def test_get_timeout__returns_time_w_buffer():
	max_time = 3600 #seconds
	min_time = 1200 #seconds
	file_bytes = 600
	sec_per_byte = 2
	buffer_multiplier = 2
	time_w_buffer = file_bytes * sec_per_byte * buffer_multiplier
	runtime = get_timeout(file_bytes, sec_per_byte, max_time, 
		min_time, buffer_multiplier)
	assert runtime == time_w_buffer
