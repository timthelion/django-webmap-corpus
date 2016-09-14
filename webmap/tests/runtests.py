#!/usr/bin/env python
"""
This script is a trick to setup a fake Django environment, since this reusable
app will be developed and tested outside any specifiv Django project.

Via ``settings.configure`` you will be able to set all necessary settings
for your app and run the tests as if you were calling ``./manage.py test``.

"""
import sys
import warnings

from django.conf import settings

import test_settings


if not settings.configured:
    settings.configure(**test_settings.__dict__)

from django_nose import NoseTestSuiteRunner

def runtests(*test_args):
    warnings.simplefilter('always')
    failures = NoseTestSuiteRunner(verbosity=2, interactive=True).run_tests(
        test_args)
    sys.exit(failures)


if __name__ == '__main__':
    runtests(*sys.argv[1:])
