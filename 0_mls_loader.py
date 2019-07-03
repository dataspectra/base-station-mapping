#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import redis
import argparse


'''
Notes:
    net == mnc
    area == lac

    File to download: https://location.services.mozilla.com/downloads
'''



parser = argparse.ArgumentParser(description='File to load')
parser.add_argument('-f', '--file', help='Mass process queries from a file.')
args = parser.parse_args()

r = redis.Redis(unix_socket_path='cache/cache.sock')

r.flushall()

p = r.pipeline()

with open(args.file) as f:
    reader = csv.DictReader(f)
    for i, row in enumerate(reader):
        name = '{}|{}|{}'.format(row['net'], row['area'], row['cell'])
        p.geoadd(row['mcc'], row['lon'], row['lat'], name)
        if (i % 10000) == 0 :
            p.execute()
            p = r.pipeline()
p.execute()
