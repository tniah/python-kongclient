## Python - Kong Client

This is a Python library for the Kong admin API.

It was build around [kong 1.14.x specifications](https://docs.konghq.com/1.4.x/admin-api/)

## Installation ##

### PypI ###
```sh
pip install python-kongclient
```

### Manual ###
1. Clone the repository `git clone git@github.com:haintd/python-kongclient.git`
2. Enter it `cd python-kongclient`
3. Install it `python setup.py install`

## Instructions

**Import into your project**
```sh
from kongclient import KongClient
```

**Create a kong client**
```sh
kong_client = KongClient(kong_url='https://localhost:8444', verify_ssl=True)

kong_client.services.create(name='httpbin', url='https://httpbin.org')
kong_client.services.add_route(service_id='httpbin', name='route', hosts=['httpbin.org'])
kong_client.routes.list()
...
```

**For Python-Flask**
```sh
from flask import Flask
from kongclient.flask import KongClient

app = Flask(__name__)
app.config['KONG_ADMIN_URL'] = 'https://localhost:8444'
app.config['KONG_ADMIN_VERIFY_SSL'] = True
kong_client = KongClient(app)

@app.route('/services', methods=['GET])
def get_services():
   return kong_client.services.list()
```

For more details, checkout [kong documentation](https://docs.konghq.com/)