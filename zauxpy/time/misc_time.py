#!/usr/bin/env python

import datetime
from dateutil.tz import tzlocal


def localnow():
    return datetime.datetime.now().astimezone(tzlocal())
