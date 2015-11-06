import os

AWS_ACCESS_KEY = os.getenv('VAA3D_AWS_ACCESS_KEY', 'password')
AWS_SECRET_KEY = os.getenv('VAA3D_AWS_SECRET_KEY', 'password')

S3_INPUT_BUCKET='vaa3d-input'
S3_OUTPUT_BUCKET='vaa3d-output'

TEST_INPUT_FILENAME='input.tif'
TEST_OUTPUT_FILENAME='output.swc'
TEST_INPUT_FILE_PATH=os.path.abspath(TEST_INPUT_FILENAME)
TEST_OUTPUT_FILE_PATH=os.path.abspath(TEST_OUTPUT_FILENAME)

# Vaa3d Program Directory
# /Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64
# /home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh
VAA3D_PATH=os.getenv('VAA3D_PATH', '/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh')
VAA3D_PLUGIN='vn2'
VAA3D_PLUGIN_FUNC='app2'

VAA3D_TEST_JOB = {
	"plugin":VAA3D_PLUGIN,
	"func":VAA3D_PLUGIN_FUNC,
	"input_filename":TEST_INPUT_FILENAME,
	"output_filename":TEST_OUTPUT_FILENAME,
	"input_file_path":TEST_INPUT_FILE_PATH,
	"output_file_path":TEST_OUTPUT_FILE_PATH
}