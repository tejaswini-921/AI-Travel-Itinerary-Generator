# ============================================================
# ADVANCED ITINERARY ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================

"""
Central orchestration engine for the travel planning system.

This module connects:
    AI Engine
    Recommendation Engine
    Weather Engine
    Budget Optimizer
    Location Optimizer
    Time Optimizer
    Constraint Optimizer
    Explanation Engine
"""


from datetime import datetime, timedelta

from recommendation_engine import (
    analyze_itinerary_recommendations
)

from budget_optimizer import (
    optimize_budget
)

from location_optimizer import (
    optimize_locations,
    generate_location_summary
)

from time_optimizer import (
    optimize_itinerary_time,
    generate_time_summary
)

from constraint_optimizer import (
    optimize_constraints,
    generate_constraint_summary
)

from explanation_engine import (
    generate_itinerary_explanations,
    explain_optimization_results
)


# ------------------------------------------------------------
# DATE GENERATION
# ------------------------------------------------------------

def generate_trip_dates(
    start_date,
    number_of_days
):
    """
    Generate dates for every trip day.
    """

    try:

        start = datetime.strptime(
            str(start_date),
            "%Y-%m-%d"
        ).date()

    except Exception:

        return []

    dates = []

    for day_number in range(
        number_of_days
    ):

        current_date = (
            start
            +
            timedelta(
                days=day_number
            )
        )

        dates.append(
            current_date.isoformat()
        )

    return dates


# ------------------------------------------------------------
# BASIC ITINERARY VALIDATION
# ------------------------------------------------------------

