# ============================================================
# EXPLAINABLE AI ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================

"""
This module explains why activities, places and planning
decisions were selected by the travel optimization system.
"""


# ------------------------------------------------------------
# SCORE INTERPRETATION
# ------------------------------------------------------------

def classify_score(score):
    """
    Convert numerical score into a readable category.
    """

    try:
        score = float(score)
    except Exception:
        score = 0

    if score >= 90:
        return "Excellent"

    if score >= 75:
        return "Very Good"

    if score >= 60:
        return "Good"

    if score >= 40:
        return "Moderate"

    return "Low"


# ------------------------------------------------------------
# INTEREST EXPLANATION
# ------------------------------------------------------------

def explain_interest_match(
    activity,
    interests,
    interest_score
):
    """
    Explain how well an activity matches
    the traveler's interests.
    """

    activity_text = str(
        activity or ""
    ).lower()

    matched_interests = []

    for interest in interests or []:

        interest_text = str(
            interest
        ).lower()

        if interest_text in activity_text:

            matched_interests.append(
                interest
            )

    if matched_interests:

        return (
            f"Selected because it matches "
            f"your interest in "
            f"{', '.join(matched_interests)}."
        )

    category = classify_score(
        interest_score
    )

    if category in [
        "Excellent",
        "Very Good"
    ]:

        return (
            "Selected because the activity "
            "strongly aligns with your "
            "selected interests."
        )

    if category == "Good":

        return (
            "Selected because the activity "
            "has a good connection with "
            "your travel interests."
        )

    return (
        "Included to provide variety "
        "and improve overall trip coverage."
    )


# ------------------------------------------------------------
# TRAVEL STYLE EXPLANATION
# ------------------------------------------------------------

def explain_style_match(
    activity,
    travel_style,
    style_score
):
    """
    Explain compatibility with travel style.
    """

    style = str(
        travel_style or ""
    )

    category = classify_score(
        style_score
    )

    if category in [
        "Excellent",
        "Very Good"
    ]:

        return (
            f"Fits your {style} travel style "
            "and supports the preferred "
            "type of travel experience."
        )

    if category == "Good":

        return (
            f"Reasonably suitable for your "
            f"{style} travel style."
        )

    return (
        "Added as a complementary activity "
        "to maintain itinerary variety."
    )


# ------------------------------------------------------------
# WEATHER EXPLANATION
# ------------------------------------------------------------

def explain_weather_decision(
    weather_score,
    weather_category,
    activity
):
    """
    Explain how weather affected activity selection.
    """

    category = str(
        weather_category or "unknown"
    ).lower()

    try:

        score = float(
            weather_score
        )

    except Exception:

        score = 0

    activity_text = str(
        activity or ""
    ).lower()

    outdoor_keywords = [
        "beach",
        "trek",
        "hiking",
        "park",
        "garden",
        "waterfall",
        "camping",
        "cycling",
        "boating",
        "sightseeing",
        "viewpoint",
        "nature"
    ]

    indoor_keywords = [
        "museum",
        "mall",
        "shopping",
        "restaurant",
        "cafe",
        "cinema",
        "gallery",
        "aquarium",
        "indoor"
    ]

    is_outdoor = any(
        keyword in activity_text
        for keyword in outdoor_keywords
    )

    is_indoor = any(
        keyword in activity_text
        for keyword in indoor_keywords
    )

    if category in [
        "rain",
        "storm"
    ]:

        if is_indoor:

            return (
                "Indoor activity preferred because "
                "rain or storm conditions may "
                "affect outdoor activities."
            )

        if is_outdoor:

            return (
                "Outdoor activity has lower weather "
                "suitability because rain/storm "
                "conditions may affect the experience."
            )

        return (
            "Weather conditions were considered "
            "while evaluating this activity."
        )

    if category == "clear":

        if is_outdoor:

            return (
                "Clear conditions make this "
                "outdoor activity suitable."
            )

        return (
            "Weather conditions are favorable "
            "for this activity."
        )

    if category == "cloudy":

        return (
            "Cloudy conditions provide reasonable "
            "travel conditions for this activity."
        )

    if score >= 75:

        return (
            "Weather suitability is favorable "
            "for this activity."
        )

    return (
        "Weather conditions were considered "
        "during activity selection."
    )


# ------------------------------------------------------------
# BUDGET EXPLANATION
# ------------------------------------------------------------

def explain_budget_decision(
    activity_cost,
    budget_score,
    total_budget
):
    """
    Explain the budget impact of an activity.
    """

    try:

        cost = float(
            activity_cost or 0
        )

    except Exception:

        cost = 0

    try:

        score = float(
            budget_score
        )

    except Exception:

        score = 0

    try:

        budget = float(
            total_budget or 0
        )

    except Exception:

        budget = 0

    if budget <= 0:

        return (
            "Activity cost was considered "
            "during budget planning."
        )

    percentage = (
        cost / budget
    ) * 100

    if score >= 80:

        return (
            f"Estimated cost of ₹{cost:.0f} "
            f"uses approximately {percentage:.1f}% "
            "of the total trip budget and is "
            "considered budget-friendly."
        )

    if score >= 50:

        return (
            f"Estimated cost of ₹{cost:.0f} "
            "was included as a moderate "
            "budget allocation."
        )

    return (
        f"Estimated cost of ₹{cost:.0f} "
        "has a relatively high budget impact "
        "and should be balanced with lower-cost "
        "activities."
    )


