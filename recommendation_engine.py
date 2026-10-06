# ============================================================
# ADVANCED RECOMMENDATION ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================


# ------------------------------------------------------------
# INTEREST KEYWORDS
# ------------------------------------------------------------

INTEREST_KEYWORDS = {

    "Beaches": [
        "beach",
        "sea",
        "coast",
        "island",
        "water",
        "shore"
    ],

    "History": [
        "fort",
        "palace",
        "museum",
        "heritage",
        "historical",
        "monument",
        "temple"
    ],

    "Food": [
        "restaurant",
        "food",
        "cafe",
        "market",
        "street food",
        "cuisine",
        "dining"
    ],

    "Adventure": [
        "trek",
        "hiking",
        "rafting",
        "camping",
        "water sports",
        "adventure",
        "zipline",
        "climbing"
    ],

    "Nature": [
        "park",
        "waterfall",
        "forest",
        "lake",
        "garden",
        "wildlife",
        "nature",
        "mountain",
        "valley"
    ],

    "Shopping": [
        "market",
        "shopping",
        "mall",
        "bazaar",
        "street market"
    ],

    "Culture": [
        "temple",
        "festival",
        "heritage",
        "museum",
        "cultural",
        "art",
        "tradition"
    ],

    "Photography": [
        "viewpoint",
        "sunset",
        "scenic",
        "photography",
        "lake",
        "beach",
        "mountain",
        "landscape"
    ],

    "Relaxation": [
        "spa",
        "resort",
        "beach",
        "park",
        "garden",
        "relax",
        "wellness"
    ],

    "Nightlife": [
        "club",
        "bar",
        "night",
        "pub",
        "nightlife",
        "lounge",
        "party"
    ]
}


# ------------------------------------------------------------
# TRAVEL STYLE KEYWORDS
# ------------------------------------------------------------

STYLE_KEYWORDS = {

    "Budget": [
        "free",
        "walk",
        "public",
        "market",
        "park",
        "street",
        "local",
        "budget"
    ],

    "Luxury": [
        "resort",
        "spa",
        "premium",
        "luxury",
        "fine dining",
        "private",
        "five star"
    ],

    "Adventure": [
        "trek",
        "rafting",
        "hiking",
        "camping",
        "water sports",
        "adventure",
        "climbing"
    ],

    "Family": [
        "park",
        "museum",
        "zoo",
        "family",
        "garden",
        "beach",
        "kid"
    ],

    "Romantic": [
        "sunset",
        "beach",
        "candlelight",
        "resort",
        "romantic",
        "viewpoint",
        "couple"
    ],

    "Solo": [
        "walking",
        "museum",
        "cafe",
        "market",
        "photography",
        "explore",
        "local"
    ],

    "Standard": [
        "tour",
        "sightseeing",
        "restaurant",
        "museum",
        "market",
        "park"
    ]
}


# ------------------------------------------------------------
# WEATHER KEYWORDS
# ------------------------------------------------------------

WEATHER_RULES = {

    "Rainy": {
        "preferred": [
            "museum",
            "cafe",
            "restaurant",
            "mall",
            "indoor",
            "shopping",
            "heritage"
        ],

        "avoid": [
            "beach",
            "trek",
            "hiking",
            "water sports",
            "outdoor"
        ]
    },

    "Very Hot": {
        "preferred": [
            "museum",
            "mall",
            "cafe",
            "indoor",
            "restaurant"
        ],

        "avoid": [
            "trek",
            "hiking",
            "long walk",
            "outdoor"
        ]
    },

    "Hot": {
        "preferred": [
            "museum",
            "cafe",
            "restaurant",
            "park",
            "indoor"
        ],

        "avoid": [
            "long walk",
            "trek"
        ]
    },

    "Pleasant": {
        "preferred": [
            "beach",
            "park",
            "trek",
            "hiking",
            "photography",
            "sightseeing",
            "outdoor"
        ],

        "avoid": []
    },

    "Cool": {
        "preferred": [
            "sightseeing",
            "museum",
            "park",
            "photography",
            "walking"
        ],

        "avoid": []
    },

    "Cold": {
        "preferred": [
            "museum",
            "cafe",
            "restaurant",
            "indoor"
        ],

        "avoid": [
            "water sports"
        ]
    }
}


# ------------------------------------------------------------
# INTEREST SCORE
# ------------------------------------------------------------

