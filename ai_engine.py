# ============================================================
# AI ENGINE
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================

import os
import json
import requests
from dotenv import load_dotenv


load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_API_URL = (
    "https://api.groq.com/openai/v1/chat/completions"
)


# ------------------------------------------------------------
# AI MODEL CONFIGURATION
# ------------------------------------------------------------

# This can be changed if Groq changes model availability.
DEFAULT_MODEL = "openai/gpt-oss-20b"


# ------------------------------------------------------------
# BUILD TRAVEL PLANNING PROMPT
# ------------------------------------------------------------

def build_travel_prompt(
    destination,
    start_date,
    number_of_days,
    travelers,
    budget,
    interests,
    travel_style,
    transportation,
    accommodation,
    special_requirements,
    weather_data=None
):
    """
    Create a structured AI prompt for travel itinerary generation.
    """

    weather_information = "Weather forecast unavailable."

    if weather_data:

        if weather_data.get("success"):

            weather_information = json.dumps(
                weather_data.get(
                    "forecast",
                    []
                ),
                indent=2
            )

    prompt = f"""
You are an advanced AI Travel Planning and Optimization System.

Your task is to generate a highly personalized and practical
travel itinerary using artificial intelligence.

TRAVELER INFORMATION
--------------------
Destination: {destination}
Travel Start Date: {start_date}
Number of Days: {number_of_days}
Number of Travelers: {travelers}
Total Budget: INR {budget}

INTERESTS
---------
{", ".join(interests)}

TRAVEL STYLE
------------
{travel_style}

TRANSPORTATION PREFERENCE
-------------------------
{transportation}

ACCOMMODATION PREFERENCE
------------------------
{accommodation}

SPECIAL REQUIREMENTS
--------------------
{special_requirements}

WEATHER INFORMATION
-------------------
{weather_information}


IMPORTANT OPTIMIZATION OBJECTIVES
---------------------------------

1. PERSONALIZATION
   Select activities that strongly match the traveler's interests
   and travel style.

2. BUDGET OPTIMIZATION
   Keep the complete estimated trip cost within the user's budget
   whenever realistically possible.

3. LOCATION OPTIMIZATION
   Prefer attractions that are geographically close to each other
   on the same day.

4. TIME OPTIMIZATION
   Assign activities intelligently to morning, afternoon and evening.

5. WEATHER AWARENESS
   If rain or extreme heat is expected, prefer suitable indoor or
   weather-safe activities.

6. TRAVEL EFFICIENCY
   Avoid unnecessary long-distance movement between attractions.

7. SPECIAL REQUIREMENTS
   Strictly consider all user-provided requirements.

8. REALISTIC PLANNING
   Do not overload a single day with too many activities.

9. EXPLAINABILITY
   Provide a short explanation for why important activities were
   selected.

10. COST AWARENESS
    Provide approximate costs in Indian Rupees.


OUTPUT FORMAT
-------------

Return ONLY valid JSON.

Use exactly this structure:

{{
    "trip_summary": {{
        "destination": "",
        "duration": 0,
        "travelers": 0,
        "estimated_total_cost": 0,
        "planning_strategy": ""
    }},

    "daily_itinerary": [
        {{
            "day": 1,
            "date": "",
            "weather_note": "",
            "morning": {{
                "place": "",
                "activity": "",
                "duration": "",
                "cost": 0,
                "reason": ""
            }},
            "afternoon": {{
                "place": "",
                "activity": "",
                "duration": "",
                "cost": 0,
                "reason": ""
            }},
            "evening": {{
                "place": "",
                "activity": "",
                "duration": "",
                "cost": 0,
                "reason": ""
            }},
            "daily_cost": 0
        }}
    ],

    "accommodation": [
        {{
            "area": "",
            "type": "",
            "estimated_cost_per_night": 0,
            "reason": ""
        }}
    ],

    "food_recommendations": [
        {{
            "food": "",
            "type": "",
            "estimated_cost": 0,
            "reason": ""
        }}
    ],

    "transportation": [
        {{
            "mode": "",
            "estimated_cost": 0,
            "reason": ""
        }}
    ],

    "budget_breakdown": {{
        "accommodation": 0,
        "food": 0,
        "transportation": 0,
        "activities": 0,
        "miscellaneous": 0
    }},

    "packing_checklist": [],

    "travel_tips": [],

    "optimization_summary": {{
        "budget_strategy": "",
        "location_strategy": "",
        "weather_strategy": "",
        "time_strategy": ""
    }}
}}

IMPORTANT:
- Return JSON only.
- Do not use Markdown.
- Do not add explanations outside JSON.
- Keep costs realistic and approximate.
- Do not claim exact prices.
- Do not invent real-time information.
"""

    return prompt


