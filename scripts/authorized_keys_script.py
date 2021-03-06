#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
import logging

logging.basicConfig(filename="/var/log/auth_prog.log",level=logging.DEBUG)

try:
    con = mdb.connect('localhost', 'login', 'password', 'database');

    cur = con.cursor(mdb.cursors.DictCursor)

    key = sys.stdin.readline().rstrip('\n')
    if (len(key) < 10):
        logging.debug("error key too short")
        sys.exit(1)
    cur.execute("SELECT `login` FROM `keys` WHERE `key`=%s", (key))
    logging.debug(key)
    rows = cur.fetchall()
    if (len(rows) == 0 or len(rows) >= 2):
        logging.debug("len: ==0 or >=2")
        sys.stdout.write("command='/bin/disabled'")
        sys.exit(1)
    row = rows[0]
    sys.stdout.write('command="my_svn-serve '+row["login"]+'",no-port-forwarding,no-X11-forwarding,no-agent-forwarding,no-pty')
    logging.debug(row['login'])
except mdb.Error, e:
    logging.debug("Error "+e.args[0]+": "+e.args[1])
    sys.exit(1)
    
finally:            
    if con:    
        con.close()

