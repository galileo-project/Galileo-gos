from pyut import eq, it
from pyos import SysOperation

TMP_DIR      = "test_dir"
TMP_FILE     = "test_file"
TEST_CONTENT = "test_content"

def pyut_test_run():
    it(SysOperation.run("ls"))

def pyut_test_mkdir():
    it(SysOperation.mkdir(TMP_DIR))

def pyut_test_rm():
    it(SysOperation.rm(TMP_DIR))

def pyut_test_touch():
    it(SysOperation.touch(TMP_FILE, TEST_CONTENT))

def pyut_test_read():
    content = SysOperation.read(TMP_FILE)
    eq(content, TEST_CONTENT)

def pyut_test_ls():
    it(SysOperation.ls() is not None)
