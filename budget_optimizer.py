# ============================================================
# ADVANCED BUDGET OPTIMIZATION ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================


# ------------------------------------------------------------
# SAFE NUMERIC CONVERSION
# ------------------------------------------------------------

def safe_float(value, default=0):
    """
    Convert different cost formats into float.
    """

    if value is None:
        return default

    if isinstance(
        value,
        (int, float)
    ):
        return float(value)

    text = str(value)

    text = (
        text
        .replace(",", "")
        .replace("₹", "")
        .replace("Rs.", "")
        .replace("Rs", "")
    )

    numbers = []

    current = ""

    for character in text:

        if (
            character.isdigit()
            or character == "."
        ):

            current += character

        else:

            if current:

                try:
                    numbers.append(
                        float(current)
                    )

                except ValueError:
                    pass

                current = ""

    if current:

        try:
            numbers.append(
                float(current)
            )

        except ValueError:
            pass

    if not numbers:

        return default

    # For ranges such as ₹500 - ₹800,
    # use the average.
    if len(numbers) >= 2:

        return (
            numbers[0]
            +
            numbers[1]
        ) / 2

    return numbers[0]


# ------------------------------------------------------------
# CALCULATE ACTIVITY COST
# ------------------------------------------------------------

def calculate_activity_cost(
    daily_itinerary
):
    """
    Calculate total activity cost
    across all travel days.
    """

    total_cost = 0

    daily_costs = []

    for day in daily_itinerary:

        day_number = day.get(
            "day",
            len(daily_costs) + 1
        )

        daily_activity_cost = 0

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

            cost = safe_float(
                section.get(
                    "cost",
                    0
                )
            )

            daily_activity_cost += cost

        declared_daily_cost = safe_float(
            day.get(
                "daily_cost",
                0
            )
        )

        # Use the larger value only when
        # the declared daily cost contains
        # information not present in sections.
        if (
            declared_daily_cost
            >
            daily_activity_cost
        ):

            daily_activity_cost = (
                declared_daily_cost
            )

        daily_costs.append(
            {
                "day": day_number,
                "activity_cost": round(
                    daily_activity_cost,
                    2
                )
            }
        )

        total_cost += (
            daily_activity_cost
        )

    return {
        "total_activity_cost": round(
            total_cost,
            2
        ),

        "daily_costs": daily_costs
    }


# ------------------------------------------------------------
# CALCULATE TOTAL COST
# ------------------------------------------------------------

def calculate_total_estimated_cost(
    daily_itinerary,
    budget_breakdown,
    travelers=1
):
    """
    Calculate complete estimated
    travel expenditure.
    """

    activity_result = (
        calculate_activity_cost(
            daily_itinerary
        )
    )

    activity_cost = (
        activity_result[
            "total_activity_cost"
        ]
    )

    accommodation_cost = safe_float(
        budget_breakdown.get(
            "accommodation",
            0
        )
    )

    food_cost = safe_float(
        budget_breakdown.get(
            "food",
            0
        )
    )

    transportation_cost = safe_float(
        budget_breakdown.get(
            "transportation",
            0
        )
    )

    miscellaneous_cost = safe_float(
        budget_breakdown.get(
            "miscellaneous",
            0
        )
    )

    # Activities are taken separately.
    # If the AI already provides an activity
    # amount in the budget breakdown, avoid
    # accidental double counting.
    declared_activities = safe_float(
        budget_breakdown.get(
            "activities",
            0
        )
    )

    if declared_activities > 0:

        activity_cost = max(
            activity_cost,
            declared_activities
        )

    total_cost = (
        accommodation_cost
        +
        food_cost
        +
        transportation_cost
        +
        activity_cost
        +
        miscellaneous_cost
    )

    travelers = max(
        int(
            safe_float(
                travelers,
                1
            )
        ),
        1
    )

    per_person_cost = (
        total_cost
        /
        travelers
    )

    return {

        "activity_cost": round(
            activity_cost,
            2
        ),

        "accommodation_cost": round(
            accommodation_cost,
            2
        ),

        "food_cost": round(
            food_cost,
            2
        ),

        "transportation_cost": round(
            transportation_cost,
            2
        ),

        "miscellaneous_cost": round(
            miscellaneous_cost,
            2
        ),

        "total_estimated_cost": round(
            total_cost,
            2
        ),

        "per_person_cost": round(
            per_person_cost,
            2
        ),

        "daily_costs": (
            activity_result[
                "daily_costs"
            ]
        )
    }


# ------------------------------------------------------------
# BUDGET STATUS
# ------------------------------------------------------------