# ------------------------------------------------------------
# LOCATION EXPLANATION
# ------------------------------------------------------------

def explain_location_decision(
    distance_km,
    location_score
):
    """
    Explain geographical efficiency.
    """

    try:

        distance = float(
            distance_km
        )

    except Exception:

        distance = 0

    try:

        score = float(
            location_score
        )

    except Exception:

        score = 0

    if distance <= 2:

        return (
            f"Selected because the next location "
            f"is approximately {distance:.1f} km away, "
            "reducing unnecessary travel."
        )

    if distance <= 5:

        return (
            f"Good geographical grouping with "
            f"approximately {distance:.1f} km "
            "between locations."
        )

    if distance <= 10:

        return (
            f"Moderate travel distance of "
            f"approximately {distance:.1f} km; "
            "still reasonable for the day."
        )

    if score >= 50:

        return (
            f"Approximately {distance:.1f} km of "
            "travel is required, so location efficiency "
            "was considered during optimization."
        )

    return (
        f"Longer distance of approximately "
        f"{distance:.1f} km detected. "
        "The optimizer flags this for possible "
        "rearrangement."
    )


# ------------------------------------------------------------
# TIME EXPLANATION
# ------------------------------------------------------------

def explain_time_decision(
    time_slot,
    time_score
):
    """
    Explain why an activity was placed
    in a particular time slot.
    """

    slot = str(
        time_slot or ""
    ).lower()

    try:

        score = float(
            time_score
        )

    except Exception:

        score = 0

    if slot == "morning":

        if score >= 75:

            return (
                "Scheduled in the morning because "
                "the time slot is suitable for "
                "comfortable sightseeing."
            )

        return (
            "Scheduled in the morning to avoid "
            "less favorable conditions later."
        )

    if slot == "afternoon":

        if score >= 75:

            return (
                "Scheduled in the afternoon because "
                "weather and activity timing are suitable."
            )

        return (
            "Afternoon placement was balanced "
            "against other itinerary constraints."
        )

    if slot == "evening":

        if score >= 75:

            return (
                "Scheduled in the evening because "
                "the activity is suitable for "
                "the evening time period."
            )

        return (
            "Evening placement helps distribute "
            "activities across the day."
        )

    return (
        "Time slot was selected based on "
        "overall itinerary optimization."
    )


# ------------------------------------------------------------
# OVERALL ACTIVITY EXPLANATION
# ------------------------------------------------------------

def generate_activity_explanation(
    activity,
    place,
    interests=None,
    travel_style="",
    interest_score=0,
    style_score=0,
    weather_score=0,
    weather_category="unknown",
    activity_cost=0,
    budget_score=0,
    total_budget=0,
    distance_km=0,
    location_score=0,
    time_slot="",
    time_score=0
):
    """
    Generate a complete explainable-AI
    explanation for one activity.
    """

    interests = interests or []

    explanations = []

    explanations.append(
        explain_interest_match(
            activity,
            interests,
            interest_score
        )
    )

    explanations.append(
        explain_style_match(
            activity,
            travel_style,
            style_score
        )
    )

    explanations.append(
        explain_weather_decision(
            weather_score,
            weather_category,
            activity
        )
    )

    explanations.append(
        explain_budget_decision(
            activity_cost,
            budget_score,
            total_budget
        )
    )

    explanations.append(
        explain_location_decision(
            distance_km,
            location_score
        )
    )

    explanations.append(
        explain_time_decision(
            time_slot,
            time_score
        )
    )

    return {

        "place": place,

        "activity": activity,

        "explanation": explanations,

        "summary": (
            f"{activity} at {place} was selected "
            "based on a combination of traveler "
            "preferences, travel style, weather, "
            "budget, location efficiency and timing."
        )
    }


# ------------------------------------------------------------
# DAY EXPLANATION
# ------------------------------------------------------------

