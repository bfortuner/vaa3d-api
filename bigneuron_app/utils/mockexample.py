import os
from bigneuron_app import config

def my_method(num):
	os.remove('filedoesnotexist.txt') #ok since we are mocking!
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

def method_which_uses_global_config_val():
	return config.WEBSITE_URL

def method_which_uses_env_variable():
	return os.getenv('VAA3D_CONFIG')

def method_which_doesnt_usually_throw_exception():
	return 100


class ExampleClass():
	def __init__():
		self.var1 = 5
		seld.var2 = 10

	def this_method_does_exist(self):
		return self.var1

	def get_var2(self):
		return self.var2

	def set_var1(self, val):
		self.var1 = val

	def set_var2(self, val):
		self.var2 = val