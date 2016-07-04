# API_wrapper

## Basic info
This wrapper is supposed to act as a gateway to the HP WebInspect scanner. Given we don't want to grant all the methods to the users, we can expose only the methods we want. Using the self-generated tokens in the XML, we can grant as many users we want.

### Usage
Service is started easily, just by running:

./webpy_sample_webservice.py

By default the it will bind to the 9999 port, but you can change it to whatever to want.

Once it is started, you can make simple GET request visiting the site:
http://localhost:9999

You will get a bit information how to make a sample request to the server.


