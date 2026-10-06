# ============================================================
# TIME OPTIMIZATION ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================

from datetime import datetime, timedelta


# ------------------------------------------------------------
# ACTIVITY TIME PREFERENCES
# ------------------------------------------------------------

TIME_PREFERENCES = {

    "morning": [
        "sunrise",
        "temple",
        "trek",
        "hiking",
        "walking",
        "nature",
        "park",
        "fort",
        "breakfast",
        "photography"
    ],

    "afternoon": [
        "museum",
        "shopping",
        "mall",
        "restaurant",
        "cafe",
        "indoor",
        "market",
        "heritage"
    ],

    "evening": [
        "sunset",
        "beach",
        "viewpoint",
        "dinner",
        "nightlife",
        "cultural",
        "photography",
        "light show"
    ]
}


# ------------------------------------------------------------
# TIME SLOT CONFIGURATION
# ------------------------------------------------------------

TIME_SLOTS = {

    "morning": {
        "start": "08:00",
        "end": "12:00"
    },

    "afternoon": {
        "start": "13:00",
        "end": "17:00"
    },

    "evening": {
        "start": "17:30",
        "end": "21:00"
    }
}


# ------------------------------------------------------------
# ACTIVITY TIME SCORE
# ------------------------------------------------------------

def calculate_time_preference_score(
    activity,
    time_slot
):
    """
    Calculate how suitable an activity is
    for a particular time slot.
    """

    if not activity:

        return 0

    activity_text = (
        activity.lower()
    )

    keywords = TIME_PREFERENCES.get(
        time_slot,
        []
    )

    if not keywords:

        return 50

    matched = 0

    for keyword in keywords:

        if keyword in activity_text:

            matched += 1

    if matched == 0:

        return 50

    score = min(
        50 + (matched * 15),
        100
    )

    return score


# ------------------------------------------------------------
# WEATHER-AWARE TIME SCORE
# ------------------------------------------------------------

def calculate_weather_time_score(
    activity,
    time_slot,
    weather_category
):
    """
    Adjust activity scheduling based on weather.
    """

    if not activity:

        return 0

    if not weather_category:

        return 70

    activity_text = (
        activity.lower()
    )

    if weather_category == "Rainy":

        indoor_keywords = [
            "museum",
            "mall",
            "cafe",
            "restaurant",
            "indoor",
            "shopping",
            "heritage"
        ]

        outdoor_keywords = [
            "beach",
            "trek",
            "hiking",
            "water sports",
            "outdoor"
        ]

        for keyword in indoor_keywords:

            if keyword in activity_text:

                return 100

        for keyword in outdoor_keywords:

            if keyword in activity_text:

                return 20

        return 50

    if weather_category in [
        "Very Hot",
        "Hot"
    ]:

        if time_slot in [
            "morning",
            "evening"
        ]:

            return 90

        indoor_keywords = [
            "museum",
            "mall",
            "cafe",
            "restaurant",
            "indoor",
            "shopping"
        ]

        for keyword in indoor_keywords:

            if keyword in activity_text:

                return 100

        return 40

    if weather_category == "Pleasant":

        return 95

    if weather_category == "Cool":

        return 85

    if weather_category == "Cold":

        indoor_keywords = [
            "museum",
            "cafe",
            "restaurant",
            "mall",
            "indoor"
        ]

        for keyword in indoor_keywords:

            if keyword in activity_text:

                return 95

        return 60

    return 70


# ------------------------------------------------------------
# COMBINED TIME SCORE
# ------------------------------------------------------------

def calculate_slot_score(
    activity,
    time_slot,
    weather_category=None
):
    """
    Calculate final suitability score
    for assigning an activity to a time slot.
    """

    preference_score = (
        calculate_time_preference_score(
            activity,
            time_slot
        )
    )

    weather_score = (
        calculate_weather_time_score(
            activity,
            time_slot,
            weather_category
        )
    )

    final_score = (
        preference_score * 0.55
        +
        weather_score * 0.45
    )

    return round(
        final_score,
        2
    )


# ------------------------------------------------------------
# BEST TIME SLOT
# ------------------------------------------------------------

def find_best_time_slot(
    activity,
    weather_category=None,
    used_slots=None
):
    """
    Find the best available time slot.
    """

    if used_slots is None:

        used_slots = []

    available_slots = [
        "morning",
        "afternoon",
        "evening"
    ]

    available_slots = [
        slot
        for slot in available_slots
        if slot not in used_slots
    ]

    if not available_slots:

        available_slots = [
            "morning",
            "afternoon",
            "evening"
        ]

    scores = []

    for slot in available_slots:

        score = calculate_slot_score(
            activity,
            slot,
            weather_category
        )

        scores.append(
            {
                "slot": slot,
                "score": score
            }
        )

    scores.sort(
        key=lambda item: item[
            "score"
        ],
        reverse=True
    )

    return scores[0]


