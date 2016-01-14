import mock
import bigneuron_app.utils.mockexample as mockexample




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

#my_method(3, key='value')
#my_method.assert_called_with(4, key='value')