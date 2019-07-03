#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import redis
import subprocess
from datetime import datetime
from pathlib import Path


r = redis.Redis(unix_socket_path='cache/cache.sock')

now = Path(str(datetime.now().isoformat()))

now.mkdir()

p = subprocess.Popen(['sudo', 'python', 'grgsm_scanner', '-w', str(now / 'scan.txt')])

p.communicate()

found = ''
not_found = ''
dafuck = ''

with open(now / 'scan.txt') as f:
    for line in f:
        parsed = re.findall('ARFCN:[ ]*(.*), Freq:[ ]*(.*), CID:[ ]*(.*), LAC:[ ]*(.*), MCC:[ ]*(.*), MNC:[ ]*(.*), Pwr:[ ]*(.*)', line)
        if not parsed[0]:
            continue
        arfcn, freq, cid, lac, mcc, mnc, pwr = parsed[0]
        name = '{}|{}|{}'.format(mnc, lac, cid)
        if r.exists(mcc):
            position = r.geopos(mcc, name)
            if position[0]:
                found += line
                found += 'http://www.openstreetmap.org/?mlat={0}&mlon={1}#map=17/{0}/{1}\n'.format(position[0][1], position[0][0])
                found += 'grgsm_livemon_headless -f {} --serverport=4730\n\n'.format(freq)
            else:
                not_found += line
                not_found += 'grgsm_livemon_headless -f {} --serverport=4730\n\n'.format(freq)
        else:
            dafuck += line
            dafuck == 'grgsm_livemon_headless -f {} --serverport=4730\n\n'.format(freq)

if found:
    with open(now / 'found.txt', 'w') as f:
        f.write(found)

if not_found:
    with open(now / 'notfound.txt', 'w') as f:
        f.write(not_found)
if dafuck:
    with open(now / 'dafuck.txt', 'w') as f:
        f.write(dafuck)
