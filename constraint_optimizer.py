# ============================================================
# CONSTRAINT OPTIMIZATION ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================


# ------------------------------------------------------------
# CONSTRAINT WEIGHTS
# ------------------------------------------------------------

CONSTRAINT_WEIGHTS = {
    "budget": 0.25,
    "interest": 0.20,
    "weather": 0.15,
    "distance": 0.15,
    "time": 0.10,
    "completeness": 0.10,
    "requirements": 0.05
}


# ------------------------------------------------------------
# SAFE NUMERIC CONVERSION
# ------------------------------------------------------------

def safe_float(value, default=0):
    """
    Safely convert a value into a float.
    """

    try:
        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


# ------------------------------------------------------------
# BUDGET CONSTRAINT
# ------------------------------------------------------------

def evaluate_budget_constraint(
    user_budget,
    estimated_cost
):
    """
    Evaluate whether the itinerary fits
    within the user's budget.
    """

    budget = safe_float(
        user_budget
    )

    cost = safe_float(
        estimated_cost
    )

    if budget <= 0:

        return {
            "score": 0,
            "status": "Invalid Budget",
            "difference": 0
        }

    if cost <= budget:

        percentage_used = (
            cost / budget
        ) * 100

        if percentage_used <= 70:

            score = 100
            status = "Excellent"

        elif percentage_used <= 85:

            score = 90
            status = "Good"

        elif percentage_used <= 100:

            score = 80
            status = "Within Budget"

        else:

            score = 70
            status = "Near Budget Limit"

        return {
            "score": score,
            "status": status,
            "difference": round(
                budget - cost,
                2
            ),
            "percentage_used": round(
                percentage_used,
                2
            )
        }

    excess = (
        cost - budget
    )

    excess_percentage = (
        excess / budget
    ) * 100

    if excess_percentage <= 10:

        score = 55
        status = "Slightly Over Budget"

    elif excess_percentage <= 25:

        score = 35
        status = "Over Budget"

    else:

        score = 15
        status = "Significantly Over Budget"

    return {
        "score": score,
        "status": status,
        "difference": round(
            -excess,
            2
        ),
        "percentage_used": round(
            (cost / budget) * 100,
            2
        )
    }


# ------------------------------------------------------------
# INTEREST CONSTRAINT
# ------------------------------------------------------------

def evaluate_interest_constraint(
    recommendation_scores
):
    """
    Evaluate how well the itinerary
    matches user interests.
    """

    if not recommendation_scores:

        return {
            "score": 50,
            "status": "No recommendation data"
        }

    valid_scores = []

    for score in recommendation_scores:

        numeric_score = safe_float(
            score
        )

        valid_scores.append(
            numeric_score
        )

    if not valid_scores:

        return {
            "score": 50,
            "status": "No valid scores"
        }

    average_score = (
        sum(valid_scores)
        /
        len(valid_scores)
    )

    if average_score >= 85:

        status = "Excellent Interest Match"

    elif average_score >= 70:

        status = "Good Interest Match"

    elif average_score >= 50:

        status = "Moderate Interest Match"

    else:

        status = "Low Interest Match"

    return {
        "score": round(
            min(
                average_score,
                100
            ),
            2
        ),
        "status": status
    }


# ------------------------------------------------------------
# WEATHER CONSTRAINT
# ------------------------------------------------------------

