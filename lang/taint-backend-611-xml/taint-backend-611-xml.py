from xml.etree import ElementTree, cElementTree
from xml.dom.expatbuilder import parse
from defusedxml.ElementTree import parse as defusedParse
from flask import Flask, request 

app = Flask(__name__)
DOCUMENT = "file.xml"
XML_STRING = "<note>\n\
<to>GR</to>\n\
<from>Security Squad</from>\n\
<heading>Reminder</heading>\n\
<body>Don't forget to update</body>\n\
</note>"

@app.route("/test")
def test():
    taintedInput = request.args["xml_string"]

    # ruleid: taint-backend-611-xml
    node = cElementTree.parse(taintedInput)
    
    # ok: taint-backend-611-xml
    node = ElementTree.parse(DOCUMENT)
    
    # ruleid: taint-backend-611-xml
    node = ElementTree.fromstring(taintedInput)
    
    # ok: taint-backend-611-xml
    node = cElementTree.fromstring(XML_STRING)
    
    taintedInput = sanitize(taintedInput)
    # todook: taint-backend-611-xml
    node = cElementTree.parse(taintedInput)
    
    # ruleid: taint-backend-611-xml
    node = parse(taintedInput)
    
    # ok: taint-backend-611-xml
    node = defusedParse(taintedInput)