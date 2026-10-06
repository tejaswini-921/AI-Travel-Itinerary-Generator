# ============================================================
# ADVANCED LOCATION & DISTANCE OPTIMIZATION ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================

import requests
from math import radians, sin, cos, sqrt, atan2


GEOCODING_URL = (
    "https://geocoding-api.open-meteo.com/v1/search"
)


# ------------------------------------------------------------
# GEOCODING
# ------------------------------------------------------------

def geocode_place(place_name):
    """
    Convert a place name into approximate
    geographical coordinates.
    """

    if not place_name:

        return None

    try:

        params = {
            "name": place_name,
            "count": 1,
            "language": "en",
            "format": "json"
        }

        response = requests.get(
            GEOCODING_URL,
            params=params,
            timeout=15
        )

        if response.status_code != 200:

            return None

        data = response.json()

        results = data.get(
            "results",
            []
        )

        if not results:

            return None

        location = results[0]

        return {
            "name": location.get(
                "name",
                place_name
            ),

            "latitude": location.get(
                "latitude"
            ),

            "longitude": location.get(
                "longitude"
            ),

            "country": location.get(
                "country",
                ""
            )
        }

    except Exception:

        return None


# ------------------------------------------------------------
# HAVERSINE DISTANCE
# ------------------------------------------------------------

