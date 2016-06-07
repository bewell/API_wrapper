#!/usr/bin/env python
#
# curl -i -H "Content-Type: application/json" -X POST -d '{"SecurityToken":"1","user":"Steve"}' http://localhost:8080
#
#

import web
import json
import urlparse
import requests
import xml.etree.ElementTree as ETT
from lxml import etree as ET


urls = (
    '/(.*)', 'hello'
)

tree = ET.parse('user_data.xml')
root = tree.getroot()


app = web.application(urls, globals())

class hello:
#     def GET(self, name):
#        if not name: 
#            name = 'World'
#        return 'Hello, ' + name + '!'
    def POST(self, _):
        data = json.loads(web.data())   # in this step we load the json, that was received from client
        SecurityToken_got_from_request = data["SecurityToken"]  #take only SecurityToken
        
        # from here we iterate the xml to confirm SecurityToken, also we are finding attribute of the same parrent
        for child in root.iter('SecurityToken'):
            SecurityTokenParent = child.getparent()
            if SecurityToken_got_from_request == child.text:
                for NavId in root.iter('NavID'):
                        NavIDParent = NavId.getparent()
                        if SecurityTokenParent.attrib.values() == NavIDParent.attrib.values():
                            print "You win"
        #               r = requests.get('https://api.github.com/events')
        # gaunam NavID parent, jeigu jie lygus, do action

        





        web.header('Content-Type', 'application/json')
#from here the response back to the user
        try:
                r
        except NameError:
                return 'The sample request to the github was not made. Probably the variable "value" did not match '
        else:
                return r.headers


if __name__ == "__main__":
    app.run()
