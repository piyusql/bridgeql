# -*- coding: utf-8 -*-
# Copyright © 2023 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from bridgeql.django.auth import read_auth_decorator, write_auth_decorator
from bridgeql.django.exceptions import BridgeqlException, InvalidRequest
from bridgeql.django.helpers import JSONResponse, get_json_request_body
from bridgeql.django.models import ModelBuilder, ModelObject


@csrf_exempt
@require_http_methods(['POST'])
@write_auth_decorator
def create_django_model(request, db_name, app_label, model_name):
    try:
        params = get_json_request_body(request)
        mo = ModelObject(app_label, model_name, db_name)
        obj = mo.create(params)
        msg = 'Added new object of %s with pk=%s' % (
            model_name,
            obj.pk
        )
        res = {'data': obj.id, 'message': msg, 'success': True}
        return JSONResponse(res, status=201)
    except BridgeqlException as e:
        e.log()
        res = {'data': [], 'message': str(e.detail), 'success': False}
        return JSONResponse(res, status=e.status_code)


@csrf_exempt
@require_http_methods(['GET', 'POST'])
@read_auth_decorator
def read_django_model(request, db_name, app_label, model_name, pk=None):
    """
    GET  /read/<db>/<app>/<model>/<pk>/  — look up a single object by pk.
    POST /read/<db>/<app>/<model>/       — filter using a JSON payload in the
                                           request body to avoid URL-length limits.
    Any other combination returns HTTP 400.
    """
    try:
        if pk and request.method == 'GET':
            params = {
                'filter': {
                    'pk': pk
                }
            }
        elif not pk and request.method == 'POST':
            params = get_json_request_body(request)
        else:
            raise InvalidRequest(
                'GET requests require a pk in the URL; '
                'POST requests require a JSON payload in the request body'
            )
        mb = ModelBuilder(db_name, app_label, model_name, params)
        qset = mb.queryset()
        res = {'data': qset, 'message': '', 'success': True}
        return JSONResponse(res)
    except BridgeqlException as e:
        e.log()
        res = {'data': [], 'message': str(e.detail), 'success': False}
        return JSONResponse(res, status=e.status_code)


# no session to ride, hence no need for csrf protection
@csrf_exempt
@require_http_methods(['PATCH'])
@write_auth_decorator
def update_django_model(request, db_name, app_label, model_name, pk):
    try:
        params = get_json_request_body(request)
        mo = ModelObject(app_label, model_name, db_name, pk=pk)
        obj = mo.update(params)
        msg = 'Updated %s with pk=%s, fields=%s' % (
            model_name,
            obj.pk,
            ", ".join(params.keys()))
        res = {'data': obj.id, 'message': msg, 'success': True}
        return JSONResponse(res)
    except BridgeqlException as e:
        e.log()
        res = {'data': [], 'message': str(e.detail), 'success': False}
        return JSONResponse(res, status=e.status_code)


@csrf_exempt
@require_http_methods(['DELETE'])
@write_auth_decorator
def delete_django_model(_request, db_name, app_label, model_name, pk):
    try:
        mo = ModelObject(app_label, model_name, db_name, pk=pk)
        obj = mo.delete()
        msg = 'Deleted %s with pk=%s' % (model_name, pk)
        res = {'data': obj, 'message': msg, 'success': True}
        return JSONResponse(res)
    except BridgeqlException as e:
        e.log()
        res = {'data': [], 'message': str(e.detail), 'success': False}
        return JSONResponse(res, status=e.status_code)
