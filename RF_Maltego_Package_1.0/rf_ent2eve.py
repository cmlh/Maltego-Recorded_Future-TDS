#!/usr/bin/env python

"""Find events related to an RF Entity."""

import sys
from datetime import date
from dateutil.relativedelta import relativedelta
from MaltegoTransform import *
from rf_maltego_conv import rf2maltego
from APIUtil import APIUtil

mt = MaltegoTransform()

mt.parseArguments(sys.argv)
eid = mt.getVar("eid")

if not eid:
    sys.stderr.write("This transform will only work on entities with the 'eid' property.\n")
    exit(1)

rfapi = APIUtil()
# Limit to the past 6 months.
min_pub = date.today() + relativedelta( months = -6 )

cluster_query = {
    "cluster": {
        "document": {
            "published": {
                "min": str(min_pub)
            }
        },
        "attributes": [
            {
                "entity": { "id" : eid },
            }
        ],
        "limit": 100
    }
}

for eve in rfapi.query(cluster_query).get("events", []):
    rfevent = mt.addEntity("recfut.RFEvent",eve['type'] + " [id: {0}]".format(eve['id']));
    rfevent.addAdditionalFields("eid","Event ID",False,eve['id']);
    rfevent.addAdditionalFields("etype","Event Type",False,eve['type']);
    rfevent.addAdditionalFields("starttime","Start Time",False,eve['attributes'].get('start',''));
    rfevent.addAdditionalFields("stoptime","Stop Time",False,eve['attributes'].get('stop',''));
    rfevent.addAdditionalFields("fragment","Fragment",False,eve['stats']['top_sources'][0]['fragment'].encode('utf-8'));
    rfevent.addAdditionalFields("document_link","Document Link",False,eve['stats']['top_sources'][0]['document_link'].encode('utf-8'));

sys.stderr.write("RF Transform Done.\n")

mt.returnOutput()