def evaluate_weather_constraint(
    weather_analysis
):
    """
    Evaluate whether activities are
    suitable for expected weather.
    """

    if not weather_analysis:

        return {
            "score": 70,
            "status": "Weather data unavailable"
        }

    total_score = 0
    count = 0

    for day in weather_analysis:

        category = day.get(
            "category",
            ""
        )

        if category == "Rainy":

            score = 60

        elif category == "Very Hot":

            score = 65

        elif category == "Hot":

            score = 75

        elif category == "Pleasant":

            score = 100

        elif category == "Cool":

            score = 90

        elif category == "Cold":

            score = 80

        else:

            score = 70

        total_score += score
        count += 1

    if count == 0:

        return {
            "score": 70,
            "status": "Weather data unavailable"
        }

    average_score = (
        total_score / count
    )

    if average_score >= 90:

        status = "Excellent Weather Compatibility"

    elif average_score >= 75:

        status = "Good Weather Compatibility"

    elif average_score >= 60:

        status = "Moderate Weather Compatibility"

    else:

        status = "Low Weather Compatibility"

    return {
        "score": round(
            average_score,
            2
        ),
        "status": status
    }


# ------------------------------------------------------------
# DISTANCE CONSTRAINT
# ------------------------------------------------------------

def evaluate_distance_constraint(
    distance_analysis
):
    """
    Evaluate geographical travel efficiency.
    """

    if not distance_analysis:

        return {
            "score": 70,
            "status": "Distance data unavailable",
            "total_distance": 0
        }

    total_distance = 0
    day_scores = []

    for day in distance_analysis:

        distance = safe_float(
            day.get(
                "total_distance_km",
                0
            )
        )

        total_distance += distance

        if distance <= 10:

            score = 100

        elif distance <= 20:

            score = 90

        elif distance <= 30:

            score = 75

        elif distance <= 50:

            score = 55

        else:

            score = 30

        day_scores.append(
            score
        )

    if not day_scores:

        return {
            "score": 70,
            "status": "Distance data unavailable",
            "total_distance": 0
        }

    average_score = (
        sum(day_scores)
        /
        len(day_scores)
    )

    if average_score >= 90:

        status = "Highly Efficient"

    elif average_score >= 75:

        status = "Efficient"

    elif average_score >= 55:

        status = "Moderate Travel"

    else:

        status = "High Travel Distance"

    return {
        "score": round(
            average_score,
            2
        ),
        "status": status,
        "total_distance": round(
            total_distance,
            2
        )
    }


# ------------------------------------------------------------
# TIME CONSTRAINT
# ------------------------------------------------------------

def evaluate_time_constraint(
    daily_itinerary
):
    """
    Evaluate whether each day contains
    a reasonable number of activities.
    """

    if not daily_itinerary:

        return {
            "score": 0,
            "status": "No itinerary available"
        }

    day_scores = []

    for day in daily_itinerary:

        activity_count = 0

        for slot in [
            "morning",
            "afternoon",
            "evening"
        ]:

            section = day.get(
                slot,
                {}
            )

            if isinstance(
                section,
                dict
            ):

                if section.get(
                    "activity",
                    ""
                ):

                    activity_count += 1

        if activity_count == 0:

            score = 20

        elif activity_count <= 2:

            score = 100

        elif activity_count == 3:

            score = 90

        elif activity_count == 4:

            score = 60

        else:

            score = 30

        day_scores.append(
            score
        )

    average_score = (
        sum(day_scores)
        /
        len(day_scores)
    )

    if average_score >= 90:

        status = "Excellent Schedule"

    elif average_score >= 75:

        status = "Good Schedule"

    elif average_score >= 50:

        status = "Moderate Schedule"

    else:

        status = "Overloaded Schedule"

    return {
        "score": round(
            average_score,
            2
        ),
        "status": status
    }


# ------------------------------------------------------------
# COMPLETENESS CONSTRAINT
# ------------------------------------------------------------

def evaluate_completeness(
    itinerary_data
):
    """
    Evaluate whether important sections
    of the generated plan are available.
    """

    if not isinstance(
        itinerary_data,
        dict
    ):

        return {
            "score": 0,
            "status": "Invalid itinerary"
        }

    required_sections = [
        "trip_summary",
        "daily_itinerary",
        "accommodation",
        "food_recommendations",
        "transportation",
        "budget_breakdown",
        "packing_checklist",
        "travel_tips"
    ]

    available = 0

    for section in required_sections:

        if section in itinerary_data:

            value = itinerary_data.get(
                section
            )

            if value is not None:

                available += 1

    score = (
        available
        /
        len(required_sections)
    ) * 100

    if score >= 90:

        status = "Complete"

    elif score >= 70:

        status = "Mostly Complete"

    elif score >= 50:

        status = "Partially Complete"

    else:

        status = "Incomplete"

    return {
        "score": round(
            score,
            2
        ),
        "status": status,
        "available_sections": available,
        "total_sections": len(
            required_sections
        )
    }