def analyze_budget_status(
    total_budget,
    estimated_cost
):
    """
    Determine whether the itinerary
    is within the user's budget.
    """

    budget = safe_float(
        total_budget
    )

    cost = safe_float(
        estimated_cost
    )

    if budget <= 0:

        return {
            "status": "Invalid",
            "difference": 0,
            "percentage_used": 0,
            "score": 0,
            "message": (
                "Please provide a valid budget."
            )
        }

    difference = (
        budget - cost
    )

    percentage_used = (
        cost / budget
    ) * 100

    if cost <= budget:

        if percentage_used <= 70:

            status = (
                "Comfortably Within Budget"
            )

            score = 100

        elif percentage_used <= 85:

            status = (
                "Within Budget"
            )

            score = 90

        elif percentage_used <= 100:

            status = (
                "Near Budget Limit"
            )

            score = 80

        else:

            status = "Unknown"

            score = 70

        message = (
            "The estimated travel cost "
            "fits within the selected budget."
        )

    else:

        excess_percentage = (
            (cost - budget)
            /
            budget
        ) * 100

        if excess_percentage <= 10:

            status = (
                "Slightly Over Budget"
            )

            score = 60

        elif excess_percentage <= 25:

            status = "Over Budget"

            score = 40

        else:

            status = (
                "Significantly Over Budget"
            )

            score = 20

        message = (
            "The estimated travel cost "
            "exceeds the selected budget."
        )

    return {

        "status": status,

        "difference": round(
            difference,
            2
        ),

        "percentage_used": round(
            percentage_used,
            2
        ),

        "score": score,

        "message": message
    }


# ------------------------------------------------------------
# COST CATEGORY ANALYSIS
# ------------------------------------------------------------

def analyze_cost_categories(
    cost_analysis
):
    """
    Analyze how the travel budget
    is distributed across categories.
    """

    total = safe_float(
        cost_analysis.get(
            "total_estimated_cost",
            0
        )
    )

    if total <= 0:

        return {}

    categories = {

        "Accommodation": (
            cost_analysis.get(
                "accommodation_cost",
                0
            )
        ),

        "Food": (
            cost_analysis.get(
                "food_cost",
                0
            )
        ),

        "Transportation": (
            cost_analysis.get(
                "transportation_cost",
                0
            )
        ),

        "Activities": (
            cost_analysis.get(
                "activity_cost",
                0
            )
        ),

        "Miscellaneous": (
            cost_analysis.get(
                "miscellaneous_cost",
                0
            )
        )
    }

    result = {}

    for category, value in (
        categories.items()
    ):

        numeric_value = safe_float(
            value
        )

        percentage = (
            numeric_value
            /
            total
        ) * 100

        result[category] = {

            "amount": round(
                numeric_value,
                2
            ),

            "percentage": round(
                percentage,
                2
            )
        }

    return result


# ------------------------------------------------------------
# IDENTIFY EXPENSIVE CATEGORIES
# ------------------------------------------------------------

def identify_expensive_categories(
    category_analysis
):
    """
    Find categories consuming
    a large portion of the budget.
    """

    expensive = []

    for category, data in (
        category_analysis.items()
    ):

        percentage = safe_float(
            data.get(
                "percentage",
                0
            )
        )

        if percentage >= 30:

            expensive.append(
                {
                    "category": category,
                    "percentage": percentage,
                    "amount": data.get(
                        "amount",
                        0
                    )
                }
            )

    expensive.sort(
        key=lambda item: item[
            "percentage"
        ],
        reverse=True
    )

    return expensive


# ------------------------------------------------------------
# BUDGET SAVING STRATEGIES
# ------------------------------------------------------------

def generate_budget_suggestions(
    budget_status,
    category_analysis,
    travel_style
):
    """
    Generate intelligent strategies
    for controlling travel expenses.
    """

    suggestions = []

    status = budget_status.get(
        "status",
        ""
    )

    if status in [
        "Comfortably Within Budget",
        "Within Budget"
    ]:

        suggestions.append(
            "The current itinerary is within "
            "the selected budget."
        )

        if travel_style == "Budget":

            suggestions.append(
                "Continue prioritizing public "
                "transportation, local food and "
                "budget accommodation."
            )

        elif travel_style == "Luxury":

            suggestions.append(
                "The remaining budget can be "
                "used for selected premium experiences."
            )

        return suggestions

    expensive_categories = (
        identify_expensive_categories(
            category_analysis
        )
    )

    for item in expensive_categories:

        category = item[
            "category"
        ]

        if category == "Accommodation":

            suggestions.append(
                "Choose accommodation in "
                "well-connected areas with "
                "better price-to-value ratio."
            )

        elif category == "Transportation":

            suggestions.append(
                "Use public transportation, "
                "shared mobility or walkable "
                "routes where practical."
            )

        elif category == "Food":

            suggestions.append(
                "Prefer local restaurants, "
                "regional food and affordable "
                "dining options."
            )

        elif category == "Activities":

            suggestions.append(
                "Replace selected expensive "
                "activities with free or "
                "lower-cost attractions."
            )

        elif category == "Miscellaneous":

            suggestions.append(
                "Reduce unnecessary miscellaneous "
                "expenses and reserve a smaller "
                "emergency allowance."
            )

    if not suggestions:

        suggestions.append(
            "Reduce high-cost activities and "
            "transportation expenses."
        )

    suggestions.append(
        "Group nearby attractions together "
        "to reduce transportation costs."
    )

    suggestions.append(
        "Prioritize activities that provide "
        "high personal value for their cost."
    )

    return suggestions


