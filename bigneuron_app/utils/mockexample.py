
def my_method(num):
	return 5

def my_wrapper_method():
	result = my_method(8)
	return result

def my_second_helper_method(num1, num2):
	return 10

def my_second_wrapper_method(num):
	return my_second_helper_method(num, 5) + my_method(num)

def method_called_with_params():
	return my_second_helper_method(5, 5)
