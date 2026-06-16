# -*- coding: utf-8 -*-
# Copyright © 2023 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

import base64
import importlib
import json
import socket


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def local_ip_hostname():
    hostname = socket.getfqdn()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('192.255.255.255', 1))
        ip_address = s.getsockname()[0]
    except OSError:
        ip_address = '127.0.0.1'
    finally:
        s.close()
    return ip_address, hostname


def b64encode(data):
    return base64.b64encode(data.encode('utf-8'))


def b64decode(data):
    return base64.b64decode(data).decode('utf-8')


def b64encode_json(data):
    return base64.b64encode(json.dumps(data).encode('utf-8'))


def b64decode_json(data):
    return json.loads(base64.b64decode(data).decode('utf-8'))


def load_function(function_str):
    mod_name, func_name = function_str.rsplit('.', 1)
    mod = importlib.import_module(mod_name)
    return getattr(mod, func_name)