# ------------------------------------------------------------
# OPTIMIZATION POTENTIAL
# ------------------------------------------------------------

def calculate_saving_potential(
    total_budget,
    estimated_cost
):
    """
    Estimate how much cost reduction
    may be required.
    """

    budget = safe_float(
        total_budget
    )

    cost = safe_float(
        estimated_cost
    )

    if budget <= 0:

        return {
            "required_reduction": 0,
            "percentage_reduction": 0
        }

    if cost <= budget:

        return {
            "required_reduction": 0,
            "percentage_reduction": 0
        }

    reduction = (
        cost - budget
    )

    percentage = (
        reduction / cost
    ) * 100

    return {

        "required_reduction": round(
            reduction,
            2
        ),

        "percentage_reduction": round(
            percentage,
            2
        )
    }


# ------------------------------------------------------------
# BUDGET OPTIMIZATION SCORE
# ------------------------------------------------------------

def calculate_budget_optimization_score(
    budget_status,
    category_analysis
):
    """
    Calculate an overall budget efficiency score.
    """

    budget_score = safe_float(
        budget_status.get(
            "score",
            0
        )
    )

    category_score = 100

    expensive_categories = (
        identify_expensive_categories(
            category_analysis
        )
    )

    if len(
        expensive_categories
    ) >= 3:

        category_score = 60

    elif len(
        expensive_categories
    ) == 2:

        category_score = 75

    elif len(
        expensive_categories
    ) == 1:

        category_score = 90

    final_score = (
        budget_score * 0.70
        +
        category_score * 0.30
    )

    return round(
        final_score,
        2
    )


# ------------------------------------------------------------
# MAIN BUDGET OPTIMIZER
# ------------------------------------------------------------

def optimize_budget(
    total_budget,
    daily_itinerary,
    budget_breakdown,
    travelers=1,
    travel_style="Standard"
):
    """
    Complete budget optimization pipeline.
    """

    if budget_breakdown is None:

        budget_breakdown = {}

    cost_analysis = (
        calculate_total_estimated_cost(
            daily_itinerary=(
                daily_itinerary or []
            ),
            budget_breakdown=(
                budget_breakdown
            ),
            travelers=travelers
        )
    )

    estimated_cost = (
        cost_analysis[
            "total_estimated_cost"
        ]
    )

    budget_status = (
        analyze_budget_status(
            total_budget,
            estimated_cost
        )
    )

    category_analysis = (
        analyze_cost_categories(
            cost_analysis
        )
    )

    expensive_categories = (
        identify_expensive_categories(
            category_analysis
        )
    )

    saving_potential = (
        calculate_saving_potential(
            total_budget,
            estimated_cost
        )
    )

    optimization_score = (
        calculate_budget_optimization_score(
            budget_status,
            category_analysis
        )
    )

    suggestions = (
        generate_budget_suggestions(
            budget_status,
            category_analysis,
            travel_style
        )
    )

    return {

        "user_budget": round(
            safe_float(
                total_budget
            ),
            2
        ),

        "estimated_cost": round(
            estimated_cost,
            2
        ),

        "remaining_budget": round(
            safe_float(
                total_budget
            )
            -
            estimated_cost,
            2
        ),

        "per_person_cost": (
            cost_analysis[
                "per_person_cost"
            ]
        ),

        "cost_analysis": cost_analysis,

        "category_analysis": (
            category_analysis
        ),

        "expensive_categories": (
            expensive_categories
        ),

        "budget_status": (
            budget_status
        ),

        "saving_potential": (
            saving_potential
        ),

        "optimization_score": (
            optimization_score
        ),

        "optimization_suggestions": (
            suggestions
        )
    }


# ------------------------------------------------------------
# BUDGET SUMMARY
# ------------------------------------------------------------

def generate_budget_summary(
    budget_result
):
    """
    Generate a concise budget summary.
    """

    if not budget_result:

        return (
            "Budget optimization unavailable."
        )

    budget = safe_float(
        budget_result.get(
            "user_budget",
            0
        )
    )

    estimated = safe_float(
        budget_result.get(
            "estimated_cost",
            0
        )
    )

    remaining = safe_float(
        budget_result.get(
            "remaining_budget",
            0
        )
    )

    status = (
        budget_result
        .get(
            "budget_status",
            {}
        )
        .get(
            "status",
            "Unknown"
        )
    )

    score = safe_float(
        budget_result.get(
            "optimization_score",
            0
        )
    )

    if remaining >= 0:

        remaining_text = (
            f"₹{remaining:,.0f} remaining"
        )

    else:

        remaining_text = (
            f"₹{abs(remaining):,.0f} over budget"
        )

    return (
        f"Budget Status: {status}. "
        f"Estimated Cost: ₹{estimated:,.0f}. "
        f"Budget: ₹{budget:,.0f}. "
        f"{remaining_text}. "
        f"Budget Optimization Score: "
        f"{score:.1f}/100."
    )