# HotelService
# 🏨 Hotel Booking Service

Django + Django REST project for rent hotels

| Stack |
|-------|--------|
| Python | 3.11 + |
| Django | 5.2 |
| Django REST Framework | 3.15 |
| SQL Lite| 14 + |
| Bootstrap 5 (UI) | CDN |
| Simple JWT | 5.3 |


| Public hotel catalog |

- filtering by city, price, dates, and number of guests

- display of available rooms with thumbnails

| Hotel detail page |

- list of available rooms for selected dates

- average rating and user reviews

| Booking |

- date overlap check

- user dashboard with booking history

- Hotel reviews (1 review per user)

| JWT authentication for API + regular sessions for HTML |

| Admin panel for managing hotels, rooms, and bookings |

| DRF API (version v1) |

| Hotels /api/hotels/ |

| Rooms /api/rooms/ |

| Bookings /api/bookings/ |

| Reviews /api/hotel-reviews/ |

---

# 1. Clone the repository
git clone https://github.com/your-org/hotel-service.git
cd hotel-service

# 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\\Scripts\\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Environment setup
cp .env.example .env              # and configure your secrets / DB URL
export $(cat .env | xargs)        # helper for Linux/macOS

# 5. Apply migrations and create superuser
python manage.py migrate
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver

# 7. (Optional) Run tests
pytest  # or python manage.py test

| App Structure |

HotelService/   

* **HotelService/**
  * **Booking/**
  * **Hotel/**
  * **Customer/**
  * **templates/**
    * **hotels/**
      * `hotel-detail.html`
      * `hotel-list.html`
      * `room-detail.html`
    * **bookings/**
      * `booking-detail.html`
      * `booking-form.html`
    * **users/**
      * `login.html`, `logout.html`, `register.html`
      * `profile.html`, `profile-edit.html`
      * `password_change.html`, `password_change_done.html`
  * `base.html`
  * `api.py`, `serializers.py`, `urls.py`

