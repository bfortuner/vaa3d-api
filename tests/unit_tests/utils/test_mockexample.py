import os
import mock
import pytest
from pytest_mock import mocker 
from bigneuron_app.utils import mockexample
from bigneuron_app import config



### Examples with Pytest-Mock ###

def test_pytest_mocker_example__called_with(mocker):
	#https://pypi.python.org/pypi/pytest-mock
	mocker.patch.object(mockexample, 'my_method')
	mockexample.my_wrapper_method()
	mockexample.my_method.assert_called_with(8)

def test_mocker_example__return_value_override(mocker):
	mocker.patch.object(mockexample, 'my_method')
	mockexample.my_method.return_value = 200
	result = mockexample.my_wrapper_method()
	assert result == 200

def test_mocker_example__class_w_autospec__fails_if_method_does_not_exist(mocker):
	mocker.patch.object(mockexample, 'ExampleClass', autospec=True)
	assert mockexample.ExampleClass.this_method_does_exist() is not None
	with pytest.raises(AttributeError):
		mockexample.ExampleClass.this_method_does_not_exist()

def test_mocker_example__class_w_out_autospec__does_not_fail_if_method_does_not_exist(mocker):
	mocker.patch.object(mockexample, 'ExampleClass', autospec=False)
	assert mockexample.ExampleClass.this_method_does_exist() is not None
	mockexample.ExampleClass.this_method_does_not_exist()

def test_mocker_example_pytest_raises_exception(mocker):
	assert mockexample.method_which_doesnt_usually_throw_exception() == 100
	mocker.patch.object(mockexample, 'method_which_doesnt_usually_throw_exception')
	mockexample.method_which_doesnt_usually_throw_exception.side_effect = Exception()
	with pytest.raises(Exception):
		mockexample.method_which_doesnt_usually_throw_exception()


### Pytest Monkeypatch ###

def test_pytest_monkeypatch__update_global_config_variable(monkeypatch):
	#https://pytest.org/latest/monkeypatch.html
	assert mockexample.method_which_uses_global_config_val() == config.WEBSITE_URL
	monkeypatch.setattr(config, 'WEBSITE_URL', 'brendan.com')
	assert mockexample.method_which_uses_global_config_val() == 'brendan.com'

def test_pytest_monkeypatch__set_env_variable(monkeypatch):
	monkeypatch.setenv('VAA3D_CONFIG', 'FakeConfig')
	assert mockexample.method_which_uses_env_variable() == 'FakeConfig'



### Examples with Mock ###

@mock.patch('bigneuron_app.utils.mockexample.my_method', return_value=3)
def test_my_method(get_timeout_mock):
	assert mockexample.my_wrapper_method() == 3


def test_my_method_internal_patch():
	with mock.patch('bigneuron_app.utils.mockexample.my_method', 
		return_value=8) as internal_example:
		assert mockexample.my_wrapper_method() == 8

@mock.patch('bigneuron_app.utils.mockexample.my_method', return_value=3)
@mock.patch('bigneuron_app.utils.mockexample.my_second_helper_method', return_value=3)
def test_my_second_method_w_two_patches(my_method, my_second_mocked_method):
	assert mockexample.my_second_wrapper_method(78) == 6

@mock.patch('bigneuron_app.utils.mockexample.my_second_helper_method', return_value=3)
def test_method_called_with_params(my_second_mock):
	mockexample.method_called_with_params()
	my_second_mock.assert_called_with(5, 5)



### Creating Customer Decorators ###
# slow = pytest.mark.skipif(
#     not pytest.config.getoption("--runslow"),
#     reason="need --runslow option to run"
# )

# @slow
# def test_func_slow():
#     pass


