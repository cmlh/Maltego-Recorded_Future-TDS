#!/usr/bin/env python

"""Resolve a company or an organization by name using the Recorded Future API."""

import sys
from MaltegoTransform import *
from APIUtil import APIUtil

mt = MaltegoTransform()

mt.parseArguments(sys.argv)
name = mt.getVar("properties.companyname")

sys.stderr.write("Resolving company...")

rfapi = APIUtil()

entity_query = {
        "entity":{"name":name, "type":["Company", "Organization"], "limit":1}
}

query_response = rfapi.query(entity_query)
eid = None
for q_eid, q_ent in query_response.get('entity_details', {}).items():
    sys.stderr.write("Found eid: {0}".format(q_eid))
    name = q_ent['name']
    eid = q_eid
    etype = q_ent['type']
    ent = q_ent

if not eid:
    sys.stderr.write("Could not resolve any company/organization named '{0}'".format(name.encode('utf-8')))
    exit(1)

ment = mt.addEntity('recfut.Company' if etype == 'Company' else 'recfut.Organization',name.encode('utf-8'))
ment.addAdditionalFields("eid","Entity ID", False, eid);

sys.stderr.write("RF Transform Done.\n")

mt.returnOutput()