def calculate_interest_score(
    activity,
    interests
):
    """
    Calculate how strongly an activity matches
    the user's selected interests.
    """

    if not activity:
        return 0

    activity_text = (
        activity.lower()
    )

    if not interests:
        return 50

    matched_interests = 0

    for interest in interests:

        keywords = INTEREST_KEYWORDS.get(
            interest,
            []
        )

        for keyword in keywords:

            if keyword.lower() in activity_text:

                matched_interests += 1

                break

    if not interests:
        return 0

    score = (
        matched_interests
        /
        len(interests)
    ) * 100

    return round(
        min(score, 100),
        2
    )


# ------------------------------------------------------------
# TRAVEL STYLE SCORE
# ------------------------------------------------------------

def calculate_style_score(
    activity,
    travel_style
):
    """
    Calculate compatibility with travel style.
    """

    if not activity:
        return 0

    activity_text = (
        activity.lower()
    )

    keywords = STYLE_KEYWORDS.get(
        travel_style,
        []
    )

    if not keywords:
        return 50

    matches = 0

    for keyword in keywords:

        if keyword.lower() in activity_text:

            matches += 1

    if matches == 0:

        return 30

    score = min(
        matches * 20,
        100
    )

    return score


# ------------------------------------------------------------
# WEATHER SCORE
# ------------------------------------------------------------

def calculate_weather_score(
    activity,
    weather_category
):
    """
    Calculate suitability of an activity
    under expected weather conditions.
    """

    if not activity:

        return 0

    if not weather_category:

        return 70

    rules = WEATHER_RULES.get(
        weather_category
    )

    if not rules:

        return 70

    activity_text = (
        activity.lower()
    )

    for keyword in rules[
        "avoid"
    ]:

        if keyword.lower() in activity_text:

            return 20

    for keyword in rules[
        "preferred"
    ]:

        if keyword.lower() in activity_text:

            return 100

    return 60


# ------------------------------------------------------------
# BUDGET SCORE
# ------------------------------------------------------------

def calculate_budget_score(
    cost,
    daily_budget
):
    """
    Calculate affordability of an activity.
    """

    try:

        cost = float(
            cost or 0
        )

        daily_budget = float(
            daily_budget or 0
        )

    except (
        TypeError,
        ValueError
    ):

        return 50

    if daily_budget <= 0:

        return 50

    percentage = (
        cost / daily_budget
    ) * 100

    if percentage <= 10:

        return 100

    if percentage <= 20:

        return 90

    if percentage <= 30:

        return 80

    if percentage <= 40:

        return 65

    if percentage <= 50:

        return 50

    if percentage <= 70:

        return 35

    return 20


# ------------------------------------------------------------
# TIME SCORE
# ------------------------------------------------------------

def calculate_time_score(
    activity,
    time_slot
):
    """
    Estimate suitability of activity
    for a time of day.
    """

    if not activity:

        return 50

    activity_text = (
        activity.lower()
    )

    time_slot = (
        time_slot.lower()
    )

    morning_keywords = [
        "sunrise",
        "temple",
        "trek",
        "hiking",
        "walking",
        "market",
        "breakfast"
    ]

    afternoon_keywords = [
        "museum",
        "shopping",
        "mall",
        "restaurant",
        "cafe",
        "indoor"
    ]

    evening_keywords = [
        "sunset",
        "beach",
        "night",
        "viewpoint",
        "dinner",
        "cultural",
        "nightlife"
    ]

    if time_slot == "morning":

        keywords = morning_keywords

    elif time_slot == "afternoon":

        keywords = afternoon_keywords

    else:

        keywords = evening_keywords

    for keyword in keywords:

        if keyword in activity_text:

            return 100

    return 60


# ------------------------------------------------------------
# FINAL RECOMMENDATION SCORE
# ------------------------------------------------------------

def calculate_recommendation_score(
    activity,
    interests,
    travel_style,
    weather_category=None,
    cost=0,
    daily_budget=0,
    time_slot="morning"
):
    """
    Calculate final multi-factor recommendation score.
    """

    interest_score = (
        calculate_interest_score(
            activity,
            interests
        )
    )

    style_score = (
        calculate_style_score(
            activity,
            travel_style
        )
    )

    weather_score = (
        calculate_weather_score(
            activity,
            weather_category
        )
    )

    budget_score = (
        calculate_budget_score(
            cost,
            daily_budget
        )
    )

    time_score = (
        calculate_time_score(
            activity,
            time_slot
        )
    )

    # Weighted intelligent scoring
    final_score = (

        interest_score * 0.35

        + style_score * 0.20

        + weather_score * 0.20

        + budget_score * 0.15

        + time_score * 0.10
    )

    return round(
        min(
            max(
                final_score,
                0
            ),
            100
        ),
        2
    )


