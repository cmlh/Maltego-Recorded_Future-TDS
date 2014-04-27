import socket;
from Maltego import *

## This is a fully functional example transform
## Input type is a DNSName. It will resolve to IP address
def trx_DNS2IP(m):
    TRX = MaltegoTransform()
    
    DNSName=None
    try:
        DNSName = socket.gethostbyname(m.Value)
        TRX.addEntity("maltego.IPv4Address",DNSName)
    except socket.error as msg:
        TRX.addUIMessage("Error:"+str(msg),UIM_PARTIAL)
    
    #Write the slider value as a UI message - just for fun
    TRX.addUIMessage("Slider value is at: "+str(m.Slider))
         
    return TRX.returnOutput()    
    

    
    
# Input is a phrase entity
# Output is AS numbers
# You need ISDIV defined as transform setting on the TDS
def trx_EnumAS(m):
    # construct a return vessel
    TRX = MaltegoTransform()

    #read the value, make sure its a digit
    if (not m.Value.isdigit()):
	# if not - complain
        TRX.addUIMessage('Sorry but ['+m.Value+'] is not a whole number',UIM_PARTIAL)
        return TRX.returnOutput()

    #read the setting - you need ISDIV defined as transform setting in the TDS
    isdiv = m.getTransformSetting('ISDIV')
	
    #check if its a digit - else complain even more bitterly
    if (not isdiv.isdigit()):
        TRX.addUIMessage('Silly! We need a number',UIM_FATAL)
        return TRX.returnOutput()

    #here we know we're good to go.
    #read the value of the node
    howmany = int(m.Value);

    # how many have accumulated?
    accum=0;

    for i in range(1,howmany+1):
        if (i % int(isdiv) == 0):
		
      	    # add an AS entity with the index as a value...
            Ent = TRX.addEntity('maltego.AS', str(i))
            
            # ... and set the weight
            Ent.setWeight(howmany-i)
			
            # add a property called 'div' 
            Ent.addProperty('div','Divisible by','strict',str(isdiv))
			
            # see it's odd or even and set the link/note/bookmark properties
            # this makes for a very ugly graph..but..ya
            if (i%2==0):
                Ent.setLinkColor('0x00FF00')
		Ent.setNote('Even')
		Ent.setLinkLabel('Even link')
		Ent.setLinkStyle(LINK_STYLE_NORMAL)
		Ent.setLinkThickness(1)
		Ent.setBookmark(BOOKMARK_COLOR_GREEN)
            else:
		Ent.setLinkColor('0xFF0000')
		Ent.setNote('Odd')
		Ent.setLinkLabel('Odd link')
		Ent.setLinkStyle(LINK_STYLE_DASHED)
		Ent.setLinkThickness(2)
		Ent.setBookmark(BOOKMARK_COLOR_RED)

            accum=accum+1;
            if accum>=m.Slider:
                break

    # return the XML to the TDS server
    return TRX.returnOutput()
