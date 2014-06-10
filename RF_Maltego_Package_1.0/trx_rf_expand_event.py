#!/usr/bin/env python

"""Expand the entities related to an RF Event."""

import sys
from Maltego import *
from APIUtil import APIUtil
from rf_maltego_conv import *

def trx_rf_expand_event(m):
    TRX = MaltegoTransform();
    eid = m.getProperty("eid")

    rfapi = APIUtil()

    instance_query = {
        "instance": {
            "cluster_id":eid,
            "limit": 20
        }
    }
    
    ents = []
    seen_ids = set()
    seen_ids.add(eid)
    # Remove two lines in production i.e. debug Maltego Messages
    rf_api_url_query = rfapi.query_url(instance_query)
    TRX.addUIMessage(rf_api_url_query,UIM_DEBUG)
    for ceid, ent in rfapi.query(instance_query).get("entities", {}).items():
        if ceid not in seen_ids:
            ent["id"] = ceid
            ents.append(ent)
            seen_ids.add(ceid)

    rf2maltego(TRX, ents)


    return TRX.returnOutput()
