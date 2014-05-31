# Specific types that we want to convert.
types = {'maltego.Person':'Person',
        'recfut.Company':['Company', 'OrgEntity'],
        'recfut.Organization':'Organization',
        'recfut.Product':'Product',
        'recfut.Technology':'Technology',
        'recfut.Position':'Position',
        'maltego.IPv4Address':'IpAddress',
        'maltego.Domain':"URL",
        'maltego.Location':['Continent', 'Country', 'City', 'ProvinceOrState', 'Region', 'NaturalFeature', 'GeoEntity'],
        'maltego.File':'WinExeFile',
        'maltego.Twit':'Username'
        }

def rf2maltego(TRX, ents):
    """Use the Recorded Future entity type to transform into a Maltego entity. Default is maltego.Phrase."""
    for ent in ents:
        c_type = "maltego.Phrase"
        for k, v in types.items():
            if type(v) == type([]) and ent['type'] in v:
                c_type = k
            elif v == ent['type']:
                c_type = k

        ment = TRX.addEntity(c_type,ent['name'].encode('utf-8'))
        ment..addProperty("eid","Entity ID", False, ent["id"]);
        ment..addProperty("properties.rftype", "Entity Type", False, ent["type"])


