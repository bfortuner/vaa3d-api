from bigneuron_app.utils.command import *

TEST_LOGFILE_PATH="testlogfile.txt"

def test_command():
    c = Command("echo 'Process started'; sleep 2; echo 'Process finished'", shell=True)
    c.run(timeout=3)
    c.run(timeout=1)

    log_f = open(TEST_LOGFILE_PATH,"w")
    c = Command(["echo","'Process started'"], log_f)
    c.run(timeout=3)
    c.run(timeout=1)
    log_f.close()
    os.remove(TEST_LOGFILE_PATH)

