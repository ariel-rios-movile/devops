#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Description: ExternalDataMapper remote manager.
"""
__author__ = "Ariel Gerardo Rios (ariel.rios@movile.com)"


import os
import logging
import time

import requests


APPLICATION = u"ExternalDataMapper"

URL_RELOAD_PATH = u"/manager/html/reload?path=/%s" % APPLICATION

CONTAINERS = [{
    u"name": u"buenosaires01",
    u"auth": {
        u"user": os.environ[u"BUENOSAIRES01_MANAGER_USER"],
        u"password": os.environ[u"BUENOSAIRES01_MANAGER_PASSWORD"],
    },
    u"restart": {
        u"url": u"http://10.112.83.15:8083",
    },
    u"check": {
        u"url": u"http://10.112.83.15:8083/ExternalDataMapper/api/equivalence",
        u"ok_status": 200,
        u"wait": 2,
        u"retries": 10,
        u"success": None,
    }
}, {
    "name": u"buenosaires02",
    u"auth": {
        u"user": os.environ[u"BUENOSAIRES02_MANAGER_USER"],
        u"password": os.environ[u"BUENOSAIRES02_MANAGER_PASSWORD"],
    },
    u"restart": {
        u"url": u"http://10.112.84.15:8083",
    },
    u"check": {
        u"url": u"http://10.112.83.15:8083/ExternalDataMapper/api/equivalence",
        u"ok_status": 200,
        u"wait": 2,
        u"retries": 10,
        u"success": None,
    },
}]


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M'
)

logger = logging.getLogger('edm')

logger.info(">>> Starting EDM remote manager")

for container in CONTAINERS:

    logger.info("Contacting container %(name)s", container)

    s = requests.Session()
    auth = requests.auth.HTTPBasicAuth(
        container[u"auth"][u"user"], container[u"auth"][u"password"]
    )

    url = u"%s%s" % (container[u"restart"][u"url"], URL_RELOAD_PATH)
    logger.debug(u"POST to restart URL: %s", url)

    response = s.post(url, auth=auth)
    logger.debug(u"Status: %s", response.status_code)

    for i in range(container[u"check"][u"retries"]):
        logger.debug(
            u"Try#%d: Waiting %d seconds to check ...", i,
            container[u"check"][u"wait"]
        )
        time.sleep(container[u"check"][u"wait"])

        logger.debug(
            u"Try#%d: Done. Requesting check URL: %s", i,
            container[u"check"][u"url"]
        )
        response = s.get(container[u"check"][u"url"])

        if response.status_code == container[u"check"][u"ok_status"]:
            logger.info(
                u"Try#%d: Response has expected status: %d", i,
                container[u"check"][u"ok_status"]
            )
            container[u"check"][u"success"] = True
            break
        else:
            logger.error(
                u"Response has failed on status: found=%s, expected=%d.",
                response.status_code, container[u"check"][u"ok_status"]
            )
            container[u"check"][u"success"] = False

    logger.info(
        u"Container %s restart result: %s", container[u"name"],
        container[u"check"][u"success"]
    )
logger.info("EDM remote manager finished.")
