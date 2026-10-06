import streamlit as st
from datetime import date, timedelta
import requests
import urllib.parse
import random


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="TravelGenieAI",
    page_icon="✈️",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
    }

    .title {
        font-size: 42px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-bottom: 25px;
    }

    .card {
        padding: 20px;
        border-radius: 15px;
        background-color: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }

    .day-title {
        font-size: 25px;
        font-weight: 700;
        margin-top: 15px;
    }

    .time {
        font-weight: 700;
        font-size: 16px;
    }

    .cost {
        font-weight: 700;
    }

    .feature-box {
        padding: 15px;
        border-radius: 12px;
        background-color: #ffffff;
        border: 1px solid #ddd;
        margin-bottom: 10px;
    }

    .footer {
        text-align: center;
        padding: 30px;
        color: #777;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="title">✈️ TravelGenieAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-Powered Personalized Travel Itinerary Generator</div>',
    unsafe_allow_html=True
)


# =========================================================
# CITY DATA
# =========================================================

CITY_DATA = {

    "Hyderabad": {
        "attractions": [
            ("Charminar", "Historical Places", 50),
            ("Golconda Fort", "Historical Places", 40),
            ("Salar Jung Museum", "Museums", 50),
            ("Hussain Sagar Lake", "Nature", 0),
            ("Birla Mandir", "Religious Places", 0),
            ("Ramoji Film City", "Entertainment", 1350),
            ("Necklace Road", "Nature", 0),
            ("Qutb Shahi Tombs", "Historical Places", 20)
        ],
        "experience": [
            ("Hyderabadi Biryani Food Experience", 500),
            ("Old City Heritage Walk", 300),
            ("Traditional Pearl Shopping", 1000)
        ],
        "hidden": [
            ("Paigah Tombs", "Peaceful historical architecture away from the main tourist crowd."),
            ("Khursheed Jah Devdi", "A lesser-known heritage location with old Hyderabad charm.")
        ]
    },

    "Chennai": {
        "attractions": [
            ("Marina Beach", "Nature", 0),
            ("Kapaleeshwarar Temple", "Religious Places", 0),
            ("Fort St. George", "Historical Places", 20),
            ("Government Museum", "Museums", 20),
            ("San Thome Basilica", "Religious Places", 0),
            ("Valluvar Kottam", "Historical Places", 20),
            ("Besant Nagar Beach", "Nature", 0),
            ("Guindy National Park", "Nature", 50)
        ],
        "experience": [
            ("South Indian Breakfast Experience", 300),
            ("Chennai Street Food Walk", 500),
            ("Traditional Filter Coffee Experience", 200)
        ],
        "hidden": [
            ("Theosophical Society", "A calm green heritage space with beautiful surroundings."),
            ("Broken Bridge", "A quiet photography spot near the coast.")
        ]
    },

    "Bangalore": {
        "attractions": [
            ("Bangalore Palace", "Historical Places", 300),
            ("Lalbagh Botanical Garden", "Nature", 30),
            ("Cubbon Park", "Nature", 0),
            ("Vidhana Soudha", "Historical Places", 0),
            ("ISKCON Temple", "Religious Places", 0),
            ("Bannerghatta Biological Park", "Nature", 100),
            ("Ulsoor Lake", "Nature", 0),
            ("Visvesvaraya Museum", "Museums", 100)
        ],
        "experience": [
            ("Bangalore Café Hopping", 500),
            ("Local Food Experience", 400),
            ("Garden Photography Walk", 300)
        ],
        "hidden": [
            ("Bugle Rock Park", "A peaceful heritage park with a unique natural setting."),
            ("Sankey Tank", "A relaxing lake area suitable for evening walks.")
        ]
    },

    "Mumbai": {
        "attractions": [
            ("Gateway of India", "Historical Places", 0),
            ("Marine Drive", "Nature", 0),
            ("Chhatrapati Shivaji Maharaj Terminus", "Historical Places", 0),
            ("Elephanta Caves", "Historical Places", 40),
            ("Siddhivinayak Temple", "Religious Places", 0),
            ("Juhu Beach", "Nature", 0),
            ("Colaba Causeway", "Shopping", 0),
            ("Nehru Planetarium", "Museums", 100)
        ],
        "experience": [
            ("Mumbai Street Food Tour", 500),
            ("Local Train Experience", 100),
            ("Sunset at Marine Drive", 200)
        ],
        "hidden": [
            ("Khotachiwadi", "A heritage village hidden among modern Mumbai streets."),
            ("Banganga Tank", "A peaceful historical site in the middle of the city.")
        ]
    },

    "Delhi": {
        "attractions": [
            ("India Gate", "Historical Places", 0),
            ("Red Fort", "Historical Places", 50),
            ("Qutub Minar", "Historical Places", 40),
            ("Humayun's Tomb", "Historical Places", 50),
            ("Lotus Temple", "Religious Places", 0),
            ("Akshardham Temple", "Religious Places", 0),
            ("National Museum", "Museums", 20),
            ("Lodhi Garden", "Nature", 0)
        ],
        "experience": [
            ("Delhi Street Food Experience", 500),
            ("Old Delhi Heritage Walk", 400),
            ("Traditional Chaat Experience", 300)
        ],
        "hidden": [
            ("Agrasen Ki Baoli", "An atmospheric historic stepwell in central Delhi."),
            ("Sunder Nursery", "A beautiful heritage garden ideal for photography.")
        ]
    },

    "Kohima": {
        "attractions": [
            ("Kohima War Cemetery", "Historical Places", 0),
            ("Kisama Heritage Village", "Historical Places", 50),
            ("Naga Heritage Village", "Historical Places", 50),
            ("Kohima Cathedral", "Religious Places", 0),
            ("Japfu Peak", "Adventure", 100),
            ("Dzukou Valley", "Nature", 200),
            ("Naga State Museum", "Museums", 20),
            ("Pulie Badze", "Nature", 50)
        ],
        "experience": [
            ("Traditional Naga Food Experience", 600),
            ("Naga Culture Experience", 500),
            ("Local Handicraft Experience", 400)
        ],
        "hidden": [
            ("Khonoma Village", "A beautiful heritage village known for traditional Naga culture."),
            ("Pulie Badze Wildlife Sanctuary", "A peaceful natural destination near Kohima.")
        ]
    }
}


