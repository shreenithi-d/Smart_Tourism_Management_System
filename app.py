#=========================================================
# Smart Tourism Management System
# ==========================================================

import os
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database import (
    db,
    User,
    Destination,
    Booking,
    Favorite
)

# ==========================================================
# APP CONFIGURATION
# ==========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "smart-tourism-secret-key"
)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

db_path = os.path.join(
    BASE_DIR,
    "instance",
    "tourism.db"
)

os.makedirs(
    os.path.join(BASE_DIR, "instance"),
    exist_ok=True
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{db_path}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ==========================================================
# LOGIN DECORATORS
# ==========================================================

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login to continue.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        return f(*args, **kwargs)

    return decorated_function


def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        if session.get("role") != "admin":

            flash(
                "Admin access required.",
                "danger"
            )

            return redirect(
                url_for("destinations")
            )

        return f(*args, **kwargs)

    return decorated_function


# ==========================================================
# CURRENT USER HELPER
# ==========================================================

def current_user():

    if "user_id" not in session:
        return None

    return User.query.get(
        session["user_id"]
    )


# ==========================================================
# DESTINATION SEED DATA
# ==========================================================

DESTINATIONS = [

    {
        "name": "Ooty",
        "location": "Tamil Nadu, India",
        "category": "Hill Station",
        "price": 12000,
        "duration": "3 Days / 2 Nights",
        "rating": 4.8,
        "image_url":
        "https://images.unsplash.com/photo-1506744038136-46273834b3fb",
        "description":
        "Ooty is one of India's most famous hill stations known for tea gardens, cool weather, lakes, botanical gardens, and scenic mountain views."
    },

    {
        "name": "Munnar",
        "location": "Kerala, India",
        "category": "Nature",
        "price": 14000,
        "duration": "4 Days / 3 Nights",
        "rating": 4.9,
        "image_url":
        "https://hblimg.mmtcdn.com/content/hubble/img/destimg/mmt/destination/m_Munnar_main_tv_destination_img_1_l_630_946.jpg",
        "description":
        "Munnar is a breathtaking destination famous for rolling tea plantations, misty mountains, waterfalls, and wildlife."
    },

    {
        "name": "Kodaikanal",
        "location": "Tamil Nadu, India",
        "category": "Hill Station",
        "price": 11000,
        "duration": "3 Days / 2 Nights",
        "rating": 4.7,
        "image_url":
        "https://images.unsplash.com/photo-1469474968028-56623f02e42e",
        "description":
        "Kodaikanal offers serene lakes, pine forests, valleys, waterfalls, and pleasant weather throughout the year."
    },

    {
        "name": "Goa",
        "location": "Goa, India",
        "category": "Beach",
        "price": 18000,
        "duration": "5 Days / 4 Nights",
        "rating": 4.8,
        "image_url":
        "https://images.unsplash.com/photo-1519046904884-53103b34b206",
        "description":
        "Goa is India's beach paradise featuring nightlife, water sports, heritage churches, seafood, and vibrant culture."
    },

    {
        "name": "Jaipur",
        "location": "Rajasthan, India",
        "category": "Heritage",
        "price": 15000,
        "duration": "4 Days / 3 Nights",
        "rating": 4.7,
        "image_url":
        "https://s7ap1.scene7.com/is/image/incredibleindia/jal-mahal-jaipur-rajasthan-1-attr-hero?qlt=82&ts=1742162446740",
        "description":
        "Jaipur, the Pink City, showcases magnificent forts, palaces, royal heritage, colorful markets, and rich traditions."
    },

    {
        "name": "Manali",
        "location": "Himachal Pradesh, India",
        "category": "Adventure",
        "price": 17000,
        "duration": "5 Days / 4 Nights",
        "rating": 4.9,
        "image_url":
        "https://tripstorz.com/_astro/houses-surrounded-by-green-trees-in-manali-during-daytime.DAktkgeM_1Vbxjy.avif",
        "description":
        "Manali is renowned for snow-capped mountains, adventure sports, trekking routes, and picturesque valleys."
    },

    {
        "name": "Kashmir",
        "location": "Jammu & Kashmir, India",
        "category": "Nature",
        "price": 22000,
        "duration": "6 Days / 5 Nights",
        "rating": 5.0,
        "image_url":
        "https://images.unsplash.com/photo-1501785888041-af3ef285b470",
        "description":
        "Kashmir is known as Paradise on Earth with pristine lakes, snow peaks, gardens, and breathtaking landscapes."
    },

    {
        "name": "Andaman Islands",
        "location": "Andaman & Nicobar, India",
        "category": "Island",
        "price": 28000,
        "duration": "6 Days / 5 Nights",
        "rating": 4.9,
        "image_url":
        "https://images.unsplash.com/photo-1500375592092-40eb2168fd21",
        "description":
        "Andaman offers turquoise waters, coral reefs, scuba diving, beaches, and tropical island adventures."
    },

    {
        "name": "Dubai",
        "location": "United Arab Emirates",
        "category": "Luxury",
        "price": 65000,
        "duration": "5 Days / 4 Nights",
        "rating": 4.9,
        "image_url":
        "https://images.unsplash.com/photo-1512453979798-5ea266f8880c",
        "description":
        "Dubai features luxury shopping, iconic skyscrapers, desert safaris, beaches, and world-class entertainment."
    },

    {
        "name": "Bali",
        "location": "Indonesia",
        "category": "Beach",
        "price": 55000,
        "duration": "6 Days / 5 Nights",
        "rating": 4.9,
        "image_url":
        "https://images.unsplash.com/photo-1537996194471-e657df975ab4",
        "description":
        "Bali is famous for temples, beaches, rice terraces, luxury resorts, and tropical beauty."
    },

    {
        "name": "Singapore",
        "location": "Singapore",
        "category": "City",
        "price": 70000,
        "duration": "5 Days / 4 Nights",
        "rating": 4.8,
        "image_url":
        "https://images.unsplash.com/photo-1525625293386-3f8f99389edd",
        "description":
        "Singapore offers futuristic attractions, Marina Bay Sands, Gardens by the Bay, and vibrant urban experiences."
    },

    {
        "name": "Switzerland",
        "location": "Europe",
        "category": "Luxury",
        "price": 125000,
        "duration": "7 Days / 6 Nights",
        "rating": 5.0,
        "image_url":
        "https://images.unsplash.com/photo-1500534314209-a25ddb2bd429",
        "description":
        "Switzerland is known for alpine scenery, luxury tourism, skiing, lakes, and charming mountain villages."
    }

]

# ==========================================================
# INITIAL DATABASE SETUP
# ==========================================================

def initialize_database():

    db.create_all()

    admin = User.query.filter_by(
        email="admin@tourism.com"
    ).first()

    if not admin:

        admin = User(
            name="System Admin",
            email="admin@tourism.com",
            password=generate_password_hash(
                "admin123"
            ),
            role="admin"
        )

        db.session.add(admin)

    if Destination.query.count() == 0:

        for item in DESTINATIONS:

            destination = Destination(
                name=item["name"],
                location=item["location"],
                category=item["category"],
                price=item["price"],
                duration=item["duration"],
                rating=item["rating"],
                description=item["description"],
                image_url=item["image_url"]
            )

            db.session.add(destination)

    db.session.commit()

# ==========================================================
# AUTHENTICATION ROUTES
# ==========================================================

@app.route("/")
def home():
    return redirect(url_for("destinations"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("register")
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already registered.",
                "warning"
            )

            return redirect(
                url_for("register")
            )

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password),
            role="traveler"
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful. Please login.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            flash(
                "Invalid email or password.",
                "danger"
            )

            return redirect(
                url_for("login")
            )

        if not check_password_hash(
            user.password,
            password
        ):

            flash(
                "Invalid email or password.",
                "danger"
            )

            return redirect(
                url_for("login")
            )

        session["user_id"] = user.id
        session["role"] = user.role
        session["name"] = user.name

        flash(
            f"Welcome back, {user.name}!",
            "success"
        )

        if user.role == "admin":

            return redirect(
                url_for("admin_dashboard")
            )

        return redirect(
            url_for("user_dashboard")
        )

    return render_template(
        "login.html"
    )


@app.route("/logout")
def logout():

    session.clear()

    flash(
        "Logged out successfully.",
        "info"
    )

    return redirect(
        url_for("login")
    )


# ==========================================================
# DESTINATIONS
# ==========================================================

@app.route("/destinations")
def destinations():

    search = request.args.get(
        "search",
        ""
    )

    if search:

        destination_list = Destination.query.filter(
            Destination.name.ilike(
                f"%{search}%"
            )
        ).all()

    else:

        destination_list = Destination.query.order_by(
            Destination.rating.desc()
        ).all()

    return render_template(
        "destinations.html",
        destinations=destination_list,
        search=search
    )


@app.route(
    "/destination/<int:destination_id>",
    methods=["GET", "POST"]
)
def destination_details(destination_id):

    destination = Destination.query.get_or_404(
        destination_id
    )

    if request.method == "POST":

        if "user_id" not in session:

            flash(
                "Please login first.",
                "warning"
            )

            return redirect(
                url_for("login")
            )

        travel_date = request.form.get(
            "travel_date"
        )

        people = int(
            request.form.get(
                "people",
                1
            )
        )

        booking = Booking(
            user_id=session["user_id"],
            destination_id=destination.id,
            travel_date=travel_date,
            people=people,
            total_price=(
                destination.price * people
            ),
            status="Confirmed"
        )

        db.session.add(booking)
        db.session.commit()

        flash(
            "Trip booked successfully.",
            "success"
        )

        return redirect(
            url_for("my_bookings")
        )

    favorite_exists = False

    if "user_id" in session:

        favorite_exists = Favorite.query.filter_by(
            user_id=session["user_id"],
            destination_id=destination.id
        ).first() is not None

    return render_template(
        "destination_details.html",
        destination=destination,
        favorite_exists=favorite_exists
    )


# ==========================================================
# FAVORITES
# ==========================================================

@app.route(
    "/add-favorite/<int:destination_id>"
)
@login_required
def add_favorite(destination_id):

    existing = Favorite.query.filter_by(
        user_id=session["user_id"],
        destination_id=destination_id
    ).first()

    if not existing:

        favorite = Favorite(
            user_id=session["user_id"],
            destination_id=destination_id
        )

        db.session.add(favorite)
        db.session.commit()

        flash(
            "Destination added to favorites.",
            "success"
        )

    else:

        flash(
            "Already in favorites.",
            "warning"
        )

    return redirect(
        url_for(
            "destination_details",
            destination_id=destination_id
        )
    )


@app.route(
    "/remove-favorite/<int:destination_id>"
)
@login_required
def remove_favorite(destination_id):

    favorite = Favorite.query.filter_by(
        user_id=session["user_id"],
        destination_id=destination_id
    ).first()

    if favorite:

        db.session.delete(favorite)
        db.session.commit()

    flash(
        "Removed from favorites.",
        "info"
    )

    return redirect(
        url_for("favorites")
    )


@app.route("/favorites")
@login_required
def favorites():

    favorite_list = Favorite.query.filter_by(
        user_id=session["user_id"]
    ).all()

    return render_template(
        "favorites.html",
        favorites=favorite_list
    )


# ==========================================================
# USER DASHBOARD
# ==========================================================

@app.route("/user-dashboard")
@login_required
def user_dashboard():

    user = current_user()

    bookings = Booking.query.filter_by(
        user_id=user.id
    ).all()

    favorites_count = Favorite.query.filter_by(
        user_id=user.id
    ).count()

    total_spent = sum(
        booking.total_price
        for booking in bookings
    )

    recent_bookings = Booking.query.filter_by(
        user_id=user.id
    ).order_by(
        Booking.id.desc()
    ).limit(5).all()

    return render_template(
        "user_dashboard.html",
        user=user,
        total_bookings=len(bookings),
        total_favorites=favorites_count,
        total_spent=total_spent,
        recent_bookings=recent_bookings
    )


@app.route(
    "/my-bookings"
)
@login_required
def my_bookings():

    bookings = Booking.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "my_bookings.html",
        bookings=bookings
    )