# ------------------------------------------------------------
# CALL GROQ AI
# ------------------------------------------------------------

def call_groq_ai(
    prompt,
    model=DEFAULT_MODEL
):
    """
    Send the travel planning prompt to Groq AI.
    """

    if not GROQ_API_KEY:

        return {
            "success": False,
            "error": (
                "GROQ_API_KEY is missing. "
                "Please configure the .env file."
            )
        }

    headers = {
        "Authorization": (
            f"Bearer {GROQ_API_KEY}"
        ),
        "Content-Type": "application/json"
    }

    payload = {

        "model": model,

        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an advanced AI travel "
                    "planning and optimization assistant. "
                    "Always follow the requested JSON structure."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        "temperature": 0.4,

        "max_tokens": 7000
    }

    try:

        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=180
        )

        if response.status_code != 200:

            try:
                error_data = response.json()

            except Exception:

                error_data = response.text

            return {
                "success": False,
                "status_code": response.status_code,
                "error": error_data
            }

        response_data = response.json()

        choices = response_data.get(
            "choices",
            []
        )

        if not choices:

            return {
                "success": False,
                "error": (
                    "AI returned no response."
                )
            }

        content = (
            choices[0]
            .get("message", {})
            .get("content", "")
        )

        if not content:

            return {
                "success": False,
                "error": (
                    "AI response content is empty."
                )
            }

        return {
            "success": True,
            "content": content,
            "raw_response": response_data
        }

    except requests.exceptions.Timeout:

        return {
            "success": False,
            "error": (
                "AI request timed out. "
                "Please try again."
            )
        }

    except requests.exceptions.RequestException as error:

        return {
            "success": False,
            "error": (
                f"Network error: {str(error)}"
            )
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


# ------------------------------------------------------------
# CLEAN AI JSON RESPONSE
# ------------------------------------------------------------

def clean_json_response(content):
    """
    Clean common formatting issues from AI output.
    """

    if not content:

        return ""

    content = content.strip()

    if content.startswith("```json"):

        content = content[
            len("```json"):
        ]

    elif content.startswith("```"):

        content = content[
            len("```"):
        ]

    if content.endswith("```"):

        content = content[
            :-len("```")
        ]

    return content.strip()


# ------------------------------------------------------------
# PARSE AI RESPONSE
# ------------------------------------------------------------

def parse_ai_response(content):
    """
    Convert AI JSON response into a Python dictionary.
    """

    try:

        cleaned_content = (
            clean_json_response(
                content
            )
        )

        parsed_data = json.loads(
            cleaned_content
        )

        if not isinstance(
            parsed_data,
            dict
        ):

            return {
                "success": False,
                "error": (
                    "AI response is not "
                    "a valid JSON object."
                )
            }

        return {
            "success": True,
            "data": parsed_data
        }

    except json.JSONDecodeError as error:

        return {
            "success": False,
            "error": (
                "AI returned invalid JSON: "
                f"{str(error)}"
            ),
            "raw_content": content
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


# ------------------------------------------------------------
# GENERATE TRAVEL PLAN
# ------------------------------------------------------------

def generate_ai_travel_plan(
    destination,
    start_date,
    number_of_days,
    travelers,
    budget,
    interests,
    travel_style,
    transportation,
    accommodation,
    special_requirements,
    weather_data=None
):
    """
    Main AI travel planning pipeline.
    """

    prompt = build_travel_prompt(
        destination=destination,
        start_date=start_date,
        number_of_days=number_of_days,
        travelers=travelers,
        budget=budget,
        interests=interests,
        travel_style=travel_style,
        transportation=transportation,
        accommodation=accommodation,
        special_requirements=special_requirements,
        weather_data=weather_data
    )

    ai_result = call_groq_ai(
        prompt
    )

    if not ai_result.get(
        "success",
        False
    ):

        return ai_result

    parsed_result = parse_ai_response(
        ai_result.get(
            "content",
            ""
        )
    )

    if not parsed_result.get(
        "success",
        False
    ):

        return parsed_result

    return {
        "success": True,

        "data": parsed_result.get(
            "data",
            {}
        ),

        "model": DEFAULT_MODEL
    }


# ------------------------------------------------------------
# VALIDATE AI ITINERARY
# ------------------------------------------------------------

def validate_ai_itinerary(
    itinerary_data
):
    """
    Validate important sections of the AI-generated plan.
    """

    if not isinstance(
        itinerary_data,
        dict
    ):

        return False

    required_sections = [
        "trip_summary",
        "daily_itinerary",
        "budget_breakdown"
    ]

    for section in required_sections:

        if section not in itinerary_data:

            return False

    if not isinstance(
        itinerary_data.get(
            "daily_itinerary"
        ),
        list
    ):

        return False

    return True