# ------------------------------------------------------------
# SPECIAL REQUIREMENTS CONSTRAINT
# ------------------------------------------------------------

def evaluate_special_requirements(
    itinerary_data,
    special_requirements
):
    """
    Basic validation of user special requirements.
    """

    if not special_requirements:

        return {
            "score": 100,
            "status": "No special requirements"
        }

    requirement_text = (
        str(
            special_requirements
        ).lower()
    )

    searchable_content = (
        str(
            itinerary_data
        ).lower()
    )

    requirements = [
        item.strip()
        for item in requirement_text.split(
            ","
        )
        if item.strip()
    ]

    if not requirements:

        return {
            "score": 100,
            "status": "No special requirements"
        }

    matched = 0

    for requirement in requirements:

        words = requirement.split()

        useful_words = [
            word
            for word in words
            if len(word) > 3
        ]

        if not useful_words:

            continue

        word_matches = 0

        for word in useful_words:

            if word in searchable_content:

                word_matches += 1

        if (
            word_matches
            >=
            max(
                1,
                len(useful_words) // 2
            )
        ):

            matched += 1

    score = (
        matched
        /
        len(requirements)
    ) * 100

    if score >= 90:

        status = "Requirements Well Covered"

    elif score >= 60:

        status = "Requirements Partially Covered"

    else:

        status = "Requirements Need Review"

    return {
        "score": round(
            score,
            2
        ),
        "status": status,
        "matched_requirements": matched,
        "total_requirements": len(
            requirements
        )
    }


# ------------------------------------------------------------
# OVERALL CONSTRAINT SCORE
# ------------------------------------------------------------

def calculate_overall_constraint_score(
    constraint_results
):
    """
    Calculate the final weighted optimization score.
    """

    total_score = 0

    for constraint_name, weight in (
        CONSTRAINT_WEIGHTS.items()
    ):

        result = constraint_results.get(
            constraint_name,
            {}
        )

        score = safe_float(
            result.get(
                "score",
                0
            )
        )

        total_score += (
            score * weight
        )

    return round(
        min(
            max(
                total_score,
                0
            ),
            100
        ),
        2
    )


# ------------------------------------------------------------
# CLASSIFY OPTIMIZATION QUALITY
# ------------------------------------------------------------

def classify_optimization_score(
    score
):
    """
    Convert optimization score
    into a readable quality level.
    """

    if score >= 90:

        return "Excellent"

    if score >= 80:

        return "Highly Optimized"

    if score >= 70:

        return "Well Optimized"

    if score >= 60:

        return "Moderately Optimized"

    if score >= 50:

        return "Needs Improvement"

    return "Poor Optimization"


# ------------------------------------------------------------
# GENERATE OPTIMIZATION SUGGESTIONS
# ------------------------------------------------------------