# ------------------------------------------------------------
# OPTIMIZE ACTIVITY SCHEDULE
# ------------------------------------------------------------

def optimize_activity_schedule(
    activities,
    weather_category=None
):
    """
    Assign activities to the best
    available time slots.
    """

    if not activities:

        return []

    schedule = []

    used_slots = []

    for activity_item in activities:

        if isinstance(
            activity_item,
            dict
        ):

            activity = activity_item.get(
                "activity",
                ""
            )

            place = activity_item.get(
                "place",
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

            place = ""

            cost = 0

        best_slot = find_best_time_slot(
            activity=(
                f"{place} {activity}"
            ),
            weather_category=weather_category,
            used_slots=used_slots
        )

        selected_slot = best_slot[
            "slot"
        ]

        used_slots.append(
            selected_slot
        )

        schedule.append(
            {
                "time_slot": selected_slot,
                "place": place,
                "activity": activity,
                "cost": cost,
                "score": best_slot[
                    "score"
                ],
                "time_range": TIME_SLOTS[
                    selected_slot
                ]
            }
        )

    return schedule


# ------------------------------------------------------------
# OPTIMIZE COMPLETE DAY
# ------------------------------------------------------------

def optimize_day_schedule(
    day_data
):
    """
    Reorganize a single day based on
    activity suitability and weather.
    """

    if not isinstance(
        day_data,
        dict
    ):

        return day_data

    weather_category = (
        day_data.get(
            "weather_category",
            None
        )
    )

    activities = []

    for time_slot in [
        "morning",
        "afternoon",
        "evening"
    ]:

        section = day_data.get(
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

        if not activity:

            continue

        activities.append(
            {
                "place": section.get(
                    "place",
                    ""
                ),

                "activity": activity,

                "cost": section.get(
                    "cost",
                    0
                )
            }
        )

    if not activities:

        return day_data

    optimized = optimize_activity_schedule(
        activities,
        weather_category
    )

    new_day = {
        **day_data
    }

    for slot in [
        "morning",
        "afternoon",
        "evening"
    ]:

        new_day[slot] = {}

    for item in optimized:

        slot = item[
            "time_slot"
        ]

        new_day[slot] = {

            "place": item[
                "place"
            ],

            "activity": item[
                "activity"
            ],

            "cost": item[
                "cost"
            ],

            "duration": (
                "Approximately 2-3 hours"
            ),

            "time_range": item[
                "time_range"
            ],

            "optimization_score": item[
                "score"
            ]
        }

    return new_day


# ------------------------------------------------------------
# OPTIMIZE COMPLETE ITINERARY
# ------------------------------------------------------------

def optimize_itinerary_time(
    daily_itinerary
):
    """
    Optimize the time allocation
    for the complete itinerary.
    """

    if not daily_itinerary:

        return []

    optimized_itinerary = []

    for day in daily_itinerary:

        optimized_day = optimize_day_schedule(
            day
        )

        optimized_itinerary.append(
            optimized_day
        )

    return optimized_itinerary


# ------------------------------------------------------------
# DETECT SCHEDULING CONFLICTS
# ------------------------------------------------------------

def detect_schedule_conflicts(
    daily_itinerary
):
    """
    Detect missing or conflicting
    time assignments.
    """

    conflicts = []

    for day in daily_itinerary:

        day_number = day.get(
            "day",
            0
        )

        occupied_slots = []

        for slot in [
            "morning",
            "afternoon",
            "evening"
        ]:

            section = day.get(
                slot,
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

            if activity:

                if slot in occupied_slots:

                    conflicts.append(
                        {
                            "day": day_number,
                            "slot": slot,
                            "message": (
                                "Multiple activities "
                                "assigned to the same "
                                "time slot."
                            )
                        }
                    )

                occupied_slots.append(
                    slot
                )

    return conflicts


# ------------------------------------------------------------
# GENERATE TIME OPTIMIZATION SUMMARY
# ------------------------------------------------------------

def generate_time_summary(
    daily_itinerary
):
    """
    Generate a human-readable summary
    of the scheduling optimization.
    """

    if not daily_itinerary:

        return (
            "No itinerary available "
            "for time optimization."
        )

    conflicts = detect_schedule_conflicts(
        daily_itinerary
    )

    total_days = len(
        daily_itinerary
    )

    if conflicts:

        return (
            f"Time optimization completed for "
            f"{total_days} days with "
            f"{len(conflicts)} scheduling "
            f"conflicts detected."
        )

    return (
        f"Time optimization completed for "
        f"{total_days} days. Activities were "
        f"assigned to suitable morning, "
        f"afternoon and evening periods."
    )