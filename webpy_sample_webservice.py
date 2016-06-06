#!/usr/bin/env python
#
# curl -i -H "Content-Type: application/json" -X POST -d '{"SecurityToken":"1","user":"Steve"}' http://localhost:8080
#
#

import web
import json
import urlparse
import requests
import xml.etree.ElementTree as ET


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
        data = json.loads(web.data())
        data_got_from_request = data["SecurityToken"]

        for child in root.iter('SecurityToken'):
            if data_got_from_request == child.text:
                r = requests.get('https://api.github.com/events')


        





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