@app.route(
    "/profile",
    methods=["GET", "POST"]
)
@login_required
def profile():

    user = current_user()

    if request.method == "POST":

        user.name = request.form.get(
            "name"
        )

        user.email = request.form.get(
            "email"
        )

        password = request.form.get(
            "password"
        )

        if password:

            user.password = (
                generate_password_hash(
                    password
                )
            )

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("profile")
        )

    return render_template(
        "profile.html",
        user=user
    )
# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

@app.route("/admin-dashboard")
@admin_required
def admin_dashboard():

    total_destinations = Destination.query.count()

    total_travelers = User.query.filter_by(
        role="traveler"
    ).count()

    total_bookings = Booking.query.count()

    total_revenue = db.session.query(
        db.func.sum(
            Booking.total_price
        )
    ).scalar() or 0

    recent_bookings = Booking.query.order_by(
        Booking.id.desc()
    ).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        total_destinations=total_destinations,
        total_travelers=total_travelers,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        recent_bookings=recent_bookings
    )


# ==========================================================
# DESTINATION CRUD
# ==========================================================

@app.route("/add-destination", methods=["GET", "POST"])
@admin_required
def add_destination():

    if request.method == "POST":

        destination = Destination(
            name=request.form.get("name"),
            location=request.form.get("location"),
            category=request.form.get("category"),
            price=float(request.form.get("price")),
            duration=request.form.get("duration"),
            rating=float(request.form.get("rating")),
            description=request.form.get("description"),
            image_url=request.form.get("image_url")
        )

        db.session.add(destination)
        db.session.commit()

        flash(
            "Destination added successfully.",
            "success"
        )

        return redirect(
            url_for("destinations")
        )

    return render_template(
        "destination_form.html",
        destination=None
    )


