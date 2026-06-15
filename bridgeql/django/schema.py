# -*- coding: utf-8 -*-
# Copyright © 2023 VMware, Inc.  All rights reserved.
# SPDX-License-Identifier: BSD-2-Clause

from collections import defaultdict

from django.apps import apps

from bridgeql.django.helpers import get_allowed_apps


class BridgeqlModelFields:

    @classmethod
    def get_all_app_models(cls):
        _apps = apps.get_app_configs()
        _all_apps = [{_app.name: [_model.__name__ for _model in _app.get_models()]}
                     for _app in _apps]
        return _all_apps

    @classmethod
    def get_local_apps_models(cls):
        _local_apps = get_allowed_apps()
        _all_apps = cls.get_all_app_models()
        _local_apps_models = defaultdict(list)
        for _app in _local_apps:
            for each in _all_apps:
                if each.get(_app):
                    _local_apps_models[_app] = each.get(_app)
        return _local_apps_models