def calculate_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):
    """
    Calculate approximate geographical
    distance between two coordinates.
    """

    if None in [
        latitude1,
        longitude1,
        latitude2,
        longitude2
    ]:

        return None

    earth_radius = 6371.0

    lat1 = radians(
        latitude1
    )

    lat2 = radians(
        latitude2
    )

    difference_latitude = radians(
        latitude2 - latitude1
    )

    difference_longitude = radians(
        longitude2 - longitude1
    )

    a = (
        sin(
            difference_latitude / 2
        ) ** 2

        +

        cos(lat1)
        *
        cos(lat2)
        *
        sin(
            difference_longitude / 2
        ) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    distance = (
        earth_radius * c
    )

    return round(
        distance,
        2
    )


# ------------------------------------------------------------
# DISTANCE CLASSIFICATION
# ------------------------------------------------------------

def classify_distance(
    distance
):
    """
    Classify geographical distance.
    """

    if distance is None:

        return "Unknown"

    if distance <= 2:

        return "Very Close"

    if distance <= 5:

        return "Nearby"

    if distance <= 10:

        return "Moderate Distance"

    if distance <= 20:

        return "Far"

    return "Very Far"


# ------------------------------------------------------------
# DISTANCE EFFICIENCY SCORE
# ------------------------------------------------------------

def calculate_distance_score(
    distance
):
    """
    Convert distance into an efficiency score.
    """

    if distance is None:

        return 50

    if distance <= 2:

        return 100

    if distance <= 5:

        return 95

    if distance <= 10:

        return 85

    if distance <= 20:

        return 70

    if distance <= 30:

        return 55

    if distance <= 50:

        return 40

    return 20


# ------------------------------------------------------------
# PLACE-TO-PLACE DISTANCE
# ------------------------------------------------------------

def calculate_place_distance(
    place1,
    place2
):
    """
    Calculate distance between two named places.
    """

    location1 = geocode_place(
        place1
    )

    location2 = geocode_place(
        place2
    )

    if (
        not location1
        or not location2
    ):

        return {
            "success": False,
            "place1": place1,
            "place2": place2,
            "distance": None,
            "classification": "Unknown",
            "score": 50
        }

    distance = calculate_distance(
        location1[
            "latitude"
        ],

        location1[
            "longitude"
        ],

        location2[
            "latitude"
        ],

        location2[
            "longitude"
        ]
    )

    return {

        "success": True,

        "place1": place1,

        "place2": place2,

        "distance": distance,

        "classification": (
            classify_distance(
                distance
            )
        ),

        "score": (
            calculate_distance_score(
                distance
            )
        )
    }


# ------------------------------------------------------------
# EXTRACT ITINERARY PLACES
# ------------------------------------------------------------

def extract_itinerary_places(
    daily_itinerary
):
    """
    Extract all places from the itinerary.
    """

    places = []

    for day in daily_itinerary:

        day_number = day.get(
            "day",
            len(places) + 1
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

            place = section.get(
                "place",
                ""
            )

            activity = section.get(
                "activity",
                ""
            )

            if place:

                places.append(
                    {
                        "day": day_number,

                        "time": time_slot,

                        "place": place,

                        "activity": activity
                    }
                )

    return places


# ------------------------------------------------------------
# GEOCODE ITINERARY
# ------------------------------------------------------------

def geocode_itinerary_places(
    daily_itinerary
):
    """
    Geocode itinerary places with caching.
    """

    places = (
        extract_itinerary_places(
            daily_itinerary
        )
    )

    geocoded_places = []

    cache = {}

    for item in places:

        place = item[
            "place"
        ]

        if place in cache:

            location = cache[
                place
            ]

        else:

            location = geocode_place(
                place
            )

            cache[
                place
            ] = location

        geocoded_places.append(
            {
                **item,
                "location": location
            }
        )

    return geocoded_places


# ------------------------------------------------------------
# DAILY DISTANCE ANALYSIS
# ------------------------------------------------------------

def analyze_daily_distances(
    daily_itinerary
):
    """
    Calculate travel distance between
    consecutive attractions on each day.
    """

    geocoded_places = (
        geocode_itinerary_places(
            daily_itinerary
        )
    )

    days = {}

    for item in geocoded_places:

        day_number = item[
            "day"
        ]

        if day_number not in days:

            days[
                day_number
            ] = []

        days[
            day_number
        ].append(
            item
        )

    results = []

    for day_number, items in (
        days.items()
    ):

        day_distances = []

        for index in range(
            len(items) - 1
        ):

            first = items[
                index
            ]

            second = items[
                index + 1
            ]

            location1 = first.get(
                "location"
            )

            location2 = second.get(
                "location"
            )

            if (
                location1
                and
                location2
            ):

                distance = calculate_distance(

                    location1.get(
                        "latitude"
                    ),

                    location1.get(
                        "longitude"
                    ),

                    location2.get(
                        "latitude"
                    ),

                    location2.get(
                        "longitude"
                    )
                )

                day_distances.append(
                    {
                        "from": first[
                            "place"
                        ],

                        "to": second[
                            "place"
                        ],

                        "distance_km": distance,

                        "classification": (
                            classify_distance(
                                distance
                            )
                        ),

                        "efficiency_score": (
                            calculate_distance_score(
                                distance
                            )
                        )
                    }
                )

        total_distance = sum(
            item.get(
                "distance_km",
                0
            ) or 0

            for item in day_distances
        )

        if day_distances:

            average_score = (
                sum(
                    item.get(
                        "efficiency_score",
                        0
                    )

                    for item in day_distances
                )

                /

                len(day_distances)
            )

        else:

            average_score = 100

        results.append(
            {
                "day": day_number,

                "total_distance_km": round(
                    total_distance,
                    2
                ),

                "average_efficiency_score": round(
                    average_score,
                    2
                ),

                "connections": day_distances
            }
        )

    return results


# ------------------------------------------------------------
# LONG DISTANCE DETECTION
# ------------------------------------------------------------

def identify_long_distance_travel(
    distance_analysis,
    threshold_km=10
):
    """
    Identify inefficient long-distance
    connections.
    """

    long_distance = []

    for day in distance_analysis:

        day_number = day.get(
            "day"
        )

        for connection in day.get(
            "connections",
            []
        ):

            distance = connection.get(
                "distance_km",
                0
            )

            if (
                distance is not None
                and distance > threshold_km
            ):

                long_distance.append(
                    {
                        "day": day_number,

                        "from": connection.get(
                            "from",
                            ""
                        ),

                        "to": connection.get(
                            "to",
                            ""
                        ),

                        "distance_km": distance,

                        "classification": (
                            classify_distance(
                                distance
                            )
                        )
                    }
                )

    return long_distance


# ------------------------------------------------------------
# NEARBY PLACE GROUPING
# ------------------------------------------------------------

def group_nearby_places(
    places,
    proximity_km=10
):
    """
    Group attractions that are geographically
    close to each other.
    """

    if not places:

        return []

    groups = []

    used = set()

    for index, place in enumerate(
        places
    ):

        if index in used:

            continue

        current_group = [
            place
        ]

        used.add(
            index
        )

        location1 = place.get(
            "location"
        )

        if not location1:

            continue

        for other_index in range(
            index + 1,
            len(places)
        ):

            if other_index in used:

                continue

            other = places[
                other_index
            ]

            location2 = other.get(
                "location"
            )

            if not location2:

                continue

            distance = calculate_distance(

                location1.get(
                    "latitude"
                ),

                location1.get(
                    "longitude"
                ),

                location2.get(
                    "latitude"
                ),

                location2.get(
                    "longitude"
                )
            )

            if (
                distance is not None
                and distance <= proximity_km
            ):

                current_group.append(
                    other
                )

                used.add(
                    other_index
                )

        groups.append(
            {
                "group_id": (
                    len(groups) + 1
                ),

                "places": current_group,

                "size": len(
                    current_group
                )
            }
        )

    return groups


# ------------------------------------------------------------
# DAILY EFFICIENCY
# ------------------------------------------------------------

def calculate_daily_efficiency(
    distance_analysis
):
    """
    Calculate overall geographical efficiency.
    """

    if not distance_analysis:

        return {
            "score": 100,
            "status": "No distance data"
        }

    scores = []

    for day in distance_analysis:

        score = day.get(
            "average_efficiency_score",
            70
        )

        scores.append(
            score
        )

    if not scores:

        return {
            "score": 70,
            "status": "No distance data"
        }

    overall_score = (
        sum(scores)
        /
        len(scores)
    )

    if overall_score >= 90:

        status = "Highly Efficient"

    elif overall_score >= 75:

        status = "Efficient"

    elif overall_score >= 55:

        status = "Moderately Efficient"

    else:

        status = "Travel Distance Needs Optimization"

    return {
        "score": round(
            overall_score,
            2
        ),

        "status": status
    }


# ------------------------------------------------------------
# LOCATION SUGGESTIONS
# ------------------------------------------------------------

def generate_location_suggestions(
    distance_analysis,
    long_distance_connections
):
    """
    Generate practical location optimization
    suggestions.
    """

    suggestions = []

    for day in distance_analysis:

        day_number = day.get(
            "day"
        )

        total_distance = day.get(
            "total_distance_km",
            0
        )

        if total_distance > 30:

            suggestions.append(
                f"Day {day_number}: "
                "High intra-day travel detected. "
                "Group nearby attractions together."
            )

        elif total_distance > 15:

            suggestions.append(
                f"Day {day_number}: "
                "Moderate travel distance detected. "
                "Consider rearranging attractions."
            )

        else:

            suggestions.append(
                f"Day {day_number}: "
                "Attractions are reasonably grouped."
            )

    if long_distance_connections:

        suggestions.append(
            "Long-distance connections were detected. "
            "Consider replacing or rearranging "
            "distant attractions."
        )

    else:

        suggestions.append(
            "No major long-distance connections "
            "were detected."
        )

    return suggestions


# ------------------------------------------------------------
# MAIN LOCATION OPTIMIZER
# ------------------------------------------------------------

def optimize_locations(
    daily_itinerary,
    proximity_km=10
):
    """
    Complete location optimization pipeline.
    """

    if not daily_itinerary:

        return {

            "success": False,

            "message": (
                "No itinerary available "
                "for location optimization."
            ),

            "distance_analysis": [],

            "long_distance_connections": [],

            "nearby_groups": [],

            "efficiency": {},

            "suggestions": []
        }

    geocoded_places = (
        geocode_itinerary_places(
            daily_itinerary
        )
    )

    distance_analysis = (
        analyze_daily_distances(
            daily_itinerary
        )
    )

    long_distance_connections = (
        identify_long_distance_travel(
            distance_analysis
        )
    )

    nearby_groups = (
        group_nearby_places(
            geocoded_places,
            proximity_km
        )
    )

    efficiency = (
        calculate_daily_efficiency(
            distance_analysis
        )
    )

    suggestions = (
        generate_location_suggestions(
            distance_analysis,
            long_distance_connections
        )
    )

    return {

        "success": True,

        "geocoded_places": (
            geocoded_places
        ),

        "distance_analysis": (
            distance_analysis
        ),

        "long_distance_connections": (
            long_distance_connections
        ),

        "nearby_groups": (
            nearby_groups
        ),

        "efficiency": efficiency,

        "suggestions": suggestions
    }


# ------------------------------------------------------------
# LOCATION SUMMARY
# ------------------------------------------------------------

def generate_location_summary(
    location_result
):
    """
    Generate a concise location optimization summary.
    """

    if not location_result.get(
        "success",
        False
    ):

        return (
            "Location optimization is unavailable."
        )

    distance_analysis = (
        location_result.get(
            "distance_analysis",
            []
        )
    )

    total_distance = 0

    for day in distance_analysis:

        total_distance += (
            day.get(
                "total_distance_km",
                0
            )

            or

            0
        )

    long_connections = len(
        location_result.get(
            "long_distance_connections",
            []
        )
    )

    efficiency = (
        location_result.get(
            "efficiency",
            {}
        )
    )

    efficiency_score = efficiency.get(
        "score",
        0
    )

    efficiency_status = efficiency.get(
        "status",
        "Unknown"
    )

    return (
        f"Estimated intra-day travel distance: "
        f"{total_distance:.2f} km. "
        f"Long-distance connections: "
        f"{long_connections}. "
        f"Location efficiency: "
        f"{efficiency_score:.1f}/100 "
        f"({efficiency_status})."
    )