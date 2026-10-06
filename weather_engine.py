def analyze_itinerary_weather(
    itinerary,
    forecast
):
    """
    Analyze weather conditions for each day of an itinerary.
    Handles both dictionary-based and string-based day entries.
    """

    results = []

    if not itinerary:
        return results

    # Build a simple forecast lookup
    forecast_map = {}

    if isinstance(forecast, list):

        for item in forecast:

            if isinstance(item, dict):

                forecast_date = item.get(
                    "date",
                    ""
                )

                if forecast_date:

                    forecast_map[
                        str(forecast_date)
                    ] = item

    elif isinstance(forecast, dict):

        forecast_map = forecast

    # Analyze every itinerary day
    for day in itinerary:

        # Convert string day into dictionary
        if isinstance(day, str):

            day = {
                "date": day,
                "activities": []
            }

        # Ignore invalid entries
        if not isinstance(day, dict):
            continue

        day_date = day.get(
            "date",
            ""
        )

        activities = day.get(
            "activities",
            []
        )

        weather = forecast_map.get(
            str(day_date),
            {}
        )

        if not isinstance(
            weather,
            dict
        ):

            weather = {}

        weather_condition = weather.get(
            "condition",
            weather.get(
                "weather",
                "Unknown"
            )
        )

        temperature = weather.get(
            "temperature",
            weather.get(
                "temperature_max",
                ""
            )
        )

        precipitation = weather.get(
            "precipitation",
            weather.get(
                "precipitation_probability",
                0
            )
        )

        # Calculate general weather risk
        try:

            precipitation_value = float(
                precipitation
            )

        except (
            TypeError,
            ValueError
        ):

            precipitation_value = 0

        if precipitation_value >= 70:

            risk_level = "High"

        elif precipitation_value >= 40:

            risk_level = "Moderate"

        else:

            risk_level = "Low"

        activity_results = []

        if isinstance(
            activities,
            list
        ):

            for activity in activities:

                if isinstance(
                    activity,
                    str
                ):

                    activity_name = activity

                elif isinstance(
                    activity,
                    dict
                ):

                    activity_name = activity.get(
                        "activity",
                        activity.get(
                            "name",
                            "Activity"
                        )
                    )

                else:

                    continue

                activity_results.append(
                    {
                        "activity": activity_name,
                        "weather_condition": weather_condition,
                        "temperature": temperature,
                        "risk_level": risk_level
                    }
                )

        results.append(
            {
                "date": day_date,
                "weather_condition": weather_condition,
                "temperature": temperature,
                "precipitation": precipitation,
                "risk_level": risk_level,
                "activities": activity_results
            }
        )

    return results


def optimize_weather(weather_data):

    if not weather_data:
        return []

    optimized_results = []

    for day in weather_data:

        if not isinstance(
            day,
            dict
        ):
            continue

        weather_condition = str(
            day.get(
                "weather_condition",
                ""
            )
        ).lower()

        risk_level = str(
            day.get(
                "risk_level",
                "Low"
            )
        ).lower()

        activities = day.get(
            "activities",
            []
        )

        # Keep all activities by default
        suitable_activities = activities

        # For rainy or high-risk weather,
        # prefer indoor activities
        if (
            "rain" in weather_condition
            or risk_level == "high"
        ):

            indoor_activities = []

            if isinstance(
                activities,
                list
            ):

                for activity in activities:

                    if isinstance(
                        activity,
                        dict
                    ):

                        activity_name = str(
                            activity.get(
                                "activity",
                                activity.get(
                                    "name",
                                    ""
                                )
                            )
                        ).lower()

                        indoor_keywords = [
                            "indoor",
                            "museum",
                            "mall",
                            "shopping",
                            "restaurant",
                            "cafe",
                            "gallery"
                        ]

                        if any(
                            word in activity_name
                            for word in indoor_keywords
                        ):

                            indoor_activities.append(
                                activity
                            )

            # Only replace the list if
            # suitable indoor activities exist
            if indoor_activities:

                suitable_activities = (
                    indoor_activities
                )

        updated_day = day.copy()

        updated_day[
            "activities"
        ] = suitable_activities

        updated_day[
            "weather_optimized"
        ] = True

        optimized_results.append(
            updated_day
        )

    return optimized_results