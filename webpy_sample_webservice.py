#!/usr/bin/env python
#
# 
#
#

import web
import json
import urlparse
import requests
from lxml import etree as ET
from io import StringIO, BytesIO

#SSL support
#from web.wsgiserver import CherryPyWSGIServer
#CherryPyWSGIServer.ssl_certificate = "/path/to/ssl_certificate"
#CherryPyWSGIServer.ssl_private_key = "/path/to/ssl_private_key"

urls = (
    '/', 'WrapperService',
    '/CreateScan', 'CreateScan',
)

WebInspectLicenseHost = "https://slgdsm020002314.intranet.barcapint.com/WIE/Licenseservice.asmx"
WebInspectManagerHost = "https://slgdsm020002314.intranet.barcapint.com/WIE/Managerservice.asmx"

##### Parsing User data xml where the static tokens are kept ###########
tree = ET.parse('user_data.xml')
root = tree.getroot()
###### END of PARSING ###########

class WebService(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

class WrapperService:
    def GET(self):
        web.header('Content-Type', 'html')
        return "<html>Hello, this is a webservice to interact with the WebInspect Scanner. <br></br> If you are here, that means you have your team token. The example request to the Wrapper service looks like this: <br></br> curl -i -H \"Content-Type: application/json\" -X POST -d '{\"SecurityToken\":\"4\",\"user\":\"Steve\",\"TeamURL\":\"https://teamURL\"}' http://scannerURL </html>"


    #######################################################
    #       From here the Webinspection session management
    #       We need the LicenseSessionKeyValue from the server and then we'll need to include that into all our requests to the server
    #
    #
    @staticmethod
    def authenticateToWebInspectServer():
        headers = {'SOAPAction': 'urn:com:spidynamics:webservices:Amp/ObtainClientLicense2', 'Content-Type': 'text/xml; charset=utf-8'}
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
            <username>ViliusSecTest1</username>
            <password>P@ssw0rd</password>
            </ObtainClientLicense2>
            </soap:Body>
            </soap:Envelope>"""
            #<username>APIwrapper</username>
            #<password>@P1wrapper</password>
        TheLicenseSessionKey = requests.post(WebInspectLicenseHost,data=ObtainLicensePOST_data,headers=headers,verify=False) # this response contains the ObtainClientLicense2Result which we need
        xmlResponseTree = ET.parse(BytesIO(TheLicenseSessionKey.content))
        
        TheLicenseSessionKeyValue = xmlResponseTree.find('.//{urn:com:spidynamics:webservices:Amp}ObtainClientLicense2Result').text
        return TheLicenseSessionKeyValue
    #######################################################
    
    @staticmethod
    def GetAllCompletedScans(token, URL):
        headers = {'SOAPAction': 'urn:com:spidynamics:webservices:Amp/GetAllCompletedScansBasic', 'Content-Type': 'text/xml; charset=utf-8'}
        POST_data = """<?xml version="1.0" encoding="utf-8"?>
                    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                    <soap:Body>
                        <GetAllCompletedScansBasic xmlns="urn:com:spidynamics:webservices:Amp">
                            <licenseToken>"""+token+"""</licenseToken>
                        </GetAllCompletedScansBasic>
                    </soap:Body>
                    </soap:Envelope>"""
        AllCompletedScans = requests.post(WebInspectManagerHost,data=POST_data,headers=headers,verify=False)
        JSONresponseToTheUser = []
        xmlResponseTree = ET.parse(BytesIO(AllCompletedScans.content))
        ScanList = xmlResponseTree.findall('.//{urn:com:spidynamics:webservices:Amp}ScanBasic')
        #the cycle is to extract only the scan that the team is requesting
        for element in ScanList:
            ScanURL = element.find('.//{urn:com:spidynamics:webservices:Amp}StartUri')
            for sub_element in element:
                split = sub_element.tag.split("}")       #here we are dropping the beginning of the string {urn:com:spidynamics:webservices:Amp} and returning the names of the tags 
                JSONresponseToTheUser.append({'tag': split[1], 'value' : sub_element.text})
        return JSONresponseToTheUser
        
    
    
    def POST(self):
        data = json.loads(web.data())   # in this step we load the json, that was received from client
        SecurityToken_got_from_request = data["SecurityToken"]  #extract the SecurityToken
        URL_got_from_request = data["TeamURL"]                      #extract the URL which was provided by the client
        
        # from here we iterate the xml to confirm SecurityToken, also we are finding TeamURL attribute of the same parrent
        for SecurityToken in root.iter('SecurityToken'):
            if SecurityToken_got_from_request == SecurityToken.text:
                for TeamURL in root.iter('TeamURL'):
                        if (SecurityToken.getparent().attrib.values() == TeamURL.getparent().attrib.values() and TeamURL.text in URL_got_from_request):
        #if those two parents match, that means we have attributes from the same element, we can compare the provided URL. On success we're making the call to the scanner.
                            authenticationToken = WrapperService.authenticateToWebInspectServer()
                            response = WrapperService.GetAllCompletedScans(authenticationToken, URL_got_from_request)
                            return response




        web.header('Content-Type', 'application/json')
        #from here the response back to the user
        try:
                response
        except NameError:
                return 'The request failed. Probably the variable "SecurityToken" did not match, or you specified invalid URL'

 
class CreateScan:
    
    @staticmethod
    def StartTheScan(token, URL):
        headers = {'SOAPAction': 'urn:com:spidynamics:webservices:Amp/CreateWebScan', 'Content-Type': 'text/xml; charset=utf-8'}
        POST_data = """ """
        StartScan = request.post(WebInspectManagerHost, data=POST_data, headers=headers, verify=False)
        return StartScan.content
        
    
    
    
    def POST(self):
        data = json.loads(web.data())   # in this step we load the json, that was received from client
        SecurityToken_got_from_request = data["SecurityToken"]  #extract the SecurityToken
        URL_got_from_request = data["TeamURL"]                      #extract the URL which was provided by the client
        for SecurityToken in root.iter('SecurityToken'):
            if SecurityToken_got_from_request == SecurityToken.text:
                return "True"
                #authenticationToken = WrapperService.authenticateToWebInspectServer()
                #
        

        return "This is Create function with the token: " + SecurityToken_got_from_request + "</>"






if __name__ == "__main__":
    app = WebService(urls, globals())
    app.run(port=9999)
