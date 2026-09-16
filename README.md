# MOOMEEN PRODUCTS

## Siddha & Natural Healthcare E-Commerce Website

MOOMEEN PRODUCTS is a Django-based e-commerce website designed for selling Siddha, herbal, and natural healthcare products online.

The website provides a simple and user-friendly shopping experience for customers along with a secure admin dashboard for managing products, orders, customers, and reviews.

---

## Features

### Customer Features

- User Registration and Login
- Browse Products
- Product Details
- Product Search
- Product Reviews
- Wishlist
- Shopping Cart
- Checkout
- Cash on Delivery
- Order Confirmation
- My Orders
- Order Tracking
- Customer Profile
- Address Management
- Contact / Enquiry

### Admin Features

- Secure Admin Access
- Admin Dashboard
- Product Management
- Order Management
- Customer Management
- Review Management
- Product Stock Management
- Order Status Management
- Customer Account Management

---

## Technology Stack

### Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

### Backend
- Python
- Django

### Database
- PostgreSQL

### Development Tools
- Visual Studio Code
- Git
- GitHub

---

## Order Tracking

Customers can track their orders through the following stages:

```text
Placed
   ↓
Confirmed
   ↓
Packed
   ↓
Shipped
   ↓
Out for Delivery
   ↓
Delivered

## Deployment

Install dependencies, set the production environment variables, and run:

```text
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn moomeen.wsgi:application
```

Required production variables include `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`,
`DJANGO_CSRF_TRUSTED_ORIGINS`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`,
`POSTGRES_HOST`, and `POSTGRES_PORT`. Keep `DJANGO_DEBUG` unset or set it to `false`.
