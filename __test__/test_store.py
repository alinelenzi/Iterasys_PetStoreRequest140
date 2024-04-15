import json
import pytest
import requests


order_id = 1
petId = 112092001
order_quantity = 1
order_shipDate = '2024-04-13T17:33:48.524Z'
order_status = 'placed'
order_complete = True

url = 'https://petstore.swagger.io/v2/store/order'
headers = {'Content-Type': 'application/json'}

def test_post_store():

    store = open('./fixtures/json/store1.json')
    data = json.loads(store.read())
    
    response = requests.post(
        url=url,
        headers=headers,
        data = json.dumps(data),
        timeout=5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == order_id
    assert response_body['petId'] == petId
    assert response_body['quantity'] == order_quantity
    assert response_body['status'] == order_status
    assert response_body['complete'] == order_complete

def test_get_store():
    response = requests.get(
        url = f'{url}/{order_id}',
        headers=headers,
        timeout=5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == order_id
    assert response_body['petId'] == petId
    assert response_body['quantity'] == order_quantity
    assert response_body['status'] == order_status
    assert response_body['complete'] == order_complete

def test_delete_store():
    response = requests.delete(
        url = f'{url}/{order_id}',
        headers=headers,
        timeout=5
    )

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(order_id)

    