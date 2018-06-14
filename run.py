#!/usr/bin/env python
# -*- coding: utf-8 -*-

from main import app
from main import networkutil
if __name__ == "__main__":
    app.debug = app.config['DEBUG']
    ip = networkutil.getnetworkip()
    #sapp.config['MAIN_URL']="http://"+ip+"/"
    app.run(ip)
