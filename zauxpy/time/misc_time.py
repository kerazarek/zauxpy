#!/usr/bin/env python

import datetime
from dateutil.tz import tzlocal

ZAUX_MODULE_MISC_TIME_IMPORTED = True

def localnow():
    return datetime.datetime.now().astimezone(tzlocal())