# ------------------------------------------------------------
# RANK ACTIVITIES
# ------------------------------------------------------------

def rank_activities(
    activities,
    interests,
    travel_style,
    weather_category=None,
    daily_budget=0,
    time_slot="morning"
):
    """
    Rank activities using multiple AI-inspired factors.
    """

    ranked = []

    for activity_item in activities:

        if isinstance(
            activity_item,
            dict
        ):

            activity = activity_item.get(
                "activity",
                ""
            )

            cost = activity_item.get(
                "cost",
                0
            )

        else:

            activity = str(
                activity_item
            )

            cost = 0

        score = (
            calculate_recommendation_score(
                activity=activity,
                interests=interests,
                travel_style=travel_style,
                weather_category=weather_category,
                cost=cost,
                daily_budget=daily_budget,
                time_slot=time_slot
            )
        )

        ranked.append(
            {
                "activity": activity,
                "cost": cost,
                "score": score
            }
        )

    ranked.sort(
        key=lambda item: item[
            "score"
        ],
        reverse=True
    )

    return ranked


# ------------------------------------------------------------
# RECOMMENDATION LEVEL
# ------------------------------------------------------------

def classify_recommendation(
    score
):
    """
    Convert numerical score into
    human-readable recommendation level.
    """

    if score >= 85:

        return "Highly Recommended"

    if score >= 70:

        return "Recommended"

    if score >= 50:

        return "Moderately Recommended"

    return "Low Priority"


# ------------------------------------------------------------
# GENERATE RECOMMENDATION SUMMARY
# ------------------------------------------------------------

def generate_recommendation_summary(
    activities,
    interests,
    travel_style,
    weather_category=None,
    daily_budget=0
):
    """
    Generate ranked recommendations
    and an explainable summary.
    """

    ranked = rank_activities(
        activities=activities,
        interests=interests,
        travel_style=travel_style,
        weather_category=weather_category,
        daily_budget=daily_budget
    )

    if not ranked:

        return {
            "ranked_activities": [],
            "top_recommendation": None,
            "summary": (
                "No activities were available "
                "for recommendation."
            )
        }

    for item in ranked:

        item[
            "recommendation_level"
        ] = classify_recommendation(
            item[
                "score"
            ]
        )

    top_activity = ranked[0]

    summary = (
        f"'{top_activity['activity']}' "
        f"received the highest personalized "
        f"recommendation score of "
        f"{top_activity['score']}/100."
    )

    return {

        "ranked_activities": ranked,

        "top_recommendation": (
            top_activity
        ),

        "summary": summary
    }


# ------------------------------------------------------------
# ITINERARY RECOMMENDATION ANALYSIS
# ------------------------------------------------------------

def analyze_itinerary_recommendations(
    daily_itinerary,
    interests,
    travel_style
):
    """
    Analyze the activities already selected
    in the generated itinerary.
    """

    results = []

    for day in daily_itinerary:

        day_number = day.get(
            "day",
            0
        )

        for time_slot in [
            "morning",
            "afternoon",
            "evening"
        ]:

            section = day.get(
                time_slot,
                {}
            )

            if not isinstance(
                section,
                dict
            ):

                continue

            activity = section.get(
                "activity",
                ""
            )

            place = section.get(
                "place",
                ""
            )

            cost = section.get(
                "cost",
                0
            )

            weather_category = (
                day.get(
                    "weather_category",
                    None
                )
            )

            score = (
                calculate_recommendation_score(
                    activity=(
                        f"{place} {activity}"
                    ),
                    interests=interests,
                    travel_style=travel_style,
                    weather_category=(
                        weather_category
                    ),
                    cost=cost,
                    time_slot=time_slot
                )
            )

            results.append(
                {
                    "day": day_number,
                    "time": time_slot,
                    "place": place,
                    "activity": activity,
                    "score": score,
                    "recommendation_level": (
                        classify_recommendation(
                            score
                        )
                    )
                }
            )

    return results