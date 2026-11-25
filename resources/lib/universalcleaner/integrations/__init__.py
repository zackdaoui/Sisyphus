# -*- coding: utf-8 -*-
"""Registry of supported add-on integrations.

To add support for another add-on, create a module here with an Integration
subclass and add it to ALL_INTEGRATIONS (see CONTRIBUTING.md).
"""
from .elementum import ElementumIntegration
from .pov import PovIntegration
from .tmdbhelper import TmdbHelperIntegration

ALL_INTEGRATIONS = [
    ElementumIntegration(),
    PovIntegration(),
    TmdbHelperIntegration(),
]
