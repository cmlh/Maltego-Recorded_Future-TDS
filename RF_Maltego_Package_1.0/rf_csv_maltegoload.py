#!/usr/bin/env python

"""Transform a CSV file exported from the Recorded Future UI into Maltego entities."""

import json
import sys
import csv
import Tkinter, tkFileDialog
from MaltegoTransform import *

mt = MaltegoTransform()

# Use Tkinter to open up a file dialog.
root = Tkinter.Tk()
root.lift()
root.withdraw()
sys.stderr.write("Click the Python icon to select a file.")
csvfilename = tkFileDialog.askopenfilename()

data = csv.DictReader(open(csvfilename), delimiter=',',fieldnames=('Event Id','Event Type','Event Title','Start Time','End Time','Precision','Count','First Published Time','Last Published Time','Sample Fragment','Entities','Locations','Source Count','Positive Sentiment','Negative Sentiment'))

next(data)

for row in data:
    event = row['Event Type']+"-"+row['Event Id']
    rfevent = mt.addEntity("recfut.RFEvent",event);
    rfevent.addAdditionalFields("eid","Event ID",False,row['Event Id']);
    rfevent.addAdditionalFields("etype","Event Type",False,row['Event Type']);
    rfevent.addAdditionalFields("title","Event Title",False,row['Event Title']);
    rfevent.addAdditionalFields("starttime","Start Time",False,row['Start Time']);
    rfevent.addAdditionalFields("stoptime","Stop Time",False,row['End Time']);
    rfevent.addAdditionalFields("fragment","Fragment",False,row['Sample Fragment']);
    rfevent.addAdditionalFields("precision","Precision",False,row['Precision']);
    rfevent.addAdditionalFields("count","Count",False,row['Count']);
    rfevent.addAdditionalFields("firstpublished","First Published",False,row['First Published Time']);
    rfevent.addAdditionalFields("lastpublished","Last Published",False,row['Last Published Time']);
    rfevent.addAdditionalFields("sourcecount","Source Count",False,row['Source Count']);
    rfevent.addAdditionalFields("pos_sentiment","Positive Sentiment",False,row['Positive Sentiment']);
    rfevent.addAdditionalFields("neg_sentiment","Negative Sentiment",False,row['Negative Sentiment']);

mt.addUIMessage("RF event load completed!")
mt.returnOutput()

