#!/usr/bin/env python
import os, sys

import django
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG = True,
                   DATABASES={
                        'default': {
                              'ENGINE': 'django.db.backends.sqlite3',
                              'ATOMIC_REQUESTS': True,
                        }
                  },
                   INSTALLED_APPS = ('django.contrib.auth',
                                     'django.contrib.contenttypes',
                                     'django.contrib.sessions',
                                     'django.contrib.admin',
                                     'hashbrown',
                                    )
                   )

try:
      django.setup()
except AttributeError:
      # Running Django<1.7
      pass

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['hashbrown', ])
if failures:
    sys.exit(failures)