def generate_constraint_suggestions(
    constraint_results
):
    """
    Generate improvement suggestions
    based on weak constraints.
    """

    suggestions = []

    budget = constraint_results.get(
        "budget",
        {}
    )

    if safe_float(
        budget.get(
            "score",
            0
        )
    ) < 70:

        suggestions.append(
            "Reduce expensive activities, "
            "accommodation or transportation "
            "to improve budget compliance."
        )

    interest = constraint_results.get(
        "interest",
        {}
    )

    if safe_float(
        interest.get(
            "score",
            0
        )
    ) < 70:

        suggestions.append(
            "Replace low-interest activities "
            "with attractions that better match "
            "the user's preferences."
        )

    weather = constraint_results.get(
        "weather",
        {}
    )

    if safe_float(
        weather.get(
            "score",
            0
        )
    ) < 70:

        suggestions.append(
            "Rearrange outdoor and indoor activities "
            "according to expected weather conditions."
        )

    distance = constraint_results.get(
        "distance",
        {}
    )

    if safe_float(
        distance.get(
            "score",
            0
        )
    ) < 70:

        suggestions.append(
            "Group geographically nearby attractions "
            "to reduce unnecessary travel."
        )

    time_result = constraint_results.get(
        "time",
        {}
    )

    if safe_float(
        time_result.get(
            "score",
            0
        )
    ) < 70:

        suggestions.append(
            "Reduce the number of activities "
            "scheduled in a single day."
        )

    completeness = constraint_results.get(
        "completeness",
        {}
    )

    if safe_float(
        completeness.get(
            "score",
            0
        )
    ) < 80:

        suggestions.append(
            "Complete missing itinerary sections "
            "before finalizing the travel plan."
        )

    requirements = constraint_results.get(
        "requirements",
        {}
    )

    if safe_float(
        requirements.get(
            "score",
            0
        )
    ) < 70:

        suggestions.append(
            "Review the itinerary against all "
            "special travel requirements."
        )

    if not suggestions:

        suggestions.append(
            "The itinerary satisfies the major "
            "planning constraints."
        )

    return suggestions


# ------------------------------------------------------------
# MAIN CONSTRAINT OPTIMIZER
# ------------------------------------------------------------

def optimize_constraints(
    itinerary_data,
    user_budget,
    estimated_cost,
    recommendation_scores=None,
    weather_analysis=None,
    distance_analysis=None,
    special_requirements=""
):
    """
    Evaluate the complete itinerary using
    multiple optimization constraints.
    """

    if recommendation_scores is None:

        recommendation_scores = []

    if weather_analysis is None:

        weather_analysis = []

    if distance_analysis is None:

        distance_analysis = []

    daily_itinerary = itinerary_data.get(
        "daily_itinerary",
        []
    )

    constraint_results = {

        "budget": (
            evaluate_budget_constraint(
                user_budget,
                estimated_cost
            )
        ),

        "interest": (
            evaluate_interest_constraint(
                recommendation_scores
            )
        ),

        "weather": (
            evaluate_weather_constraint(
                weather_analysis
            )
        ),

        "distance": (
            evaluate_distance_constraint(
                distance_analysis
            )
        ),

        "time": (
            evaluate_time_constraint(
                daily_itinerary
            )
        ),

        "completeness": (
            evaluate_completeness(
                itinerary_data
            )
        ),

        "requirements": (
            evaluate_special_requirements(
                itinerary_data,
                special_requirements
            )
        )
    }

    overall_score = (
        calculate_overall_constraint_score(
            constraint_results
        )
    )

    optimization_level = (
        classify_optimization_score(
            overall_score
        )
    )

    suggestions = (
        generate_constraint_suggestions(
            constraint_results
        )
    )

    return {

        "overall_score": overall_score,

        "optimization_level": (
            optimization_level
        ),

        "constraint_results": (
            constraint_results
        ),

        "suggestions": suggestions
    }


# ------------------------------------------------------------
# GENERATE FINAL OPTIMIZATION SUMMARY
# ------------------------------------------------------------

def generate_constraint_summary(
    optimization_result
):
    """
    Generate a concise human-readable
    optimization summary.
    """

    if not optimization_result:

        return (
            "Optimization analysis unavailable."
        )

    score = safe_float(
        optimization_result.get(
            "overall_score",
            0
        )
    )

    level = optimization_result.get(
        "optimization_level",
        "Unknown"
    )

    return (
        f"Overall itinerary optimization score: "
        f"{score:.1f}/100 — {level}."
    )