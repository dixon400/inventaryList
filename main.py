from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-16508.c16.us-east-1-3.ec2.cloud.redislabs.com",
    port=16508,
    password="3AkXZYVxuhyBGf3ffavA6jGhw9LfHcfJ",
    decode_responses=True
)

class Product(HashModel):
    name: str
    price: int
    quantity: int

    class Meta:
        database = redis


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }

@app.post("/products")
def create(product: Product):
    return product.save()

@app.get("/product/{pk}")
def get(pk: str):
    return Product.get(pk)

@app.delete("/product/{pk}")
def dekete(pk: str):
    return Product.delete(pk)