import pytest
from bigneuron_app.utils.timeout import get_timeout


def test_get_timeout__returns_max_time():
	max_time = 50 #seconds
	min_time = 10 #seconds
	file_bytes = 1000
	bytes_per_sec = 5
	buffer_multiplier = 2
	time_w_buffer = file_bytes / bytes_per_sec * buffer_multiplier #400 > max_time
	runtime = get_timeout(file_bytes, bytes_per_sec, max_time, 
		min_time, buffer_multiplier)
	assert runtime == max_time

def test_get_timeout__returns_min_time():
	max_time = 50 #seconds
	min_time = 20 #seconds
	file_bytes = 100
	bytes_per_sec = 20
	buffer_multiplier = 2
	time_w_buffer = file_bytes / bytes_per_sec * buffer_multiplier #10 < min_time
	runtime = get_timeout(file_bytes, bytes_per_sec, max_time, 
		min_time, buffer_multiplier)
	assert runtime == min_time

def test_get_timeout__returns_time_w_buffer():
	max_time = 2000 #seconds
	min_time = 1000 #seconds
	file_bytes = 600
	bytes_per_sec = 1
	buffer_multiplier = 2
	time_w_buffer = file_bytes * bytes_per_sec * buffer_multiplier #1200
	runtime = get_timeout(file_bytes, bytes_per_sec, max_time, 
		min_time, buffer_multiplier)
	assert runtime == time_w_buffer
