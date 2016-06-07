import sys
import os

if sys.version_info[:2] < (2, 7, ):
    try:
        from unittest2 import TestLoader, TextTestRunner
    except ImportError:
        raise ImportError("The ADAL test suite requires the unittest2 "
                          "package to run on Python 2.6 and below.\n"
                          "Please install this package to continue.")
else:
    from unittest import TestLoader, TextTestRunner

if sys.version_info[:2] >= (3, 3, ):
    from unittest import mock
else:
    try:
        import mock

    except ImportError:
        raise ImportError("The ADAL test suite requires the mock "
                          "package to run on Python 3.2 and below.\n"
                          "Please install this package to continue.")


if __name__ == '__main__':

    runner = TextTestRunner(verbosity=2)

    test_dir = os.path.dirname(__file__)
    top_dir = os.path.dirname(os.path.dirname(test_dir))
    test_loader = TestLoader()
    suite = test_loader.discover(test_dir,
                                 pattern="test_*.py",
                                 top_level_dir=top_dir)
    runner.run(suite)
