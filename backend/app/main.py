"""Project Phoenix - Product API (Day 1 starter).

A deliberately small FastAPI service so students can focus on
Kubernetes and GitOps, not application code.
Products are held in memory for Day 1; a real database is added later.
"""
import os
import socket

from fastapi import FastAPI, HTTPException

APP_VERSION = os.getenv("APP_VERSION", "v1.0.0")
APP_ENV = os.getenv("APP_ENV", "local")

app = FastAPI(title="Phoenix Product API", version=APP_VERSION)

PRODUCTS = [
    {"id": 1, "name": "Phoenix Hoodie", "price": 1499, "category": "Apparel", "stock": 25},
    {"id": 2, "name": "GitOps Coffee Mug", "price": 399, "category": "Kitchen", "stock": 120},
    {"id": 3, "name": "Kubernetes Sticker Pack", "price": 199, "category": "Accessories", "stock": 300},
    {"id": 4, "name": "Mechanical Keyboard", "price": 4999, "category": "Electronics", "stock": 12},
    {"id": 5, "name": "Noise-Cancelling Headphones", "price": 7999, "category": "Electronics", "stock": 8},
    {"id": 6, "name": "Developer Notebook", "price": 299, "category": "Stationery", "stock": 80},
]


@app.get("/healthz")
def healthz():
    """Liveness probe: the process is up."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    """Readiness probe: the app can serve traffic."""
    return {"status": "ready"}


@app.get("/api/info")
def info():
    """Shows which version and which pod answered - handy for GitOps demos."""
    return {
        "service": "product-api",
        "version": APP_VERSION,
        "environment": APP_ENV,
        "pod": socket.gethostname(),
    }


@app.get("/api/products")
def list_products():
    return PRODUCTS


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")
