# Coderr Backend

A REST API backend for a freelancer marketplace platform built with Django and Django REST Framework.

## Requirements

- Python 3.12+
- pip

## Setup

**1. Clone the repository**

```bash
git clone <repository-url>
cd Coderr
```

**2. Create and activate a virtual environment**

```bash
python -m venv env
source env/bin/activate  # Mac/Linux
env\Scripts\activate     # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Run migrations**

Since migration files are excluded from version control, you need to create and apply them:

```bash
python manage.py makemigrations
python manage.py migrate
```

**5. Create a superuser (optional)**

```bash
python manage.py createsuperuser
```

**6. Start the development server**

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000/`.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/api/registration/` | Register a new user | No |
| POST | `/api/login/` | Login and receive token | No |

### Profiles

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET, PATCH | `/api/profile/<id>/` | Get or update a profile | Yes |
| GET | `/api/profiles/business/` | List all business profiles | Yes |
| GET | `/api/profiles/customer/` | List all customer profiles | Yes |

### Offers

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET, POST | `/api/offers/` | List all offers or create one | Yes |
| GET, PATCH, DELETE | `/api/offers/<id>/` | Retrieve, update or delete an offer | Yes |
| GET | `/api/offerdetails/<id>/` | Get details of a specific offer | Yes |

### Orders

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET, POST | `/api/orders/` | List all orders or create one | Yes |
| PATCH, DELETE | `/api/orders/<id>/` | Update or delete an order | Yes |
| GET | `/api/order-count/<id>/` | Get in-progress order count for a business user | Yes |
| GET | `/api/completed-order-count/<id>/` | Get completed order count for a business user | Yes |

### Reviews

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET, POST | `/api/reviews/` | List all reviews or create one | Yes |
| GET, PATCH, DELETE | `/api/reviews/<id>/` | Retrieve, update or delete a review | Yes |

### General

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| GET | `/api/base-info/` | Platform statistics (review count, average rating, business profiles, offers) | No |

---

## User Types

The platform has two user types:

- **customer** — can place orders and write reviews
- **business** — can create offers and receive orders and reviews

---

## Admin

The Django admin panel is available at `/admin/`.