# =========================================================
# GENERIC CITY DATA
# =========================================================

GENERIC_DATA = {
    "attractions": [
        ("City Center", "City Attractions", 0),
        ("Central Museum", "Museums", 50),
        ("Main Heritage Area", "Historical Places", 30),
        ("City Park", "Nature", 0),
        ("Local Market", "Shopping", 0),
        ("Main Temple", "Religious Places", 0)
    ],
    "experience": [
        ("Local Food Experience", 400),
        ("Heritage Walk", 300),
        ("Local Market Experience", 300)
    ],
    "hidden": [
        ("Local Hidden Gem", "Explore a less crowded local attraction."),
        ("Quiet Nature Spot", "A peaceful place away from busy tourist areas.")
    ]
}


# =========================================================
# MOOD DATA
# =========================================================

MOOD_INFO = {

    "Relaxed": [
        "Peaceful places",
        "Nature",
        "Less crowded attractions"
    ],

    "Photography": [
        "Scenic locations",
        "Architecture",
        "Sunset spots"
    ],

    "Adventure": [
        "Outdoor activities",
        "Nature",
        "Adventure attractions"
    ],

    "Foodie": [
        "Food experiences",
        "Markets",
        "Local culture"
    ],

    "History": [
        "Historical Places",
        "Museums",
        "Heritage"
    ],

    "Family": [
        "Nature",
        "Museums",
        "Family attractions"
    ]
}


# =========================================================
# MEAL DATA
# =========================================================

