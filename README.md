
# OAF Seed Packer API Backend


Welcome to the OAF Seed Packer backend API. This backend serves the OAF Seed Packer frontend with farmers, orders and products.
Find the live backend hosted [here](https://oaf-packager.herokuapp.com/)

This backend was built following [PEP8](https://www.python.org/dev/peps/pep-0008/) standards.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

The backend is provided by [postgresql](https://www.postgresql.org/download/).

## Running the server

From within the `root` directory first ensure you are working using your created virtual environment.

To run the server, create a .env file.

```bash
    touch .env
```

Inside the .env file, export your database URIs

```bash
export DATABASE_URL='your-database-url'
export AUTH0_DOMAIN='your-auth0-domain'
export ALGORITHMS=['your-auth0-decoding-algorithm']
export API_AUDIENCE='your-auth0-api-identifier'
export FLASK_ENV='development-stage'
export TEST_DATABASE_URL='your-test-database'

```

Then excecute:

```bash
py app.py
```

```bash

Endpoints
GET '/farmers'
POST '/farmers'
PUT '/farmers/<int:farmer_id>'
DELETE '/farmers/<int:farmer_id>'

GET '/products'
POST '/products'
PUT '/products/<int:product_id>'
DELETE '/products/<int:product_id>'

GET '/orders'
POST '/orders'
PUT '/orders/<int:order_id>'
DELETE '/orders/<int:order_id>'
```

```bash

curl http://127.0.0.1:5000/farmers -H "Authorization: Bearer {{token}}"

- Fetches a list of farmers
- Returns:
{
    "count": 2,
    "data": [
        {
            "email": "peter@gmail.com",
            "firstname": "peter",
            "id": 1,
            "lastname": "pan",
            "phone": "0753969099"
        },
        {
            "email": "neil@oaf.com",
            "firstname": "Neil",
            "id": 2,
            "lastname": "Warnock",
            "phone": "1234"
        }
    ],
    "success": true
}

```

```bash

curl -X DELETE http://127.0.0.1:5000/farmers/1 -H "Authorization: Bearer {{token}}"

- Deletes a farmer
- Returns:
{
    'message': 'farmer successfully deleted'
    "success": true
}
```

```bash

curl  http://127.0.0.1:5000/farmers -X POST
-H "Content-Type: application/json" 
-H "Authorization: Bearer {{token}}" 
-d '{
	"firstname": "peter",
	"lastname": "pan",
	"phone": "0753969099",
	"email": "peter@gmail.com",
	"country": "kenya",
	"state": "central",
	"village": "kazinga"
}'

- Posts a farmer
- Returns:
{
    "id": 3,
    "message": "farmer successfully created",
    "success": true
}
```

```bash
curl http://127.0.0.1:5000/products -H "Authorization: Bearer {{token}}"

- Fetches a list of products
- Returns:
{
    "count": 3,
    "data": [
        {
            "description": "african oat beans",
            "id": 1,
            "name": "oats"
        },
        {
            "description": "African Beans",
            "id": 2,
            "name": "Beans"
        },
        {
            "description": "african oat beans",
            "id": 3,
            "name": "Barley"
        }
    ],
    "success": true
}

```

```bash

curl -X DELETE http://127.0.0.1:5000/products/1 -H "Authorization: Bearer {{token}}"

- Deletes a product
- Returns:
{
    'message': 'product successfully deleted'
    "success": true
}
```

```bash

curl  http://127.0.0.1:5000/products -X POST
-H "Content-Type: application/json" 
-H "Authorization: Bearer {{token}}" 
-d '{
	"name": "Barley",
	"description": "african oat beans",
	"qty": 10.0,
	"unit_price": "3000"
}'

- Posts a farmer
- Returns:
{
    "id": 3,
    "message": "product successfully created",
    "success": true
}
```

```bash

curl  http://127.0.0.1:5000/products/1 -X PUT
-H "Content-Type: application/json" 
-H "Authorization: Bearer {{token}}" 
-d '{
	"name": "Barley",
	"description": "african oat beans",
	"qty": 10.0,
	"unit_price": "3000"
}'

- Posts a product
- Returns:
{
    "id": 3,
    "message": "product successfully updated",
    "success": true
}
```

```bash
curl http://127.0.0.1:5000/orders -H "Authorization: Bearer {{token}}"

- Fetches a list of orders
- Returns:
{
    "count": 3,
    "data": [
        {
            "farmer_id": 1,
            "farmer_name": "peter pan",
            "id": 1,
            "order_date": "Tue, 31 Dec 2019 00:00:00 GMT",
            "order_total": 300.0
        },
        {
            "farmer_id": 1,
            "farmer_name": "peter pan",
            "id": 4,
            "order_date": "Fri, 24 Jan 2020 00:00:00 GMT",
            "order_total": 120000.0
        },
        {
            "farmer_id": 1,
            "farmer_name": "peter pan",
            "id": 5,
            "order_date": "Tue, 31 Dec 2019 00:00:00 GMT",
            "order_total": 300.0
        }
    ],
    "success": true
}

```

```bash

curl -X DELETE http://127.0.0.1:5000/orders/1 -H "Authorization: Bearer {{token}}"

- Deletes an order
- Returns:
{
    'message': 'order successfully deleted'
    "success": true
}
```

```bash

curl  http://127.0.0.1:5000/orders -X POST
-H "Content-Type: application/json" 
-H "Authorization: Bearer {{token}}" 
-d '{
	"farmer_id": 1,
	"order_date": "2019-12-31",
	"order_details": [{
		"product_id": 1,
		"line_no": 1,
		"order_qty": 2,
		"line_total": 300
	}]
}'

- Posts a farmer
- Returns:
{
    "id": 5,
    "message": "order successfully created",
    "success": true
}
```

```bash

curl  http://127.0.0.1:5000/orders/1 -X PUT
-H "Content-Type: application/json" 
-H "Authorization: Bearer {{token}}" 
-d '{
	"farmer_id": 1,
	"order_date": "2019-12-31",
	"order_details": [{
		"product_id": 1,
		"line_no": 1,
		"order_qty": 2,
		"line_total": 300
	}]
}'

- Posts a product
- Returns:
{
    "id": 5,
    "message": "order successfully updated",
    "success": true
}
```

## Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return five error types when requests fail:

400: Bad Request

```bash
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

404: Resource Not Found

```bash
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

405: Method Not Allowed

```bash
{
    "success": False,
    "error": 405,
    "message": "method not allowed"
}
```

422: Not Processable

```bash
{
    "success": False,
    "error": 422,
    "message": "unable to process request"
}
```

500: Internal Server Error

```bash
{
    "success": False,
    "error": 500,
    "message": "internal server error"
}
```

## Testing

To run the tests, run

```bash
pytest
```
