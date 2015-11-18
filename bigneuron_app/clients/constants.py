import os
from bigneuron_app import application

AWS_REGION='us-west-2'
AWS_ACCESS_KEY = application.config['AWS_ACCESS_KEY']
AWS_SECRET_KEY = application.config['AWS_SECRET_KEY']

S3_INPUT_BUCKET=application.config['S3_INPUT_BUCKET']
S3_OUTPUT_BUCKET=application.config['S3_OUTPUT_BUCKET']
S3_WORKING_INPUT_BUCKET=application.config['S3_WORKING_INPUT_BUCKET']

AWS_IAM_USER_LOGIN_LINK='https://647215175976.signin.aws.amazon.com/console'

# Vaa3d Program Directory
# /Applications/vaa3d/vaa3d64.app/Contents/MacOS/vaa3d64
# /home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh
VAA3D_PATH=os.getenv('VAA3D_PATH', '/home/ec2-user/Vaa3D_CentOS_64bit_v3.100/start_vaa3d.sh')
VAA3D_DEFAULT_PLUGIN='vn2'
VAA3D_DEFAULT_FUNC='app2'

# Test Data
VAA3D_TEST_INPUT_FILE_1='ex_Repo_hb9_eve.tif'
VAA3D_TEST_INPUT_FILE_2='zipdirtest.zip'
VAA3D_TEST_INPUT_FILE_3='v3draw_zip.zip'

VAA3D_TEST_OUTPUT_FILE_1='ex_Repo_hb9_eve.tif.swc'

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