MEAL_DATA = {

    "Budget": {
        "breakfast": 120,
        "lunch": 250,
        "dinner": 300
    },

    "Moderate": {
        "breakfast": 200,
        "lunch": 400,
        "dinner": 500
    },

    "Luxury": {
        "breakfast": 400,
        "lunch": 800,
        "dinner": 1000
    }
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_city_data(destination):

    if destination in CITY_DATA:
        return CITY_DATA[destination]

    return GENERIC_DATA


def google_maps_link(place, destination):

    query = urllib.parse.quote(
        f"{place}, {destination}"
    )

    return (
        "https://www.google.com/maps/search/"
        "?api=1&query=" + query
    )


def destination_maps_link(destination):

    query = urllib.parse.quote(destination)

    return (
        "https://www.google.com/maps/search/"
        "?api=1&query=" + query
    )


# =========================================================
# WEATHER FUNCTIONS
# =========================================================

def geocode_city(city):

    try:

        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        if data.get("results"):

            result = data["results"][0]

            return (
                result["latitude"],
                result["longitude"],
                result.get("name", city)
            )

    except Exception:
        pass

    return None, None, city


def weather_description(code):

    descriptions = {

        0: "Clear sky",

        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Fog",

        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Heavy drizzle",

        61: "Light rain",
        63: "Moderate rain",
        65: "Heavy rain",

        71: "Light snow",
        73: "Moderate snow",
        75: "Heavy snow",

        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",

        95: "Thunderstorm",
        96: "Thunderstorm",
        99: "Thunderstorm"
    }

    return descriptions.get(
        code,
        "Weather information unavailable"
    )


def get_weather(city, start_date, days):

    latitude, longitude, city_name = geocode_city(city)

    if latitude is None:

        return []

    try:

        url = "https://api.open-meteo.com/v1/forecast"

        params = {

            "latitude": latitude,
            "longitude": longitude,

            "daily": (
                "weathercode,"
                "temperature_2m_max,"
                "temperature_2m_min,"
                "precipitation_probability_max"
            ),

            "timezone": "auto",

            "start_date": start_date.isoformat(),

            "end_date": (
                start_date +
                timedelta(days=days - 1)
            ).isoformat()
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        daily = data.get("daily", {})

        result = []

        dates = daily.get("time", [])

        codes = daily.get(
            "weathercode",
            []
        )

        max_temps = daily.get(
            "temperature_2m_max",
            []
        )

        min_temps = daily.get(
            "temperature_2m_min",
            []
        )

        rain_probs = daily.get(
            "precipitation_probability_max",
            []
        )

        for i in range(len(dates)):

            result.append({

                "date": dates[i],

                "description": weather_description(
                    codes[i]
                ),

                "max_temp": max_temps[i],

                "min_temp": min_temps[i],

                "rain_probability": rain_probs[i]
            })

        return result

    except Exception:

        return []


# =========================================================
# ATTRACTION SELECTION
# =========================================================

def select_attractions(
    attractions,
    interests,
    mood,
    day_number
):

    scored = []

    mood_preferences = MOOD_INFO.get(
        mood,
        []
    )

    for attraction in attractions:

        name = attraction[0]

        category = attraction[1]

        score = 0

        if interests:

            for interest in interests:

                if interest.lower() in category.lower():

                    score += 10

                if interest.lower() in name.lower():

                    score += 5

        for preference in mood_preferences:

            if preference.lower() in category.lower():

                score += 5

        score += random.random()

        scored.append(
            (
                score,
                attraction
            )
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected = []

    for _, attraction in scored:

        if attraction not in selected:

            selected.append(
                attraction
            )

        if len(selected) == 3:

            break

    return selected


# =========================================================
# UNIQUE EXPERIENCE
# =========================================================

def get_unique_experience(
    experiences,
    day_number
):

    if not experiences:

        return (
            "Local Experience",
            300
        )

    index = (
        day_number - 1
    ) % len(experiences)

    return experiences[index]


# =========================================================
# WHY THIS PLACE
# =========================================================

def why_recommended(
    attraction,
    mood,
    interests
):

    name = attraction[0]

    category = attraction[1]

    reasons = []

    if mood == "Photography":

        reasons.append(
            "good for photography"
        )

    elif mood == "Adventure":

        reasons.append(
            "adds an adventurous element"
        )

    elif mood == "Foodie":

        reasons.append(
            "supports local cultural exploration"
        )

    elif mood == "History":

        reasons.append(
            "has historical or cultural value"
        )

    elif mood == "Relaxed":

        reasons.append(
            "fits a relaxed travel style"
        )

    elif mood == "Family":

        reasons.append(
            "works well for a family-friendly itinerary"
        )

    if interests:

        for interest in interests:

            if interest.lower() in category.lower():

                reasons.append(
                    f"matches your {interest.lower()} interest"
                )

                break

    if not reasons:

        reasons.append(
            "adds variety to your travel plan"
        )

    return (
        f"AI Recommendation: {name} is "
        + " and ".join(reasons)
        + "."
    )


# =========================================================
# PACKING LIST
# =========================================================

def generate_packing_list(
    weather,
    mood
):

    items = [
        "Mobile phone",
        "Power bank",
        "ID proof",
        "Wallet",
        "Comfortable footwear"
    ]

    if weather:

        rain = weather.get(
            "rain_probability",
            0
        )

        max_temp = weather.get(
            "max_temp",
            30
        )

        if rain >= 40:

            items.append(
                "☔ Umbrella / Raincoat"
            )

        if max_temp >= 32:

            items.append(
                "🧴 Sunscreen"
            )

            items.append(
                "🕶️ Sunglasses"
            )

        if max_temp <= 20:

            items.append(
                "🧥 Light jacket"
            )

    if mood == "Photography":

        items.append(
            "📷 Camera / Extra storage"
        )

    if mood == "Adventure":

        items.append(
            "🎒 Small backpack"
        )

    if mood == "Foodie":

        items.append(
            "🍴 Hand sanitizer"
        )

    return items


# =========================================================
# GOLDEN HOUR
# =========================================================

def golden_hour_info():

    return {
        "sunrise": "06:00 AM",
        "sunset": "06:15 PM"
    }


# =========================================================
# ITINERARY CREATION
# =========================================================

def create_itinerary(
    destination,
    start_date,
    end_date,
    travelers,
    budget,
    mood,
    interests,
    hidden_gem
):

    city_data = get_city_data(
        destination
    )

    attractions = city_data["attractions"]

    experiences = city_data["experience"]

    hidden_places = city_data["hidden"]

    total_days = (
        end_date - start_date
    ).days + 1

    itinerary = []

    total_cost = 0

    meal_prices = MEAL_DATA.get(
        budget,
        MEAL_DATA["Moderate"]
    )

    for day_index in range(total_days):

        current_date = (
            start_date +
            timedelta(days=day_index)
        )

        day_number = day_index + 1

        selected = select_attractions(
            attractions,
            interests,
            mood,
            day_number
        )

        experience = get_unique_experience(
            experiences,
            day_number
        )

        day_items = []

        # -------------------------------------------------
        # BREAKFAST
        # -------------------------------------------------

        breakfast_cost = (
            meal_prices["breakfast"]
            * travelers
        )

        day_items.append({

            "time": "08:00 AM",

            "type": "🍳 Breakfast",

            "name": (
                f"Breakfast / Tiffin "
                f"at a local restaurant"
            ),

            "cost": breakfast_cost,

            "maps": google_maps_link(
                f"Breakfast restaurant in {destination}",
                destination
            )
        })

        # -------------------------------------------------
        # ATTRACTION 1
        # -------------------------------------------------

        attraction_1 = selected[0]

        cost_1 = (
            attraction_1[2]
            * travelers
        )

        day_items.append({

            "time": "09:00 AM",

            "type": "📍 Attraction",

            "name": attraction_1[0],

            "category": attraction_1[1],

            "cost": cost_1,

            "maps": google_maps_link(
                attraction_1[0],
                destination
            ),

            "why": why_recommended(
                attraction_1,
                mood,
                interests
            )
        })

        # -------------------------------------------------
        # ATTRACTION 2
        # -------------------------------------------------

        attraction_2 = selected[1]

        cost_2 = (
            attraction_2[2]
            * travelers
        )

        day_items.append({

            "time": "11:30 AM",

            "type": "📍 Attraction",

            "name": attraction_2[0],

            "category": attraction_2[1],

            "cost": cost_2,

            "maps": google_maps_link(
                attraction_2[0],
                destination
            ),

            "why": why_recommended(
                attraction_2,
                mood,
                interests
            )
        })

        # -------------------------------------------------
        # LUNCH
        # -------------------------------------------------

        lunch_cost = (
            meal_prices["lunch"]
            * travelers
        )

        day_items.append({

            "time": "01:30 PM",

            "type": "🍛 Lunch",

            "name": (
                "Local Lunch Experience"
            ),

            "cost": lunch_cost,

            "maps": google_maps_link(
                f"Lunch restaurant in {destination}",
                destination
            )
        })

        # -------------------------------------------------
        # ATTRACTION 3
        # -------------------------------------------------

        attraction_3 = selected[2]

        cost_3 = (
            attraction_3[2]
            * travelers
        )

        day_items.append({

            "time": "03:00 PM",

            "type": "📍 Attraction",

            "name": attraction_3[0],

            "category": attraction_3[1],

            "cost": cost_3,

            "maps": google_maps_link(
                attraction_3[0],
                destination
            ),

            "why": why_recommended(
                attraction_3,
                mood,
                interests
            )
        })

        # -------------------------------------------------
        # UNIQUE EXPERIENCE
        # -------------------------------------------------

        experience_name = experience[0]

        experience_cost = (
            experience[1]
            * travelers
        )

        day_items.append({

            "time": "05:30 PM",

            "type": "✨ Unique Experience",

            "name": experience_name,

            "cost": experience_cost,

            "maps": google_maps_link(
                experience_name,
                destination
            )
        })

        # -------------------------------------------------
        # DINNER
        # -------------------------------------------------

        dinner_cost = (
            meal_prices["dinner"]
            * travelers
        )

        day_items.append({

            "time": "07:30 PM",

            "type": "🍽️ Dinner",

            "name": (
                "Local Dinner Experience"
            ),

            "cost": dinner_cost,

            "maps": google_maps_link(
                f"Dinner restaurant in {destination}",
                destination
            )
        })

        day_cost = sum(
            item["cost"]
            for item in day_items
        )

        total_cost += day_cost

        itinerary.append({

            "day": day_number,

            "date": current_date,

            "items": day_items,

            "day_cost": day_cost
        })

    hidden = None

    if hidden_gem and hidden_places:

        hidden = hidden_places[
            (total_days - 1) %
            len(hidden_places)
        ]

    return itinerary, total_cost, hidden


# =========================================================
# SIDEBAR INPUTS
# =========================================================

st.sidebar.header("🧳 Trip Planner")

destination = st.sidebar.text_input(
    "📍 Destination",
    value="Kohima"
)

travelers = st.sidebar.number_input(
    "👥 Number of Travelers",
    min_value=1,
    max_value=20,
    value=2
)

today = date.today()

start_date = st.sidebar.date_input(
    "📅 Start Date",
    value=today
)

end_date = st.sidebar.date_input(
    "📅 End Date",
    value=today + timedelta(days=2)
)

budget = st.sidebar.selectbox(
    "💰 Budget Style",
    [
        "Budget",
        "Moderate",
        "Luxury"
    ]
)

mood = st.sidebar.selectbox(
    "🎭 Travel Mood",
    [
        "Relaxed",
        "Photography",
        "Adventure",
        "Foodie",
        "History",
        "Family"
    ]
)

transport = st.sidebar.selectbox(
    "🚗 Transport",
    [
        "Public Transport",
        "Cab / Taxi",
        "Rental Car",
        "Own Vehicle"
    ]
)

stay = st.sidebar.selectbox(
    "🏨 Stay",
    [
        "Budget Hotel",
        "3-Star Hotel",
        "4-Star Hotel",
        "5-Star Hotel"
    ]
)

interests = st.sidebar.multiselect(
    "❤️ Interests",
    [
        "Historical Places",
        "Nature",
        "Museums",
        "Religious Places",
        "Adventure",
        "Shopping",
        "Food"
    ]
)

hidden_gem = st.sidebar.checkbox(
    "💚 Include Hidden Gem"
)

generate = st.sidebar.button(
    "✨ Generate AI Itinerary",
    use_container_width=True
)


# =========================================================
# VALIDATION
# =========================================================

if end_date < start_date:

    st.error(
        "❌ End date must be after start date."
    )

    st.stop()


# =========================================================
# GENERATE
# =========================================================

if generate:

    with st.spinner(
        "🤖 Creating your personalized itinerary..."
    ):

        days = (
            end_date - start_date
        ).days + 1

        itinerary, total_cost, hidden = (
            create_itinerary(
                destination,
                start_date,
                end_date,
                travelers,
                budget,
                mood,
                interests,
                hidden_gem
            )
        )

        weather_data = get_weather(
            destination,
            start_date,
            days
        )


    # =====================================================
    # SUMMARY
    # =====================================================

    st.success(
        "🎉 Your personalized itinerary is ready!"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "📅 Days",
            days
        )

    with col2:
        st.metric(
            "👥 Travelers",
            travelers
        )

    with col3:
        st.metric(
            "💰 Estimated Cost",
            f"₹{total_cost:,.0f}"
        )

    with col4:
        st.metric(
            "🎭 Mood",
            mood
        )


    # =====================================================
    # GOOGLE MAPS
    # =====================================================

    st.subheader(
        "🗺️ Google Maps"
    )

    st.link_button(
        "📍 Open Destination in Google Maps",
        destination_maps_link(
            destination
        )
    )


    # =====================================================
    # WEATHER
    # =====================================================

    st.subheader(
        "🌦️ Weather Forecast"
    )

    if weather_data:

        weather_cols = st.columns(
            min(4, len(weather_data))
        )

        for i, weather in enumerate(
            weather_data
        ):

            with weather_cols[
                i % len(weather_cols)
            ]:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                st.write(
                    f"**📅 {weather['date']}**"
                )

                st.write(
                    f"🌤️ {weather['description']}"
                )

                st.write(
                    f"🌡️ {weather['min_temp']}°C - "
                    f"{weather['max_temp']}°C"
                )

                st.write(
                    f"🌧️ Rain Probability: "
                    f"{weather['rain_probability']}%"
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

    else:

        st.info(
            "Weather data is currently unavailable."
        )


    # =====================================================
    # WHY THIS ITINERARY
    # =====================================================

    st.subheader(
        "🧠 Why this itinerary?"
    )

    st.info(
        f"This itinerary is personalized for a "
        f"**{mood.lower()}** travel experience. "
        f"It balances sightseeing, food, local "
        f"experiences and travel breaks."
    )


    # =====================================================
    # GOLDEN HOUR
    # =====================================================

    st.subheader(
        "🌅 Golden-Hour Planner"
    )

    golden = golden_hour_info()

    g1, g2 = st.columns(2)

    with g1:

        st.metric(
            "🌄 Approx. Sunrise",
            golden["sunrise"]
        )

    with g2:

        st.metric(
            "🌇 Approx. Sunset",
            golden["sunset"]
        )


    # =====================================================
    # PACKING LIST
    # =====================================================

    st.subheader(
        "🎒 AI Packing List"
    )

    first_weather = (
        weather_data[0]
        if weather_data
        else None
    )

    packing = generate_packing_list(
        first_weather,
        mood
    )

    for item in packing:

        st.checkbox(
            item,
            value=False
        )


    # =====================================================
    # HIDDEN GEM
    # =====================================================

    if hidden:

        st.subheader(
            "💚 Hidden Gem Mode"
        )

        st.markdown(
            '<div class="feature-box">',
            unsafe_allow_html=True
        )

        st.write(
            f"📍 **{hidden[0]}**"
        )

        st.write(
            hidden[1]
        )

        st.link_button(
            "🗺️ Open Hidden Gem in Maps",
            google_maps_link(
                hidden[0],
                destination
            )
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # =====================================================
    # DAILY ITINERARY
    # =====================================================

    st.header(
        "🗓️ Your Daily Itinerary"
    )

    for day in itinerary:

        st.markdown(
            f'<div class="day-title">'
            f'Day {day["day"]} — '
            f'{day["date"].strftime("%d %b %Y")}'
            f'</div>',
            unsafe_allow_html=True
        )

        for item in day["items"]:

            st.markdown(
                '<div class="card">',
                unsafe_allow_html=True
            )

            col1, col2, col3 = st.columns(
                [1.2, 4, 1.5]
            )

            with col1:

                st.markdown(
                    f"**{item['time']}**"
                )

            with col2:

                st.markdown(
                    f"### {item['type']}"
                )

                st.write(
                    f"**{item['name']}**"
                )

                if "category" in item:

                    st.caption(
                        item["category"]
                    )

                if "why" in item:

                    st.info(
                        item["why"]
                    )

            with col3:

                st.write(
                    f"💰 ₹{item['cost']:,.0f}"
                )

                st.link_button(
                    "🗺️ Maps",
                    item["maps"]
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        st.success(
            f"💰 Day {day['day']} Estimated Cost: "
            f"₹{day['day_cost']:,.0f}"
        )


    # =====================================================
    # COST BREAKDOWN
    # =====================================================

    st.header(
        "💰 Trip Cost Summary"
    )

    cost1, cost2, cost3 = st.columns(3)

    total_attractions = 0

    total_meals = 0

    total_experience = 0

    for day in itinerary:

        for item in day["items"]:

            if item["type"] == "📍 Attraction":

                total_attractions += item["cost"]

            elif item["type"] in [
                "🍳 Breakfast",
                "🍛 Lunch",
                "🍽️ Dinner"
            ]:

                total_meals += item["cost"]

            elif item["type"] == "✨ Unique Experience":

                total_experience += item["cost"]


    with cost1:

        st.metric(
            "📍 Attractions",
            f"₹{total_attractions:,.0f}"
        )

    with cost2:

        st.metric(
            "🍽️ Meals",
            f"₹{total_meals:,.0f}"
        )

    with cost3:

        st.metric(
            "✨ Experiences",
            f"₹{total_experience:,.0f}"
        )

    st.markdown(
        f"## 💵 Total Estimated Trip Cost: "
        f"₹{total_cost:,.0f}"
    )

    st.caption(
        "Note: Accommodation and transport "
        "preferences are shown for planning but "
        "are not included in this basic estimate."
    )


    # =====================================================
    # TRAVEL CHALLENGE
    # =====================================================

    st.header(
        "🎮 Travel Challenge"
    )

    challenges = [

        "📸 Take one creative photo at every attraction.",

        "🍴 Try one local food item.",

        "🗣️ Learn one local word.",

        "🌅 Capture one sunset photo.",

        "🛍️ Buy one locally made item.",

        "🤝 Talk to one local person."
    ]

    random_challenge = random.choice(
        challenges
    )

    st.info(
        f"Today's challenge: **{random_challenge}**"
    )


    # =====================================================
    # TRAVEL JOURNAL
    # =====================================================

    st.header(
        "📸 Travel Journal"
    )

    journal = st.text_area(
        "Write your travel memory here...",
        placeholder=(
            "What was your favorite place today?"
        )
    )

    if journal:

        st.success(
            "💚 Your travel memory has been added "
            "to this session."
        )


    # =====================================================
    # SMART TIPS
    # =====================================================

    st.header(
        "💡 Smart Travel Tips"
    )

    tips = [

        "Start early to avoid crowds.",

        "Keep digital copies of important documents.",

        "Carry a power bank.",

        "Keep some local cash available.",

        "Check attraction timings before visiting.",

        "Use Google Maps for navigation.",

        "Stay hydrated during sightseeing."
    ]

    for tip in tips:

        st.write(
            f"• {tip}"
        )


# =========================================================
# DEFAULT SCREEN
# =========================================================

else:

    st.markdown(
        """
        <div class="card">
        <h2>🌍 Plan your perfect trip</h2>

        <p>
        Select your destination, dates, budget,
        travel mood and interests from the sidebar.
        </p>

        <p>
        Then click
        <b>✨ Generate AI Itinerary</b>
        to create your personalized travel plan.
        </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "🧠 Personalized AI Planning"
        )

    with col2:

        st.info(
            "🌦️ Weather-Aware Suggestions"
        )

    with col3:

        st.info(
            "🗺️ Google Maps Integration"
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

    ✈️ <b>TravelGenieAI</b>

    <br><br>

    <small>
    AI-powered personalized travel planning
    </small>

    </div>
    """,
    unsafe_allow_html=True
)