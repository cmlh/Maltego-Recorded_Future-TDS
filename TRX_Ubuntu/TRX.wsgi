import os,sys

# To run in debug, comment the next two lines and see 
# end of this file

os.chdir(os.path.dirname(__file__))
sys.path.append(os.path.dirname(__file__))



from bottle import *
from Maltego import *
from trx_rf_expand_event import *

#------> RF Expand Event Transform
@route('/RFEvent', method='ANY')    
def RFEvent():
    if request.body.len>0:
        return(trx_rf_expand_event(MaltegoMsg(request.body.getvalue())))
        
## ---> Start Server
## To start in debug mode: Comment the line below...
application = default_app()

## ... and uncomment line below
#run(host='0.0.0.0', port=9001, debug=True, reloader=True)