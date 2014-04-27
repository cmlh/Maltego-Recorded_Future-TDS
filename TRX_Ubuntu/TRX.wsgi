import os,sys

# To run in debug, comment the next two lines and see 
# end of this file

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))



from bottle import *
from Maltego import *

# Transform Libraries goes here:
from DNSTRANSFORMS import *



##### TRANSFORM DISPATCHER starts here -->

#------> DNS2IP transform
@route('/DNS2IP', method='ANY')    
def DNS2IP():
    if request.body.len>0:
        return(trx_DNS2IP(MaltegoMsg(request.body.getvalue())))


# -----> EnumAS transform
@route('/EnumAS', method='ANY')    
def EnumAS():
    if request.body.len>0:
        return(trx_EnumAS(MaltegoMsg(request.body.getvalue())))





## ---> Start Server
## To start in debug mode: Comment the line below...
application = default_app()

## ... and uncomment line below
#run(host='0.0.0.0', port=9001, debug=True, reloader=True)