@app.route(
    "/edit-destination/<int:destination_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_destination(destination_id):

    destination = Destination.query.get_or_404(
        destination_id
    )

    if request.method == "POST":

        destination.name = request.form.get(
            "name"
        )

        destination.location = request.form.get(
            "location"
        )

        destination.category = request.form.get(
            "category"
        )

        destination.price = float(
            request.form.get("price")
        )

        destination.duration = request.form.get(
            "duration"
        )

        destination.rating = float(
            request.form.get("rating")
        )

        destination.description = request.form.get(
            "description"
        )

        destination.image_url = request.form.get(
            "image_url"
        )

        db.session.commit()

        flash(
            "Destination updated successfully.",
            "success"
        )

        return redirect(
            url_for("destinations")
        )

    return render_template(
        "destination_form.html",
        destination=destination
    )


@app.route(
    "/delete-destination/<int:destination_id>"
)
@admin_required
def delete_destination(destination_id):

    destination = Destination.query.get_or_404(
        destination_id
    )

    db.session.delete(destination)
    db.session.commit()

    flash(
        "Destination deleted successfully.",
        "info"
    )

    return redirect(
        url_for("destinations")
    )


# ==========================================================
# BOOKINGS MANAGEMENT
# ==========================================================

@app.route("/bookings")
@admin_required
def bookings():

    booking_list = Booking.query.order_by(
        Booking.id.desc()
    ).all()

    return render_template(
        "bookings.html",
        bookings=booking_list
    )


# ==========================================================
# TRAVELERS MANAGEMENT
# ==========================================================

@app.route("/travelers")
@admin_required
def travelers():

    traveler_list = User.query.filter_by(
        role="traveler"
    ).all()

    return render_template(
        "travelers.html",
        travelers=traveler_list
    )


@app.route(
    "/traveler/<int:user_id>"
)
@admin_required
def traveler_profile(user_id):

    traveler = User.query.get_or_404(
        user_id
    )

    traveler_bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    traveler_favorites = Favorite.query.filter_by(
        user_id=user_id
    ).all()

    return render_template(
        "traveler_profile.html",
        traveler=traveler,
        bookings=traveler_bookings,
        favorites=traveler_favorites
    )


# ==========================================================
# ANALYTICS
# ==========================================================

@app.route("/analytics")
@admin_required
def analytics():

    total_destinations = Destination.query.count()

    total_travelers = User.query.filter_by(
        role="traveler"
    ).count()

    total_bookings = Booking.query.count()

    total_revenue = db.session.query(
        db.func.sum(
            Booking.total_price
        )
    ).scalar() or 0

    popular_destination = (
        db.session.query(
            Destination.name,
            db.func.count(
                Booking.destination_id
            ).label("count")
        )
        .join(
            Booking,
            Booking.destination_id ==
            Destination.id
        )
        .group_by(
            Destination.id
        )
        .order_by(
            db.desc("count")
        )
        .first()
    )

    recent_bookings = Booking.query.order_by(
        Booking.id.desc()
    ).limit(10).all()

    return render_template(
        "analytics.html",
        total_destinations=total_destinations,
        total_travelers=total_travelers,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
        popular_destination=popular_destination,
        recent_bookings=recent_bookings
    )


# ==========================================================
# ABOUT
# ==========================================================

@app.route("/about")
def about():

    return render_template(
        "about.html"
    )


# ==========================================================
# CONTEXT PROCESSOR
# ==========================================================

@app.context_processor
def inject_user():

    return {
        "current_user": current_user(),
        "session": session
    }


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

with app.app_context():

    initialize_database()


# ==========================================================
# APPLICATION STARTUP
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)

