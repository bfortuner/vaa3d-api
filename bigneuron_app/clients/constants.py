import os

AWS_ACCESS_KEY = os.getenv('VAA3D_AWS_ACCESS_KEY', 'password')
AWS_SECRET_KEY = os.getenv('VAA3D_AWS_SECRET_KEY', 'password')

S3_INPUT_BUCKET='vaa3d-input'
S3_OUTPUT_BUCKET='vaa3d-output'

# Vaa3d Program Directory
# /Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64
# /home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh
VAA3D_PATH=os.getenv('VAA3D_PATH', '/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh')
VAA3D_DEFAULT_PLUGIN='vn2'
VAA3D_DEFAULT_FUNC='app2'

# Test Data
VAA3D_TEST_INPUT_FILE_1='input.tif'
VAA3D_TEST_INPUT_FILE_2='ex_Repo_hb9_eve.tif'

VAA3D_TEST_OUTPUT_FILE_1='input.tif.swc'
VAA3D_TEST_OUTPUT_FILE_2='ex_Repo_hb9_eve.tif.swc'

VAA3D_TEST_INPUT_FILE_PATH_1=os.path.abspath(VAA3D_TEST_INPUT_FILE_1)
VAA3D_TEST_OUTPUT_FILE_PATH_1=os.path.abspath(VAA3D_TEST_OUTPUT_FILE_1)

VAA3D_TEST_JOB = {
	"plugin":VAA3D_DEFAULT_PLUGIN,
	"func":VAA3D_DEFAULT_FUNC,
	"input_filename":VAA3D_TEST_INPUT_FILE_1,
	"output_filename":VAA3D_TEST_OUTPUT_FILE_1,
	"input_file_path":VAA3D_TEST_INPUT_FILE_PATH_1,
	"output_file_path":VAA3D_TEST_OUTPUT_FILE_PATH_1
}