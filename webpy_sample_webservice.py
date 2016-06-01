#!/usr/bin/env python
#
# The sample curl request to the service is the json. Something like this
# curl -i -H "Content-Type: application/json" -X POST -d '{"value":"310","type":"Tip 3","targetModule":"Target 3","active":true}' http://localhost:8080
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
        data_got_from_request = data["value"]

        print root[0][1].text

#       for child in root:
#               print 'child', child.tag



        if data_got_from_request == '30':
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
