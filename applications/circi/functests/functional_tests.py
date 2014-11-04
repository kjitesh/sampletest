import unittest
import urllib2
import subprocess
import sys
import os.path
from selenium import webdriver

BASE_URL = 'http://localhost:8000'

class FunctionalTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        #self.web2py = start_web2py_local_server()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(1)

    @classmethod
    def tearDownClass(self):
        self.browser.close()
        #self.web2py.kill()

    def get_response_code(self, url):
        """Returns the response code of given url
        Inputs:
          url: url to check
        output:
          returns the response code of given url
        """
        resp = urllib2.urlopen(url)
        return resp.getcode()

def start_web2py_local_server():
    """prints current directory path, and starts web2py local server"""
    print os.path.curdir
    return subprocess.Popen(['python','~/web2py/web2py.py','run','-a "123"'])

def run_functional_tests(pattern=None):
    print 'running tests'
    if pattern is None:
        tests = unittest.defaultTestLoader.discover('.')
    else:
        pattern_with_globs = '*%s*' % (pattern,)
        tests = unittest.defaultTestLoader.discover('.', pattern=pattern_with_globs)
    runner = unittest.TextTestRunner()
    runner.run(tests)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_functional_tests()
    else:
        run_functional_tests(pattern=sys.argv[1])