def validate_itinerary_structure(
    itinerary
):
    """
    Validate the basic structure of
    an AI-generated itinerary.
    """

    if not isinstance(
        itinerary,
        dict
    ):

        return {
            "valid": False,
            "errors": [
                "Itinerary must be a dictionary."
            ]
        }

    errors = []

    required_sections = [
        "trip_summary",
        "daily_itinerary",
        "budget_breakdown"
    ]

    for section in required_sections:

        if section not in itinerary:

            errors.append(
                f"Missing section: {section}"
            )

    daily_itinerary = itinerary.get(
        "daily_itinerary",
        []
    )

    if not isinstance(
        daily_itinerary,
        list
    ):

        errors.append(
            "daily_itinerary must be a list."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


# ------------------------------------------------------------
# NORMALIZE DAILY ITINERARY
# ------------------------------------------------------------

def normalize_daily_itinerary(
    daily_itinerary,
    start_date,
    number_of_days
):
    """
    Ensure every day contains the expected
    morning, afternoon and evening structure.
    """

    dates = generate_trip_dates(
        start_date,
        number_of_days
    )

    normalized = []

    for index in range(
        number_of_days
    ):

        if index < len(
            daily_itinerary
        ):

            original_day = (
                daily_itinerary[index]
            )

        else:

            original_day = {}

        if not isinstance(
            original_day,
            dict
        ):

            original_day = {}

        day_number = (
            index + 1
        )

        date = (
            original_day.get(
                "date"
            )
            or
            (
                dates[index]
                if index < len(dates)
                else ""
            )
        )

        day_data = {

            "day": day_number,

            "date": date,

            "weather_note": (
                original_day.get(
                    "weather_note",
                    ""
                )
            ),

            "morning": (
                original_day.get(
                    "morning",
                    {}
                )
                if isinstance(
                    original_day.get(
                        "morning",
                        {}
                    ),
                    dict
                )
                else {}
            ),

            "afternoon": (
                original_day.get(
                    "afternoon",
                    {}
                )
                if isinstance(
                    original_day.get(
                        "afternoon",
                        {}
                    ),
                    dict
                )
                else {}
            ),

            "evening": (
                original_day.get(
                    "evening",
                    {}
                )
                if isinstance(
                    original_day.get(
                        "evening",
                        {}
                    ),
                    dict
                )
                else {}
            ),

            "daily_cost": (
                original_day.get(
                    "daily_cost",
                    0
                )
            )
        }

        normalized.append(
            day_data
        )

    return normalized


# ------------------------------------------------------------
# APPLY WEATHER DATA
# ------------------------------------------------------------

def apply_weather_to_itinerary(
    daily_itinerary,
    weather_result
):
    """
    Add weather information to each itinerary day.
    """

    if not weather_result:

        return daily_itinerary

    forecast = weather_result.get(
        "forecast",
        []
    )

    forecast_map = {

        item.get("date"): item

        for item in forecast

        if item.get("date")
    }

    updated_itinerary = []

    for day in daily_itinerary:

        date = day.get(
            "date",
            ""
        )

        weather = forecast_map.get(
            date
        )

        updated_day = dict(
            day
        )

        if weather:

            condition = weather.get(
                "condition",
                "Unknown"
            )

            minimum_temperature = (
                weather.get(
                    "temperature_min"
                )
            )

            maximum_temperature = (
                weather.get(
                    "temperature_max"
                )
            )

            precipitation_probability = (
                weather.get(
                    "precipitation_probability",
                    0
                )
            )

            updated_day[
                "weather_note"
            ] = (
                f"{condition}. "
                f"Temperature: "
                f"{minimum_temperature}°C - "
                f"{maximum_temperature}°C. "
                f"Rain probability: "
                f"{precipitation_probability}%."
            )

            updated_day[
                "weather_category"
            ] = weather.get(
                "category",
                "unknown"
            )

            updated_day[
                "weather_score"
            ] = weather.get(
                "weather_score",
                70
            )

        updated_itinerary.append(
            updated_day
        )

    return updated_itinerary


# ------------------------------------------------------------
# APPLY TIME OPTIMIZATION
# ------------------------------------------------------------

def apply_time_optimization(
    daily_itinerary,
    weather_result=None
):
    """
    Optimize activity timing.
    """

    try:

        result = optimize_itinerary_time(
            daily_itinerary,
            weather_result
        )

        if isinstance(
            result,
            dict
        ):

            if "daily_itinerary" in result:

                return (
                    result[
                        "daily_itinerary"
                    ],
                    result
                )

            if "itinerary" in result:

                return (
                    result[
                        "itinerary"
                    ],
                    result
                )

        if isinstance(
            result,
            list
        ):

            return (
                result,
                {
                    "daily_itinerary": result
                }
            )

    except Exception as error:

        return (
            daily_itinerary,
            {
                "success": False,
                "error": str(error)
            }
        )

    return (
        daily_itinerary,
        {}
    )


# ------------------------------------------------------------
# CALCULATE BASIC ACTIVITY DATA
# ------------------------------------------------------------

def enrich_activity_data(
    daily_itinerary,
    interests,
    travel_style,
    budget
):
    """
    Add basic fields used by the optimization
    and explanation layers.
    """

    updated_itinerary = []

    for day in daily_itinerary:

        updated_day = dict(
            day
        )

        for time_slot in [
            "morning",
            "afternoon",
            "evening"
        ]:

            activity = updated_day.get(
                time_slot,
                {}
            )

            if not isinstance(
                activity,
                dict
            ):

                activity = {}

            updated_activity = dict(
                activity
            )

            updated_activity.setdefault(
                "interest_score",
                70
            )

            updated_activity.setdefault(
                "style_score",
                70
            )

            updated_activity.setdefault(
                "weather_score",
                updated_day.get(
                    "weather_score",
                    70
                )
            )

            updated_activity.setdefault(
                "budget_score",
                70
            )

            updated_activity.setdefault(
                "location_score",
                70
            )

            updated_activity.setdefault(
                "time_score",
                70
            )

            updated_activity.setdefault(
                "distance_km",
                0
            )

            updated_activity.setdefault(
                "weather_category",
                updated_day.get(
                    "weather_category",
                    "unknown"
                )
            )

            updated_day[
                time_slot
            ] = updated_activity

        updated_itinerary.append(
            updated_day
        )

    return updated_itinerary


# ------------------------------------------------------------
# APPLY LOCATION INFORMATION
# ------------------------------------------------------------

def apply_location_analysis(
    daily_itinerary,
    location_result
):
    """
    Add geographical efficiency information
    to itinerary activities.
    """

    if not location_result:

        return daily_itinerary

    distance_analysis = (
        location_result.get(
            "distance_analysis",
            []
        )
    )

    day_map = {

        item.get("day"): item

        for item in distance_analysis
    }

    updated_itinerary = []

    for day in daily_itinerary:

        updated_day = dict(
            day
        )

        day_number = updated_day.get(
            "day"
        )

        day_analysis = day_map.get(
            day_number,
            {}
        )

        connections = day_analysis.get(
            "connections",
            []
        )

        slots = [
            "morning",
            "afternoon",
            "evening"
        ]

        for index, slot in enumerate(
            slots
        ):

            activity = updated_day.get(
                slot,
                {}
            )

            if not isinstance(
                activity,
                dict
            ):

                activity = {}

            updated_activity = dict(
                activity
            )

            if index > 0:

                connection_index = (
                    index - 1
                )

                if connection_index < len(
                    connections
                ):

                    connection = connections[
                        connection_index
                    ]

                    updated_activity[
                        "distance_km"
                    ] = connection.get(
                        "distance_km",
                        0
                    )

                    updated_activity[
                        "location_score"
                    ] = connection.get(
                        "efficiency_score",
                        70
                    )

            updated_day[
                slot
            ] = updated_activity

        updated_itinerary.append(
            updated_day
        )

    return updated_itinerary


# ------------------------------------------------------------
# APPLY WEATHER ACTIVITY SCORES
# ------------------------------------------------------------

def apply_weather_activity_scores(
    daily_itinerary,
    weather_result
):
    """
    Add weather suitability scores to activities.
    """

    if not weather_result:

        return daily_itinerary

    forecast = weather_result.get(
        "forecast",
        []
    )

    forecast_map = {

        item.get("date"): item

        for item in forecast
    }

    updated = []

    for day in daily_itinerary:

        updated_day = dict(
            day
        )

        date = updated_day.get(
            "date",
            ""
        )

        weather = forecast_map.get(
            date
        )

        if weather:

            weather_score = weather.get(
                "weather_score",
                70
            )

            weather_category = weather.get(
                "category",
                "unknown"
            )

            updated_day[
                "weather_score"
            ] = weather_score

            updated_day[
                "weather_category"
            ] = weather_category

            for slot in [
                "morning",
                "afternoon",
                "evening"
            ]:

                activity = updated_day.get(
                    slot,
                    {}
                )

                if not isinstance(
                    activity,
                    dict
                ):

                    activity = {}

                updated_activity = dict(
                    activity
                )

                updated_activity[
                    "weather_score"
                ] = weather_score

                updated_activity[
                    "weather_category"
                ] = weather_category

                updated_day[
                    slot
                ] = updated_activity

        updated.append(
            updated_day
        )

    return updated


# ------------------------------------------------------------
# CALCULATE ITINERARY STATISTICS
# ------------------------------------------------------------

def calculate_itinerary_statistics(
    daily_itinerary
):
    """
    Calculate useful final itinerary statistics.
    """

    total_days = len(
        daily_itinerary
    )

    activity_count = 0

    total_activity_cost = 0

    for day in daily_itinerary:

        for slot in [
            "morning",
            "afternoon",
            "evening"
        ]:

            activity = day.get(
                slot,
                {}
            )

            if not isinstance(
                activity,
                dict
            ):

                continue

            place = activity.get(
                "place",
                ""
            )

            activity_name = activity.get(
                "activity",
                ""
            )

            if place or activity_name:

                activity_count += 1

            try:

                total_activity_cost += float(
                    activity.get(
                        "cost",
                        0
                    )
                    or 0
                )

            except Exception:

                pass

    average_activities_per_day = (
        activity_count / total_days
        if total_days > 0
        else 0
    )

    return {

        "total_days": total_days,

        "activity_count": activity_count,

        "average_activities_per_day": round(
            average_activities_per_day,
            2
        ),

        "activity_cost": round(
            total_activity_cost,
            2
        )
    }


# ------------------------------------------------------------
# COMPLETE OPTIMIZATION PIPELINE
# ------------------------------------------------------------

def optimize_complete_itinerary(
    itinerary,
    destination,
    start_date,
    number_of_days,
    travelers,
    budget,
    interests,
    travel_style,
    weather_result=None
):
    """
    Run the complete multi-stage optimization pipeline.
    """

    validation = (
        validate_itinerary_structure(
            itinerary
        )
    )

    if not validation[
        "valid"
    ]:

        return {

            "success": False,

            "error": (
                "Invalid itinerary structure."
            ),

            "validation_errors": (
                validation[
                    "errors"
                ]
            )
        }

    daily_itinerary = (
        itinerary.get(
            "daily_itinerary",
            []
        )
    )

    # --------------------------------------------------------
    # Stage 1: Normalize
    # --------------------------------------------------------

    daily_itinerary = (
        normalize_daily_itinerary(

            daily_itinerary,

            start_date,

            number_of_days
        )
    )

    # --------------------------------------------------------
    # Stage 2: Weather
    # --------------------------------------------------------

    daily_itinerary = (
        apply_weather_to_itinerary(

            daily_itinerary,

            weather_result
        )
    )

    daily_itinerary = (
        apply_weather_activity_scores(

            daily_itinerary,

            weather_result
        )
    )

    # --------------------------------------------------------
    # Stage 3: Enrich
    # --------------------------------------------------------

    daily_itinerary = (
        enrich_activity_data(

            daily_itinerary,

            interests,

            travel_style,

            budget
        )
    )

    # --------------------------------------------------------
    # Stage 4: Time Optimization
    # --------------------------------------------------------

    daily_itinerary, time_result = (
        apply_time_optimization(

            daily_itinerary,

            weather_result
        )
    )

    # --------------------------------------------------------
    # Stage 5: Recommendation Analysis
    # --------------------------------------------------------

    try:

        recommendation_result = (
            analyze_itinerary_recommendations(

                daily_itinerary,

                interests,

                travel_style,

                weather_result,

                budget
            )
        )

    except Exception as error:

        recommendation_result = {

            "success": False,

            "error": str(error)
        }

    # --------------------------------------------------------
    # Stage 6: Location Optimization
    # --------------------------------------------------------

    try:

        location_result = (
            optimize_locations(
                daily_itinerary
            )
        )

    except Exception as error:

        location_result = {

            "success": False,

            "error": str(error),

            "distance_analysis": [],

            "long_distance_connections": [],

            "nearby_groups": [],

            "efficiency": {}
        }

    daily_itinerary = (
        apply_location_analysis(

            daily_itinerary,

            location_result
        )
    )

    # --------------------------------------------------------
    # Stage 7: Budget Optimization
    # --------------------------------------------------------

    try:

        budget_result = (
            optimize_budget(

                itinerary=itinerary,

                budget=budget,

                travelers=travelers,

                travel_style=travel_style
            )
        )

    except TypeError:

        try:

            budget_result = (
                optimize_budget(
                    itinerary,
                    budget,
                    travelers,
                    travel_style
                )
            )

        except Exception as error:

            budget_result = {

                "success": False,

                "error": str(error)
            }

    except Exception as error:

        budget_result = {

            "success": False,

            "error": str(error)
        }

    # --------------------------------------------------------
    # Stage 8: Constraint Optimization
    # --------------------------------------------------------

    try:

        constraint_result = (
            optimize_constraints(

                itinerary=daily_itinerary,

                budget=budget,

                interests=interests,

                travel_style=travel_style,

                weather_data=weather_result,

                location_data=location_result,

                time_data=time_result,

                special_requirements=""
            )
        )

    except TypeError:

        try:

            constraint_result = (
                optimize_constraints(

                    daily_itinerary,

                    budget,

                    interests,

                    travel_style,

                    weather_result,

                    location_result,

                    time_result,

                    ""
                )
            )

        except Exception as error:

            constraint_result = {

                "success": False,

                "error": str(error)
            }

    except Exception as error:

        constraint_result = {

            "success": False,

            "error": str(error)
        }

    # --------------------------------------------------------
    # Stage 9: Explanation Layer
    # --------------------------------------------------------

    try:

        explanation_result = (
            generate_itinerary_explanations(

                daily_itinerary,

                interests,

                travel_style,

                budget
            )
        )

    except Exception as error:

        explanation_result = {

            "success": False,

            "explanations": [],

            "error": str(error)
        }

    # --------------------------------------------------------
    # Stage 10: Optimization Scores
    # --------------------------------------------------------

    recommendation_score = 70

    if isinstance(
        recommendation_result,
        dict
    ):

        recommendation_score = (
            recommendation_result.get(
                "overall_score",
                recommendation_result.get(
                    "score",
                    70
                )
            )
        )

    budget_score = 70

    if isinstance(
        budget_result,
        dict
    ):

        budget_score = (
            budget_result.get(
                "optimization_score",
                budget_result.get(
                    "score",
                    70
                )
            )
        )

    location_score = 70

    if isinstance(
        location_result,
        dict
    ):

        location_score = (
            location_result.get(
                "efficiency",
                {}
            ).get(
                "score",
                70
            )
        )

    time_score = 70

    if isinstance(
        time_result,
        dict
    ):

        time_summary = (
            time_result.get(
                "summary",
                {}
            )
        )

        if isinstance(
            time_summary,
            dict
        ):

            time_score = (
                time_summary.get(
                    "score",
                    70
                )
            )

    constraint_score = 70

    if isinstance(
        constraint_result,
        dict
    ):

        constraint_score = (
            constraint_result.get(
                "overall_score",
                constraint_result.get(
                    "score",
                    70
                )
            )
        )

    weather_score = 70

    if weather_result:

        forecast = weather_result.get(
            "forecast",
            []
        )

        weather_scores = [

            item.get(
                "weather_score",
                70
            )

            for item in forecast

            if item.get(
                "weather_score"
            ) is not None
        ]

        if weather_scores:

            weather_score = (
                sum(
                    weather_scores
                )
                /
                len(
                    weather_scores
                )
            )

    optimization_explanation = (
        explain_optimization_results(

            recommendation_score,

            budget_score,

            location_score,

            weather_score,

            time_score,

            constraint_score
        )
    )

    # --------------------------------------------------------
    # Statistics
    # --------------------------------------------------------

    statistics = (
        calculate_itinerary_statistics(
            daily_itinerary
        )
    )

    # --------------------------------------------------------
    # Final Result
    # --------------------------------------------------------

    optimized_itinerary = dict(
        itinerary
    )

    optimized_itinerary[
        "daily_itinerary"
    ] = daily_itinerary

    optimized_itinerary[
        "optimization_results"
    ] = {

        "recommendation": (
            recommendation_result
        ),

        "budget": (
            budget_result
        ),

        "location": (
            location_result
        ),

        "time": (
            time_result
        ),

        "constraints": (
            constraint_result
        ),

        "weather": (
            weather_result
        ),

        "explanation": (
            explanation_result
        ),

        "optimization_explanation": (
            optimization_explanation
        )
    }

    optimized_itinerary[
        "statistics"
    ] = statistics

    return {

        "success": True,

        "itinerary": optimized_itinerary,

        "daily_itinerary": daily_itinerary,

        "recommendation_result": (
            recommendation_result
        ),

        "budget_result": (
            budget_result
        ),

        "location_result": (
            location_result
        ),

        "time_result": (
            time_result
        ),

        "constraint_result": (
            constraint_result
        ),

        "weather_result": (
            weather_result
        ),

        "explanation_result": (
            explanation_result
        ),

        "optimization_explanation": (
            optimization_explanation
        ),

        "statistics": statistics
    }


# ------------------------------------------------------------
# FINAL TRIP SUMMARY
# ------------------------------------------------------------

def generate_final_trip_summary(
    optimized_result
):
    """
    Generate a concise summary for the UI.
    """

    if not optimized_result.get(
        "success",
        False
    ):

        return (
            "Itinerary optimization was unsuccessful."
        )

    statistics = optimized_result.get(
        "statistics",
        {}
    )

    optimization = optimized_result.get(
        "optimization_explanation",
        {}
    )

    destination = (
        optimized_result
        .get(
            "itinerary",
            {}
        )
        .get(
            "trip_summary",
            {}
        )
        .get(
            "destination",
            "your destination"
        )
    )

    return (

        f"Your itinerary for {destination} "
        f"contains {statistics.get('activity_count', 0)} "
        f"planned activities across "
        f"{statistics.get('total_days', 0)} day(s). "
        f"Overall optimization quality is "
        f"{optimization.get('classification', 'Not evaluated')} "
        f"with an average score of "
        f"{optimization.get('average_score', 0):.1f}/100."
    )