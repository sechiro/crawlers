# -*- coding: utf-8 -*-
__author__ = 'sechiro'
import json
import re
from datetime import datetime

filename = 'uniqlo_search.jl'

with open(filename) as f:
    jlines = f.readlines()

for i in jlines:
    item = json.loads(i)

    raw_date = item['update_date'].replace(u'更新日: ','').replace(u'日','')
    ascii_date = re.sub(u'[年月]','-', raw_date)
    formatted_date = datetime.strptime(ascii_date, '%Y-%m-%d')
    #print ascii_date
    #print formatted_date

    if formatted_date > datetime.strptime('2013-10-14', '%Y-%m-%d'):
        continue

    for key in item.keys():
        if key == 'source_links' or key == 'source_twitter_links':
            for j in item[key]:
                print '{0}: {1}'.format(key, j.encode('utf-8'))
        elif key == 'update_date':
            raw_date = item[key].replace(u'更新日: ','').replace(u'日','')
            ascii_date = re.sub(u'[年月]','-', raw_date)
            formatted_date = datetime.strptime(ascii_date, '%Y-%m-%d')
            print ascii_date
            #print formatted_date

        elif key == 'contents':
            pass
        else:
            print '{0}: {1}'.format(key, item[key].encode('utf-8'))

    print '\n'
