# FitSupply API Documentation

Complete API reference for the FitSupply backend.

## Base URL

```
https://pandonyx.pythonanywhere.com/api/v1/
```

## Authentication

All endpoints marked with 🔒 require authentication via JWT Bearer token.

**Header:**

```
Authorization: Bearer <access_token>
```

---

## 📑 Table of Contents

- [Authentication](#authentication-endpoints)
- [Products](#products-endpoints)
- [Categories](#categories-endpoints)
- [Cart](#cart-endpoints)
- [Orders](#orders-endpoints)

---

## Authentication Endpoints

### Register User

**POST** `/register/`

Create a new user account.

**Request Body:**

```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Errors:**

- `400 Bad Request` - Validation errors

---

### Login (Obtain Token)

**POST** `/token/`

Authenticate and receive JWT tokens.

**Request Body:**

```json
{
  "username": "johndoe",
  "password": "SecurePass123!"
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Errors:**

- `401 Unauthorized` - Invalid credentials

---

### Refresh Token

**POST** `/token/refresh/`

Get a new access token using refresh token.

**Request Body:**

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response:** `200 OK`

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### Get User Profile 🔒

**GET** `/user/`

Retrieve authenticated user's profile.

**Response:** `200 OK`

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_staff": false
}
```

---

### Update User Profile 🔒

**PATCH** `/user/`

Update authenticated user's profile.

**Request Body:**

```json
{
  "first_name": "Johnny",
  "last_name": "Doe",
  "email": "johnny@example.com"
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "username": "johndoe",
  "email": "johnny@example.com",
  "first_name": "Johnny",
  "last_name": "Doe",
  "is_staff": false
}
```

---

## Products Endpoints

### List Products

**GET** `/products/`

Get list of all products.

**Query Parameters:**

- `search` (string) - Search products by name or description
- `category` (int) - Filter by category ID
- `is_featured` (boolean) - Filter featured products
- `ordering` (string) - Order by field (price, -price, name, -created_at)

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "category": 1,
    "name": "Whey Protein Isolate",
    "slug": "whey-protein-isolate",
    "description": "Premium whey protein isolate with 90% protein content...",
    "short_description": "Premium whey protein isolate",
    "image": "https://pandonyx.pythonanywhere.com/media/products/whey.jpg",
    "price": "49.99",
    "compare_price": "59.99",
    "sku": "WPI-001",
    "stock_quantity": 150,
    "low_stock_threshold": 10,
    "is_active": true,
    "is_featured": true,
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T15:45:00Z"
  }
]
```

**Examples:**

```
GET /products/?search=protein
GET /products/?category=1
GET /products/?is_featured=true
GET /products/?ordering=-price
```

---

### Get Product Detail

**GET** `/products/{id}/`

Get detailed information about a specific product.

**Path Parameters:**

- `id` (int) - Product ID

**Response:** `200 OK`

```json
{
  "id": 1,
  "category": 1,
  "name": "Whey Protein Isolate",
  "slug": "whey-protein-isolate",
  "description": "Premium whey protein isolate with 90% protein content. Perfect for post-workout recovery and muscle building.",
  "short_description": "Premium whey protein isolate",
  "image": "https://pandonyx.pythonanywhere.com/media/products/whey.jpg",
  "price": "49.99",
  "compare_price": "59.99",
  "sku": "WPI-001",
  "stock_quantity": 150,
  "low_stock_threshold": 10,
  "is_active": true,
  "is_featured": true,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-20T15:45:00Z"
}
```

**Errors:**

- `404 Not Found` - Product does not exist

---

## Categories Endpoints

### List Categories

**GET** `/categories/`

Get list of all product categories.

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "name": "Protein",
    "slug": "protein",
    "description": "High-quality protein supplements for muscle building and recovery",
    "is_active": true,
    "created_at": "2024-01-10T12:00:00Z"
  },
  {
    "id": 2,
    "name": "Pre-Workout",
    "slug": "pre-workout",
    "description": "Energy boosting supplements for intense workouts",
    "is_active": true,
    "created_at": "2024-01-10T12:00:00Z"
  }
]
```

---

### Get Category Detail

**GET** `/categories/{id}/`

Get detailed information about a specific category including its products.

**Path Parameters:**

- `id` (int) - Category ID

**Response:** `200 OK`

```json
{
  "id": 1,
  "name": "Protein",
  "slug": "protein",
  "description": "High-quality protein supplements for muscle building and recovery",
  "is_active": true,
  "created_at": "2024-01-10T12:00:00Z",
  "products": [
    {
      "id": 1,
      "name": "Whey Protein Isolate",
      "price": "49.99",
      "image": "https://pandonyx.pythonanywhere.com/media/products/whey.jpg"
    }
  ]
}
```

---

## Cart Endpoints

### Get Cart 🔒

**GET** `/cart/`

Get authenticated user's shopping cart.

**Response:** `200 OK`

```json
{
  "id": 1,
  "user": 1,
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Whey Protein Isolate",
        "price": "49.99",
        "image": "https://pandonyx.pythonanywhere.com/media/products/whey.jpg",
        "stock_quantity": 150
      },
      "quantity": 2,
      "added_at": "2024-01-20T14:30:00Z"
    }
  ],
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T14:30:00Z"
}
```

---

### Add Item to Cart 🔒

**POST** `/cart/add/`

Add a product to the cart or update quantity if already exists.

**Request Body:**

```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "product": 1,
  "quantity": 2,
  "added_at": "2024-01-20T14:30:00Z"
}
```

**Errors:**

- `400 Bad Request` - Invalid product_id or quantity
- `404 Not Found` - Product does not exist

---

### Update Cart Item 🔒

**PATCH** `/cart/items/{id}/`

Update quantity of a cart item.

**Path Parameters:**

- `id` (int) - Cart item ID

**Request Body:**

```json
{
  "quantity": 3
}
```

**Response:** `200 OK`

```json
{
  "id": 1,
  "product": 1,
  "quantity": 3,
  "added_at": "2024-01-20T14:30:00Z"
}
```

---

### Remove Cart Item 🔒

**DELETE** `/cart/items/{id}/`

Remove an item from the cart.

**Path Parameters:**

- `id` (int) - Cart item ID

**Response:** `204 No Content`

---

### Clear Cart 🔒

**DELETE** `/cart/clear/`

Remove all items from the cart.

**Response:** `204 No Content`

---

## Orders Endpoints

### List Orders 🔒

**GET** `/orders/`

Get all orders for authenticated user.

**Response:** `200 OK`

```json
[
  {
    "id": 1,
    "order_number": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
    "status": "delivered",
    "total_amount": "149.97",
    "shipping_address": "123 Main St, City, State 12345",
    "billing_address": "123 Main St, City, State 12345",
    "payment_method": "credit_card",
    "created_at": "2024-01-20T10:00:00Z",
    "updated_at": "2024-01-25T16:30:00Z",
    "items": [
      {
        "id": 1,
        "product": {
          "id": 1,
          "name": "Whey Protein Isolate",
          "image": "https://pandonyx.pythonanywhere.com/media/products/whey.jpg"
        },
        "quantity": 3,
        "price_at_time": "49.99",
        "subtotal": "149.97"
      }
    ]
  }
]
```

---

### Get Order Detail 🔒

**GET** `/orders/{id}/`

Get detailed information about a specific order.

**Path Parameters:**

- `id` (int) - Order ID

**Response:** `200 OK`

```json
{
  "id": 1,
  "order_number": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
  "user": 1,
  "status": "delivered",
  "total_amount": "149.97",
  "shipping_address": "123 Main St, City, State 12345",
  "billing_address": "123 Main St, City, State 12345",
  "payment_method": "credit_card",
  "notes": "Please deliver after 5 PM",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-25T16:30:00Z",
  "items": [
    {
      "id": 1,
      "product": {
        "id": 1,
        "name": "Whey Protein Isolate",
        "sku": "WPI-001",
        "image": "https://pandonyx.pythonanywhere.com/media/products/whey.jpg"
      },
      "quantity": 3,
      "price_at_time": "49.99",
      "subtotal": "149.97"
    }
  ]
}
```

**Errors:**

- `404 Not Found` - Order does not exist or doesn't belong to user

---

### Create Order 🔒

**POST** `/orders/`

Create a new order from cart items.

**Request Body:**

```json
{
  "shipping_address": "123 Main St, City, State 12345",
  "billing_address": "123 Main St, City, State 12345",
  "payment_method": "credit_card",
  "notes": "Please deliver after 5 PM"
}
```

**Response:** `201 Created`

```json
{
  "id": 1,
  "order_number": "a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6",
  "user": 1,
  "status": "pending",
  "total_amount": "149.97",
  "shipping_address": "123 Main St, City, State 12345",
  "billing_address": "123 Main St, City, State 12345",
  "payment_method": "credit_card",
  "notes": "Please deliver after 5 PM",
  "created_at": "2024-01-20T10:00:00Z",
  "updated_at": "2024-01-20T10:00:00Z",
  "items": [
    {
      "id": 1,
      "product": 1,
      "quantity": 3,
      "price_at_time": "49.99",
      "subtotal": "149.97"
    }
  ]
}
```

**Errors:**

- `400 Bad Request` - Cart is empty or validation errors

---

## Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `204 No Content` - Request successful, no content to return
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Error Response Format

```json
{
  "detail": "Error message here"
}
```

Or for validation errors:

```json
{
  "field_name": ["Error message for this field"]
}
```

## Rate Limiting

No rate limiting currently implemented.

## Pagination

Endpoints that return lists use Django REST Framework's pagination:

```json
{
  "count": 100,
  "next": "https://pandonyx.pythonanywhere.com/api/v1/products/?page=2",
  "previous": null,
  "results": [...]
}
```

## CORS

CORS is enabled for all origins in development. Production restricts to approved domains.

## Testing with cURL

### Register

```bash
curl -X POST https://pandonyx.pythonanywhere.com/api/v1/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"Test123!","first_name":"Test","last_name":"User"}'
```

### Login

```bash
curl -X POST https://pandonyx.pythonanywhere.com/api/v1/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test123!"}'
```

### Get Products (No Auth Required)

```bash
curl https://pandonyx.pythonanywhere.com/api/v1/products/
```

### Get Cart (Auth Required)

```bash
curl https://pandonyx.pythonanywhere.com/api/v1/cart/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