def generate_day_explanation(
    day_data,
    interests=None,
    travel_style="",
    total_budget=0
):
    """
    Generate explanations for all activities
    within one itinerary day.
    """

    interests = interests or []

    day_number = day_data.get(
        "day",
        ""
    )

    date = day_data.get(
        "date",
        ""
    )

    weather_note = day_data.get(
        "weather_note",
        ""
    )

    explanations = []

    for time_slot in [
        "morning",
        "afternoon",
        "evening"
    ]:

        activity_data = day_data.get(
            time_slot,
            {}
        )

        if not isinstance(
            activity_data,
            dict
        ):

            continue

        place = activity_data.get(
            "place",
            ""
        )

        activity = activity_data.get(
            "activity",
            ""
        )

        if not place and not activity:

            continue

        explanation = (
            generate_activity_explanation(
                activity=activity,
                place=place,
                interests=interests,
                travel_style=travel_style,
                interest_score=activity_data.get(
                    "interest_score",
                    70
                ),
                style_score=activity_data.get(
                    "style_score",
                    70
                ),
                weather_score=activity_data.get(
                    "weather_score",
                    70
                ),
                weather_category=activity_data.get(
                    "weather_category",
                    "unknown"
                ),
                activity_cost=activity_data.get(
                    "cost",
                    0
                ),
                budget_score=activity_data.get(
                    "budget_score",
                    70
                ),
                total_budget=total_budget,
                distance_km=activity_data.get(
                    "distance_km",
                    0
                ),
                location_score=activity_data.get(
                    "location_score",
                    70
                ),
                time_slot=time_slot,
                time_score=activity_data.get(
                    "time_score",
                    70
                )
            )
        )

        explanations.append(
            {
                "time": time_slot,

                **explanation
            }
        )

    return {

        "day": day_number,

        "date": date,

        "weather_note": weather_note,

        "activities": explanations,

        "day_summary": (
            f"Day {day_number} was planned by "
            "balancing preferences, weather, "
            "budget, location and available time."
        )
    }


# ------------------------------------------------------------
# ITINERARY EXPLANATION
# ------------------------------------------------------------

def generate_itinerary_explanations(
    daily_itinerary,
    interests=None,
    travel_style="",
    total_budget=0
):
    """
    Generate explainable-AI information
    for the complete itinerary.
    """

    if not daily_itinerary:

        return {
            "success": False,

            "explanations": [],

            "summary": (
                "No itinerary available "
                "for explanation."
            )
        }

    explanations = []

    for day in daily_itinerary:

        explanations.append(
            generate_day_explanation(

                day_data=day,

                interests=interests,

                travel_style=travel_style,

                total_budget=total_budget
            )
        )

    return {

        "success": True,

        "explanations": explanations,

        "summary": (
            "The itinerary was generated using "
            "multi-factor decision making across "
            "traveler preferences, travel style, "
            "weather, budget, location and time."
        )
    }


# ------------------------------------------------------------
# OPTIMIZATION DECISION EXPLANATION
# ------------------------------------------------------------

def explain_optimization_results(
    recommendation_score=0,
    budget_score=0,
    location_score=0,
    weather_score=0,
    time_score=0,
    constraint_score=0
):
    """
    Explain the overall optimization decision.
    """

    scores = {

        "Personalization": (
            recommendation_score
        ),

        "Budget": (
            budget_score
        ),

        "Location": (
            location_score
        ),

        "Weather": (
            weather_score
        ),

        "Time": (
            time_score
        ),

        "Constraints": (
            constraint_score
        )
    }

    highest_factor = max(
        scores,
        key=lambda key: (
            float(
                scores[key] or 0
            )
        )
    )

    lowest_factor = min(
        scores,
        key=lambda key: (
            float(
                scores[key] or 0
            )
        )
    )

    average_score = (
        sum(
            float(
                value or 0
            )
            for value in scores.values()
        )
        /
        len(scores)
    )

    return {

        "scores": scores,

        "average_score": round(
            average_score,
            2
        ),

        "strongest_factor": (
            highest_factor
        ),

        "improvement_area": (
            lowest_factor
        ),

        "classification": (
            classify_score(
                average_score
            )
        ),

        "explanation": (
            f"The strongest optimization factor "
            f"was {highest_factor}, while "
            f"{lowest_factor} has the greatest "
            "potential for further improvement."
        )
    }


# ------------------------------------------------------------
# FINAL AI EXPLANATION
# ------------------------------------------------------------

def generate_final_explanation(
    destination,
    number_of_days,
    travelers,
    interests,
    travel_style,
    optimization_result=None
):
    """
    Generate a final explanation of how
    the AI planning system created the trip.
    """

    interests_text = ", ".join(
        interests or []
    )

    optimization_result = (
        optimization_result or {}
    )

    score = optimization_result.get(
        "average_score",
        0
    )

    classification = (
        optimization_result.get(
            "classification",
            "Not evaluated"
        )
    )

    return {

        "destination": destination,

        "duration": number_of_days,

        "travelers": travelers,

        "interests": interests_text,

        "travel_style": travel_style,

        "optimization_score": score,

        "optimization_quality": classification,

        "explanation": (
            f"The {number_of_days}-day trip to "
            f"{destination} for {travelers} traveler(s) "
            "was generated by combining traveler "
            "preferences with AI-based recommendations "
            "and multiple optimization constraints. "
            "The system considers personalization, "
            "budget, weather, geographical efficiency, "
            "timing and special requirements before "
            "producing the final itinerary."
        )
    }