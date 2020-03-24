#!/usr/bin/env python3
# import utils for tawny.wtf website
import tawny_wtf_utils
import time
import datetime

# update site
tawny_wtf_utils.update_s3_website()

print('-------------------------------------------')
print('Tawny.wtf was successfully updated at:')
print(datetime.datetime.now())
print('-------------------------------------------')
