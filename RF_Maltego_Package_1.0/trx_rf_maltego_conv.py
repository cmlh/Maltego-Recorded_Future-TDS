from xml.sax.saxutils import escape

__author__ = 'Mike Mohler Filip Reesalu'
__copyright__ = 'Copyright 2014, Recorded Future'
__credits__ = []

__license__ = 'Apache'
__version__ = '1.1'
__maintainer__ = 'Christian Heinrich'
__email__ = 'christian.heinrich@cmlh.id.au'
__status__ = 'Production'

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

def trx_rf2maltego(TRX, ents):
    """Use the Recorded Future entity type to transform into a Maltego entity. Default is maltego.Phrase."""
    for ent in ents:
        c_type = "maltego.Phrase"
        for k, v in types.items():
            if type(v) == type([]) and ent['type'] in v:
                c_type = k
            elif v == ent['type']:
                c_type = k

        ent['name'] = escape(ent['name'])
        ment = TRX.addEntity(c_type,ent['name'].encode('utf-8'))
        ent["id"] = escape(ent["id"])
        ment.addProperty("eid","Entity ID", False, ent["id"]);
        ent["type"] = escape(ent["type"])        
        ment.addProperty("properties.rftype", "Entity Type", False, ent["type"])
