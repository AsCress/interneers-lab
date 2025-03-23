# Interneers Lab

Welcome to the **Interneers Lab 2025** repository! This serves as a repository for learning and experimenting with:
- **Django** (Python)
- **React**  (with TypeScript)
- **MongoDB** (via Docker Compose)
- Development environment in **VSCode** (recommended)

---

## Table of Contents

1. [Introduction to Python & Django](#introduction-to-python--django)

---

## Introduction to Python & Django

### Week 1

1. **Building a simple `GET` API**:

    - Built a `GET` API (`hello_name`) that returns a **greeting message** alongwith **age**.

    - Uses query parameters _name_ and _age_.

    - Performs simple **formatting** on the _name_ and validates the _age_ to be a number before returning a response. 

    - Responds with meaningful **error messages** and appropriate **error codes** on validation failures.

   #### **Test Scenarios**: 
   | **Test Case** | **Request URL** | **Expected Response** | **Status Code** | **Notes** |
   |--------------|----------------|----------------------|---------------|----------|
   | ✅ Default request (no params) | `/hello/` | `{ "message": "Hello, World!" }` | `200 OK` | Should return "World" when no name is provided |
   | ✅ Valid name only | `/hello/?name=Anashuman` | `{ "message": "Hello, Anashuman!" }` | `200 OK` | Handles a single valid name |
   | ✅ Valid name with spaces | `/hello/?name=  Anashuman   ` | `{ "message": "Hello, Anashuman!" }` | `200 OK` | Extra spaces should be removed |
   | ✅ Valid name with multiple spaces | `/hello/?name=   Anashuman   Singh   ` | `{ "message": "Hello, Anashuman Singh!" }` | `200 OK` | Multiple spaces should be reduced to one |
   | ✅ Valid age only | `/hello/?age=20` | `{ "message": "Hello, World!", "age": 20 }` | `200 OK` | Should return "World" when name is missing |
   | ✅ Valid name & age | `/hello/?name=Anashuman&age=20` | `{ "message": "Hello, Anashuman!", "age": 20 }` | `200 OK` | Normal case with both parameters |
   | ❌ Invalid age (non-numeric) | `/hello/?name=Anashuman&age=abc` | `{ "error": "Age must be a valid number" }` | `400 Bad Request` | Non-numeric age should return an error |
   | ❌ Invalid age (special characters) | `/hello/?name=Anashuman&age=25!` | `{ "error": "Age must be a valid number" }` | `400 Bad Request` | Special characters in age should fail |
   | ✅ Empty age (ignored) | `/hello/?name=Anashuman&age=` | `{ "message": "Hello, Anashuman!" }` | `200 OK` | Empty age should be ignored, not cause an error |
   | ✅ Empty name (defaults to World) | `/hello/?name=&age=20` | `{ "message": "Hello, World!", "age": 20 }` | `200 OK` | Name defaults to "World" when empty |
   | ✅ Name with special characters | `/hello/?name=Anashuman@` | `{ "message": "Hello, Anashuman@!" }` | `200 OK` | Special characters in name should be allowed |
   | ✅ Age with spaces | `/hello/?name=Anashuman&age=   20  ` | `{ "message": "Hello, Anashuman!", "age": 20 }` | `200 OK` | Extra spaces in age should be ignored |
   | ✅ Name with numbers | `/hello/?name=Anashuman123` | `{ "message": "Hello, Anashuman123!" }` | `200 OK` | Numbers in name should be allowed |

   ---

### Week 2

1. **Moving forward with DRF**:
   - Created a `Product` model with basic information around name, description, category, price, brand and quantity.
   - Built sophisticated APIs for **creating, updating (including deletion) and fetching** products using **Class-Based Views**.
   - Tested using a **SQLite database** as well as **in-memory storage**.
   - Added **pagination** to the fetch products API.

2. **Testing the API**:
   #### Create a Product
   **cURL**
   ```bash
   curl -X POST http://127.0.0.1:8001/products/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Laptop", "description": "Gaming laptop", "category": "Electronics", "price": 1200, "brand": "DELL", "quantity": 10}'
   ```

   **Response** `201 Created`
   ```
   {
    "id": 1,
    "name": "Laptop",
    "description": "Gaming laptop",
    "category": "Electronics",
    "price": "90000.00",
    "brand": "DELL",
    "quantity": 10
   }
   ```

   #### Update a Product
   **cURL**
   ```bash
   curl -X PUT http://127.0.0.1:8001/products/{id}/ \
     -H "Content-Type: application/json" \
     -d '{"price": 80000}'
   ```

   **Response** `200 OK`
   ```
   {
    "name": "Laptop",
    "description": "Gaming laptop",
    "category": "Electronics",
    "price": 80000.0,
    "brand": "DELL",
    "quantity": 10,
    "id": 1
   }
   ```

   #### Fetch a Product
   **cURL**
   ```bash
   curl -X GET http://127.0.0.1:8001/products/{id}/
   ```

   **Response** `200 OK`
   ```
   {
    "id": 1,
    "name": "Laptop",
    "description": "Gaming laptop",
    "category": "Electronics",
    "price": "80000.00",
    "brand": "DELL",
    "quantity": 10
   }
   ```

   #### Fetch all Products
   **cURL**
   ```bash
   curl -X GET http://127.0.0.1:8001/products/
   ```

   **Response** `200 OK`
   ```
   {
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
         {
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "price": 80000.0,
            "brand": "DELL",
            "quantity": 10,
            "id": 1
         }
      ]
   }  
   ```

   #### Delete a Product
   **cURL**
   ```bash
   curl -X DELETE http://127.0.0.1:8001/products/{id}/
   ```

   **Response** `204 No Content`
   ```
   {
    "message": "Product deleted successfully"
   }
   ```

   #### Testing Pagination
   **cURL**
   ```bash
   curl -X GET http://127.0.0.1:8001/products?page=1&page_size=1
   ```

   **Response**
   ```
   {
    "count": 2,
    "next": "http://127.0.0.1:8001/products/?page=2&page_size=1",
    "previous": null,
    "results": [
         {
            "name": "Laptop",
            "description": "Gaming laptop",
            "category": "Electronics",
            "price": 80000.0,
            "brand": "DELL",
            "quantity": 10,
            "id": 1
         }
      ]
   }
   ```
3. **Validations**:

   | **Scenario**                           | **Request URL** | **Expected Response** | **Status Code** |
   |-----------------------------------------|-----------------|----------------------|----------------|
   | ✅ **Create a Product (Valid)** | `POST /products/` <br> Body: `{"name": "Laptop", "description": "Gaming laptop", "category": "Electronics", "price": 90000, "brand": "ASUS", "quantity": 20}` | `{"id":3,"name":"Laptop","description":"Gaming laptop","category":"Electronics","price":"90000.00","brand":"ASUS","quantity":20}` | `201 Created` |
   | ❌ **Create a Product (Missing Fields)** | `POST /products/` <br> Body: `{ "name": "Tablet" }` | `{"category":["This field is required."],"price":["This field is required."],"brand":["This field is required."]}` | `400 Bad Request` |
   | ✅ **Fetch a Single Product (Exists)** | `GET /products/{id}/` | `{"id":1,"name":"Laptop","description":"Gaming laptop","category":"Electronics","price":"80000.00","brand":"DELL","quantity":10}` | `200 OK` |
   | ❌ **Fetch a Single Product (Not Found)** | `GET /products/{id}/` | `{"detail":"Product does not exist"}` | `404 Not Found` |
   | ✅ **Fetch All Products (With Pagination)** | `GET /products/?page=1&page_size=1` | `{ "count": 3, "next": "/products/?page=2", "previous": null, "results": [...] }` | `200 OK` |
   | ✅ **Update a Product (Valid Update)** | `PUT /products/{id}/` <br> Body: `{"price":100000}` | `{"name":"Laptop","description":"Gaming laptop","category":"Electronics","price":100000.0,"brand":"DELL","quantity":10,"id":1}` | `200 OK` |
   | ❌ **Update a Product (Invalid ID)** | `PUT /products/{id}/` <br> Body: `{"price":100000}` | `{"detail":"Product does not exist"}` | `404 Not Found` |
   | ✅ **Delete a Product (Valid)** | `DELETE /products/{id}/` | `{"message":"Product deleted successfully"}` | `204 No Content` |
   | ❌ **Delete a Product (Invalid ID)** | `DELETE /products/{id}/` | `{"detail":"Product does not exist"}` | `404 Not Found` |

---
