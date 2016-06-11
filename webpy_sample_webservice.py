#!/usr/bin/env python
#
# curl -i -H "Content-Type: application/json" -X POST -d '{"SecurityToken":"1","user":"Steve","TeamURL":"http://google.com"}' http://localhost:8080
#
#

import web
import json
import urlparse
import requests
# import xml.etree.ElementTree as ETT
from lxml import etree as ET
from io import StringIO, BytesIO

urls = (
    '/(.*)', 'hello'
)
'''
#######################################################
#       From here the Webinspection session management
#       We need the LicenseSessionKeyValue from the server and then we'll need to include that into all our requests to the server
#
#

WebInspectHost = "/WIE/Licenseservice.asmx"
headersForLicense = {'SOAPAction': 'urn:com:spidynamics:webservices:Amp/ObtainClientLicense2', 'Content-Type': 'text/xml; charset=utf-8'}
ObtainLicensePOST_data = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
    <soap:Body>
    <ObtainClientLicense2 xmlns="urn:com:spidynamics:webservices:Amp">
        <clientInfo>
        <ClientID>11111111-1111-1111-1111-111111111111</ClientID>
        <AppType>WIE</AppType>
        <AppSubtype>Console</AppSubtype>
        <AppVersion>10.50.308.10</AppVersion>
        <CompatibilityVersion>1.0</CompatibilityVersion>
            </clientInfo>
                <username>username</username>
                    <password>password</password>
                </ObtainClientLicense2>
                    </soap:Body>
</soap:Envelope>"""
TheLicenseSessionKey = requests.post(WebInspectHost,data=ObtainLicensePOST_data,headers=headersForLicense,verify=False) # this response contains the ObtainClientLicense2Result which we need

xmlResponseTree = ET.parse(BytesIO(TheLicenseSessionKey.content))

TheLicenseSessionKeyValue = xmlResponseTree.find('.//{urn:com:spidynamics:webservices:Amp}ObtainClientLicense2Result').text
print TheLicenseSessionKeyValue
#
#
#######################################################
'''

tree = ET.parse('user_data.xml')
root = tree.getroot()


app = web.application(urls, globals())

class hello:
################################
# this was the sample GET method which returns Hello World
#     def GET(self, name):
#        if not name: 
#            name = 'World'
#        return 'Hello, ' + name + '!'
################################
    def POST(self, _):
        data = json.loads(web.data())   # in this step we load the json, that was received from client
        SecurityToken_got_from_request = data["SecurityToken"]  #extract the SecurityToken
        URL_got_from_request = data["URL"]                      #extract the URL which was provided by the client
        
        # from here we iterate the xml to confirm SecurityToken, also we are finding TeamURL attribute of the same parrent
        for SecurityToken in root.iter('SecurityToken'):
            if SecurityToken_got_from_request == SecurityToken.text:
                for TeamURL in root.iter('TeamURL'):
                        if (SecurityToken.getparent().attrib.values() == TeamURLgetparent().attrib.values() and URL_got_from_request == TeamURL.text):
        #if those two parents match, that means we have attributes from the same element, we can compare the provided URL. On success we're making the call to the scanner.
        
                            r = requests.get(URL_got_from_request)





        web.header('Content-Type', 'application/json')
#from here the response back to the user
        try:
                r
        except NameError:
                return 'The sample request was not made. Probably the variable "SecurityToken" did not match, or you specified invalid URL'
        else:
                return r.headers


if __name__ == "__main__":
    app.run()
