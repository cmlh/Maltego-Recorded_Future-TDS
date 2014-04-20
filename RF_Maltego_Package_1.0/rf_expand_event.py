#!/usr/bin/env python

"""Expand the entities related to an RF Event."""

import sys
from MaltegoTransform import *
from APIUtil import APIUtil
from rf_maltego_conv import *
mt = MaltegoTransform()

mt.parseArguments(sys.argv)
eid = mt.getVar("eid")

rfapi = APIUtil()

reference_query = {
    "reference": {
        "cluster_id":eid,
        "limit": 100
    }
}

sys.stderr.write("RF querying...\n")
ents = []
seen_ids = set()
seen_ids.add(eid)
for ceid, ent in rfapi.query(reference_query).get("entities", {}).items():
    if ceid not in seen_ids:
        ent["id"] = ceid
        ents.append(ent)
        seen_ids.add(ceid)

rf2maltego(mt, ents)

sys.stderr.write("RF Transform Done.\n")

mt.returnOutput()
