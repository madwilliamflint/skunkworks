#!python


# I really like this scheme more than the prior one.  This way I don't have to dick around endlessly with batch files
# AND the test harness actually works pretty well for multiple scripts full of tests

import unittest

from test_foo import *

# test_stuff has a bunch of "live" code in the test script.  Commenting it out for now since it's all been
# migrated elsewhere.  So the tests are old, running against old code.
#from test_stuff import *




if __name__ == '__main__':
    unittest.main()
