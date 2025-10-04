# FitSupply Backend API

Welcome to the backend API for FitSupply, an e-commerce platform for fitness products. This service is built with Django and Django REST Framework, providing a robust, scalable, and secure foundation for the application.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Setup](#project-setup)
- [Environment Variables](#environment-variables)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [Authentication](#authentication)
  - [Products](#products)
  - [Orders](#orders)
  - [Analytics](#analytics)

---

## Features

- **JWT Authentication**: Secure user authentication and authorization using `simple-jwt`.
- **Product Management**: Full CRUD (Create, Read, Update, Delete) operations for products and categories.
- **Order Processing**: Create and view customer orders.
- **User Management**: Custom user model for registration and profile management.
- **Sales Analytics**: Endpoints for retrieving sales and performance data.
- **CORS Ready**: Configured to accept requests from a frontend application.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: SQLite3 (development)
- **Authentication**: djangorestframework-simplejwt
- **Environment Variables**: python-decouple
- **Static Files**: WhiteNoise
- **Deployment**: Ready for services like PythonAnywhere.

---

## Project Setup

Follow these steps to get the development environment up and running.

### 1. Prerequisites

- Python 3.10+
- Pip and Virtualenv
- Git
- PostgreSQL (for production-like setup)

### 2. Clone the Repository

```bash
git clone https://github.com/Pandonyx/fitsupply-backend
cd fitsupply-backend
```

### 3. Set Up Virtual Environment

Create and activate a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

Install all the required packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the `fitsupply-backend` directory (where `manage.py` is located). See the Environment Variables section for details on what to include.

### 6. Apply Database Migrations

Run the following command to create the database tables.

```bash
python manage.py migrate
```

### 7. Create a Superuser

This allows you to access the Django admin panel.

```bash
python manage.py createsuperuser
```

---

## Environment Variables

Create a `.env` file in the root of the `fitsupply-backend` directory and add the following variables. For development, you can use the provided defaults.

```ini
# .env

# SECURITY WARNING: a strong, unique key is required for production
SECRET_KEY=django-insecure-ob@=c$!!$8!i-ym$50tit2m^=nd=ypz$sdxk23hny658_kn$8p

# Set to False in production
DEBUG=True

# For production, use your actual database URL
# Example: DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
# For development, you can omit this to use the default SQLite database
DATABASE_URL=
```

---

## Running the Server

Start the development server with the following command:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

---

## API Endpoints

All endpoints are prefixed with `/api/`. Authentication is required for most endpoints, which is done by providing a JWT in the `Authorization` header.

**Header Format**: `Authorization: Bearer <your_access_token>`

### Authentication

Base URL: `/api/accounts/`

| Method | Endpoint         | Description                                      | Authentication |
| :----- | :--------------- | :----------------------------------------------- | :------------- |
| `POST` | `register/`      | Create a new user account.                       | None           |
| `POST` | `token/`         | Obtain a new JWT access and refresh token pair.  | None           |
| `POST` | `token/refresh/` | Obtain a new access token using a refresh token. | None           |
| `POST` | `logout/`        | (If implemented) Blacklists a refresh token.     | Required       |

**Example: Obtain Token**

`POST /api/accounts/token/`

```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### Products

Base URL: `/api/products/`

| Method   | Endpoint         | Description                           | Authentication |
| :------- | :--------------- | :------------------------------------ | :------------- |
| `GET`    | `products/`      | Get a list of all products.           | Optional       |
| `POST`   | `products/`      | Create a new product.                 | Admin Only     |
| `GET`    | `products/<id>/` | Get details of a specific product.    | Optional       |
| `PUT`    | `products/<id>/` | Update a product.                     | Admin Only     |
| `DELETE` | `products/<id>/` | Delete a product.                     | Admin Only     |
| `GET`    | `categories/`    | Get a list of all product categories. | Optional       |

### Orders

Base URL: `/api/orders/`

| Method | Endpoint       | Description                                    | Authentication   |
| :----- | :------------- | :--------------------------------------------- | :--------------- |
| `GET`  | `orders/`      | Get a list of the authenticated user's orders. | Required         |
| `POST` | `orders/`      | Create a new order.                            | Required         |
| `GET`  | `orders/<id>/` | Get details of a specific order.               | Required (Owner) |

### Analytics

Base URL: `/api/analytics/`

| Method | Endpoint        | Description                                 | Authentication |
| :----- | :-------------- | :------------------------------------------ | :------------- |
| `GET`  | `sales-report/` | Get a report of sales data (e.g., monthly). | Admin Only     |
