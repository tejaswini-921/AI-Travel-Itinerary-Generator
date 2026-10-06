# ============================================================
# PDF GENERATOR
# Automated Travel Itinerary Generation Using Artificial Intelligence
# ============================================================

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    KeepTogether
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import simpleSplit

import os
from datetime import datetime


# ============================================================
# SAFE VALUE HELPERS
# ============================================================

def safe_value(value, default="N/A"):
    """
    Safely convert values into printable text.
    """
    if value is None:
        return default

    if isinstance(value, float):
        return f"{value:.2f}"

    return str(value)


def safe_number(value, default=0):
    """
    Safely convert values into numbers.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def format_currency(value):
    """
    Format amount as Indian Rupees.
    """
    amount = safe_number(value)

    if amount == int(amount):
        return f"INR {int(amount):,}"

    return f"INR {amount:,.2f}"


# ============================================================
# PDF STYLES
# ============================================================

def create_pdf_styles():
    """
    Create professional PDF styles.
    """

    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="MainTitle",
            parent=styles["Title"],
            fontSize=22,
            leading=28,
            alignment=TA_CENTER,
            spaceAfter=12,
            textColor=HexColor("#17365D")
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubTitle",
            parent=styles["Normal"],
            fontSize=11,
            leading=16,
            alignment=TA_CENTER,
            spaceAfter=18,
            textColor=HexColor("#555555")
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionHeading",
            parent=styles["Heading2"],
            fontSize=15,
            leading=20,
            spaceBefore=12,
            spaceAfter=8,
            textColor=HexColor("#17365D")
        )
    )

    styles.add(
        ParagraphStyle(
            name="SubHeading",
            parent=styles["Heading3"],
            fontSize=11,
            leading=15,
            spaceBefore=8,
            spaceAfter=5,
            textColor=HexColor("#2F5597")
        )
    )

    styles.add(
        ParagraphStyle(
            name="BodyTextCustom",
            parent=styles["BodyText"],
            fontSize=9,
            leading=14,
            spaceAfter=5
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallText",
            parent=styles["BodyText"],
            fontSize=7.5,
            leading=10
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableText",
            parent=styles["BodyText"],
            fontSize=7.5,
            leading=10
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            parent=styles["BodyText"],
            fontSize=8,
            leading=10,
            textColor=colors.white,
            alignment=TA_CENTER
        )
    )

    styles.add(
        ParagraphStyle(
            name="ExplanationText",
            parent=styles["BodyText"],
            fontSize=8,
            leading=12,
            leftIndent=8,
            rightIndent=8
        )
    )

    return styles


# ============================================================
# PARAGRAPH HELPER
# ============================================================

def make_paragraph(text, style):
    """
    Create a safe ReportLab paragraph.
    """

    if text is None:
        text = ""

    text = str(text)

    # Escape characters that may interfere with ReportLab markup
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    return Paragraph(text, style)


# ============================================================
# PAGE NUMBER
# ============================================================

def add_page_number(canvas, document):
    """
    Add page number to every PDF page.
    """

    canvas.saveState()

    page_number = canvas.getPageNumber()

    canvas.setFont("Helvetica", 8)

    canvas.drawRightString(
        A4[0] - 15 * mm,
        10 * mm,
        f"Page {page_number}"
    )

    canvas.drawString(
        15 * mm,
        10 * mm,
        "AI Travel Itinerary Generator"
    )

    canvas.restoreState()


# ============================================================
# COVER PAGE
# ============================================================

def build_cover_page(story, data, styles):
    """
    Create professional cover page.
    """

    story.append(Spacer(1, 35 * mm))

    story.append(
        make_paragraph(
            "AI TRAVEL ITINERARY GENERATOR",
            styles["MainTitle"]
        )
    )

    story.append(
        make_paragraph(
            "Automated Travel Itinerary Generation Using Artificial Intelligence",
            styles["SubTitle"]
        )
    )

    story.append(Spacer(1, 10 * mm))

    summary = data.get("trip_summary", {})

    destination = summary.get(
        "destination",
        data.get("destination", "Travel Destination")
    )

    duration = summary.get(
        "duration",
        data.get("number_of_days", "N/A")
    )

    travelers = summary.get(
        "travelers",
        data.get("travelers", "N/A")
    )

    budget = data.get(
        "budget",
        summary.get("budget", 0)
    )

    cover_data = [
        [
            make_paragraph("<b>Destination</b>", styles["TableText"]),
            make_paragraph(
                safe_value(destination),
                styles["TableText"]
            )
        ],
        [
            make_paragraph("<b>Duration</b>", styles["TableText"]),
            make_paragraph(
                f"{safe_value(duration)} days",
                styles["TableText"]
            )
        ],
        [
            make_paragraph("<b>Travelers</b>", styles["TableText"]),
            make_paragraph(
                safe_value(travelers),
                styles["TableText"]
            )
        ],
        [
            make_paragraph("<b>Total Budget</b>", styles["TableText"]),
            make_paragraph(
                format_currency(budget),
                styles["TableText"]
            )
        ],
        [
            make_paragraph("<b>Generated On</b>", styles["TableText"]),
            make_paragraph(
                datetime.now().strftime("%d-%m-%Y %H:%M"),
                styles["TableText"]
            )
        ]
    ]

    table = Table(
        cover_data,
        colWidths=[55 * mm, 95 * mm]
    )

    table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("BACKGROUND", (0, 0), (0, -1), HexColor("#EAF2F8")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(table)

    story.append(Spacer(1, 18 * mm))

    story.append(
        make_paragraph(
            "This personalized travel plan is generated using "
            "AI-based recommendation, budget, weather, location, "
            "time and constraint optimization techniques.",
            styles["BodyTextCustom"]
        )
    )

    story.append(PageBreak())


# ============================================================
# TRIP SUMMARY
# ============================================================

def build_trip_summary(story, data, styles):
    """
    Add trip summary.
    """

    story.append(
        make_paragraph(
            "1. Trip Summary",
            styles["SectionHeading"]
        )
    )

    summary = data.get("trip_summary", {})

    rows = [
        ["Parameter", "Details"],
        [
            "Destination",
            safe_value(summary.get("destination"))
        ],
        [
            "Duration",
            f"{safe_value(summary.get('duration'))} days"
        ],
        [
            "Travelers",
            safe_value(summary.get("travelers"))
        ],
        [
            "Estimated Total Cost",
            format_currency(
                summary.get("estimated_total_cost", 0)
            )
        ],
        [
            "Planning Strategy",
            safe_value(
                summary.get(
                    "planning_strategy",
                    "Personalized AI travel optimization"
                )
            )
        ]
    ]

    table = Table(
        [
            [
                make_paragraph(row[0], styles["TableHeader"]),
                make_paragraph(row[1], styles["TableText"])
            ]
            if index == 0
            else [
                make_paragraph(row[0], styles["TableText"]),
                make_paragraph(row[1], styles["TableText"])
            ]
            for index, row in enumerate(rows)
        ],
        colWidths=[55 * mm, 105 * mm]
    )

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#17365D")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(table)
    story.append(Spacer(1, 6 * mm))


# ============================================================
# DAILY ITINERARY
# ============================================================

def build_daily_itinerary(story, data, styles):
    """
    Add day-wise itinerary.
    """

    story.append(
        make_paragraph(
            "2. Day-wise AI Generated Itinerary",
            styles["SectionHeading"]
        )
    )

    daily_itinerary = data.get(
        "daily_itinerary",
        []
    )

    if not daily_itinerary:
        story.append(
            make_paragraph(
                "No daily itinerary information is available.",
                styles["BodyTextCustom"]
            )
        )
        return

    for day_data in daily_itinerary:

        day_number = day_data.get(
            "day",
            "N/A"
        )

        date = day_data.get(
            "date",
            ""
        )

        weather_note = day_data.get(
            "weather_note",
            "No weather note available."
        )

        story.append(
            make_paragraph(
                f"Day {safe_value(day_number)}"
                + (
                    f" - {safe_value(date)}"
                    if date
                    else ""
                ),
                styles["SubHeading"]
            )
        )

        story.append(
            make_paragraph(
                f"<b>Weather:</b> "
                f"{safe_value(weather_note)}",
                styles["BodyTextCustom"]
            )
        )

        rows = [
            [
                make_paragraph(
                    "Time",
                    styles["TableHeader"]
                ),
                make_paragraph(
                    "Place",
                    styles["TableHeader"]
                ),
                make_paragraph(
                    "Activity",
                    styles["TableHeader"]
                ),
                make_paragraph(
                    "Duration",
                    styles["TableHeader"]
                ),
                make_paragraph(
                    "Cost",
                    styles["TableHeader"]
                )
            ]
        ]

        for period in ["morning", "afternoon", "evening"]:

            activity = day_data.get(
                period,
                {}
            )

            if not isinstance(activity, dict):
                activity = {}

            rows.append(
                [
                    make_paragraph(
                        period.title(),
                        styles["TableText"]
                    ),
                    make_paragraph(
                        safe_value(
                            activity.get("place")
                        ),
                        styles["TableText"]
                    ),
                    make_paragraph(
                        safe_value(
                            activity.get("activity")
                        ),
                        styles["TableText"]
                    ),
                    make_paragraph(
                        safe_value(
                            activity.get("duration")
                        ),
                        styles["TableText"]
                    ),
                    make_paragraph(
                        format_currency(
                            activity.get("cost", 0)
                        ),
                        styles["TableText"]
                    )
                ]
            )

        table = Table(
            rows,
            colWidths=[
                22 * mm,
                38 * mm,
                48 * mm,
                27 * mm,
                25 * mm
            ],
            repeatRows=1
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor("#17365D")
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.35,
                        colors.grey
                    ),
                    (
                        "VALIGN",
                        (0, 0),
                        (-1, -1),
                        "TOP"
                    ),
                    (
                        "LEFTPADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    ),
                    (
                        "RIGHTPADDING",
                        (0, 0),
                        (-1, -1),
                        4
                    ),
                    (
                        "TOPPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    ),
                    (
                        "BOTTOMPADDING",
                        (0, 0),
                        (-1, -1),
                        5
                    )
                ]
            )
        )

        story.append(table)

        daily_cost = day_data.get(
            "daily_cost",
            0
        )

        story.append(
            make_paragraph(
                f"<b>Estimated Daily Cost:</b> "
                f"{format_currency(daily_cost)}",
                styles["BodyTextCustom"]
            )
        )

        # Reasons
        for period in ["morning", "afternoon", "evening"]:

            activity = day_data.get(
                period,
                {}
            )

            if not isinstance(activity, dict):
                continue

            reason = activity.get(
                "reason"
            )

            if reason:

                story.append(
                    make_paragraph(
                        f"<b>{period.title()} selection reason:</b> "
                        f"{safe_value(reason)}",
                        styles["ExplanationText"]
                    )
                )

        story.append(Spacer(1, 5 * mm))


# ============================================================
# RECOMMENDATION ANALYSIS
# ============================================================

def build_recommendation_analysis(story, data, styles):
    """
    Add AI recommendation scoring information.
    """

    story.append(
        make_paragraph(
            "3. AI Recommendation Analysis",
            styles["SectionHeading"]
        )
    )

    recommendation_analysis = data.get(
        "recommendation_analysis",
        data.get(
            "recommendations",
            {}
        )
    )

    if not recommendation_analysis:
        story.append(
            make_paragraph(
                "Recommendation scoring details were not available.",
                styles["BodyTextCustom"]
            )
        )
        return

    if isinstance(recommendation_analysis, dict):

        summary = recommendation_analysis.get(
            "summary"
        )

        if summary:
            story.append(
                make_paragraph(
                    safe_value(summary),
                    styles["BodyTextCustom"]
                )
            )

        ranked = recommendation_analysis.get(
            "ranked_activities",
            recommendation_analysis.get(
                "activities",
                []
            )
        )

        if isinstance(ranked, list) and ranked:

            rows = [
                [
                    make_paragraph(
                        "Activity",
                        styles["TableHeader"]
                    ),
                    make_paragraph(
                        "Score",
                        styles["TableHeader"]
                    ),
                    make_paragraph(
                        "Classification",
                        styles["TableHeader"]
                    )
                ]
            ]

            for item in ranked:

                if not isinstance(item, dict):
                    continue

                rows.append(
                    [
                        make_paragraph(
                            safe_value(
                                item.get(
                                    "activity",
                                    item.get(
                                        "place",
                                        "N/A"
                                    )
                                )
                            ),
                            styles["TableText"]
                        ),
                        make_paragraph(
                            safe_value(
                                item.get(
                                    "score",
                                    item.get(
                                        "recommendation_score",
                                        "N/A"
                                    )
                                )
                            ),
                            styles["TableText"]
                        ),
                        make_paragraph(
                            safe_value(
                                item.get(
                                    "classification",
                                    "N/A"
                                )
                            ),
                            styles["TableText"]
                        )
                    ]
                )

            table = Table(
                rows,
                colWidths=[
                    80 * mm,
                    35 * mm,
                    45 * mm
                ],
                repeatRows=1
            )

            table.setStyle(
                TableStyle(
                    [
                        (
                            "BACKGROUND",
                            (0, 0),
                            (-1, 0),
                            HexColor("#17365D")
                        ),
                        (
                            "GRID",
                            (0, 0),
                            (-1, -1),
                            0.4,
                            colors.grey
                        ),
                        (
                            "VALIGN",
                            (0, 0),
                            (-1, -1),
                            "TOP"
                        )
                    ]
                )
            )

            story.append(table)


# ============================================================
# BUDGET ANALYSIS
# ============================================================

def build_budget_analysis(story, data, styles):
    """
    Add budget optimization information.
    """

    story.append(
        make_paragraph(
            "4. Budget Analysis and Optimization",
            styles["SectionHeading"]
        )
    )

    budget_data = data.get(
        "budget_optimization",
        data.get(
            "budget_analysis",
            {}
        )
    )

    breakdown = data.get(
        "budget_breakdown",
        {}
    )

    if isinstance(budget_data, dict):

        budget = budget_data.get(
            "budget",
            data.get("budget", 0)
        )

        total_cost = budget_data.get(
            "total_cost",
            budget_data.get(
                "estimated_total_cost",
                data.get(
                    "estimated_total_cost",
                    0
                )
            )
        )

        score = budget_data.get(
            "optimization_score",
            budget_data.get(
                "budget_optimization_score",
                "N/A"
            )
        )

        story.append(
            make_paragraph(
                f"<b>Available Budget:</b> "
                f"{format_currency(budget)}",
                styles["BodyTextCustom"]
            )
        )

        story.append(
            make_paragraph(
                f"<b>Estimated Cost:</b> "
                f"{format_currency(total_cost)}",
                styles["BodyTextCustom"]
            )
        )

        story.append(
            make_paragraph(
                f"<b>Budget Optimization Score:</b> "
                f"{safe_value(score)}",
                styles["BodyTextCustom"]
            )
        )

        status = budget_data.get(
            "status",
            budget_data.get(
                "budget_status"
            )
        )

        if status:
            story.append(
                make_paragraph(
                    f"<b>Budget Status:</b> "
                    f"{safe_value(status)}",
                    styles["BodyTextCustom"]
                )
            )

    if isinstance(breakdown, dict):

        rows = [
            [
                make_paragraph(
                    "Category",
                    styles["TableHeader"]
                ),
                make_paragraph(
                    "Estimated Cost",
                    styles["TableHeader"]
                )
            ]
        ]

        category_names = {
            "accommodation": "Accommodation",
            "food": "Food",
            "transportation": "Transportation",
            "activities": "Activities",
            "miscellaneous": "Miscellaneous"
        }

        for key, label in category_names.items():

            rows.append(
                [
                    make_paragraph(
                        label,
                        styles["TableText"]
                    ),
                    make_paragraph(
                        format_currency(
                            breakdown.get(
                                key,
                                0
                            )
                        ),
                        styles["TableText"]
                    )
                ]
            )

        table = Table(
            rows,
            colWidths=[
                80 * mm,
                80 * mm
            ],
            repeatRows=1
        )

        table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        HexColor("#17365D")
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.4,
                        colors.grey
                    )
                ]
            )
        )

        story.append(table)

    suggestions = []

    if isinstance(budget_data, dict):

        suggestions = budget_data.get(
            "suggestions",
            budget_data.get(
                "budget_suggestions",
                []
            )
        )

    if suggestions:

        story.append(
            make_paragraph(
                "<b>Cost Saving Suggestions</b>",
                styles["SubHeading"]
            )
        )

        for suggestion in suggestions:

            story.append(
                make_paragraph(
                    "• " + safe_value(suggestion),
                    styles["BodyTextCustom"]
                )
            )


# ============================================================
# LOCATION OPTIMIZATION
# ============================================================

def build_location_analysis(story, data, styles):
    """
    Add location optimization analysis.
    """

    story.append(
        make_paragraph(
            "5. Location and Travel Efficiency Analysis",
            styles["SectionHeading"]
        )
    )

    location_data = data.get(
        "location_analysis",
        data.get(
            "location_optimization",
            {}
        )
    )

    if not location_data:
        story.append(
            make_paragraph(
                "Location optimization information is unavailable.",
                styles["BodyTextCustom"]
            )
        )
        return

    if isinstance(location_data, dict):

        score = location_data.get(
            "efficiency_score",
            location_data.get(
                "location_efficiency_score",
                "N/A"
            )
        )

        total_distance = location_data.get(
            "total_distance_km",
            location_data.get(
                "total_distance",
                "N/A"
            )
        )

        story.append(
            make_paragraph(
                f"<b>Location Efficiency Score:</b> "
                f"{safe_value(score)}",
                styles["BodyTextCustom"]
            )
        )

        story.append(
            make_paragraph(
                f"<b>Approximate Geographic Distance:</b> "
                f"{safe_value(total_distance)} km",
                styles["BodyTextCustom"]
            )
        )

        story.append(
            make_paragraph(
                "<b>Note:</b> Distance analysis is based on "
                "approximate geographical distance and should "
                "not be interpreted as road/driving distance.",
                styles["SmallText"]
            )
        )

        suggestions = location_data.get(
            "suggestions",
            location_data.get(
                "location_suggestions",
                []
            )
        )

        if suggestions:

            story.append(
                make_paragraph(
                    "<b>Location Optimization Suggestions</b>",
                    styles["SubHeading"]
                )
            )

            for suggestion in suggestions:

                story.append(
                    make_paragraph(
                        "• " + safe_value(suggestion),
                        styles["BodyTextCustom"]
                    )
                )


# ============================================================
# WEATHER ANALYSIS
# ============================================================

def build_weather_analysis(story, data, styles):
    """
    Add weather optimization information.
    """

    story.append(
        make_paragraph(
            "6. Weather Analysis",
            styles["SectionHeading"]
        )
    )

    weather_data = data.get(
        "weather_analysis",
        data.get(
            "weather_optimization",
            {}
        )
    )

    if not weather_data:

        story.append(
            make_paragraph(
                "Weather forecast information is unavailable "
                "for this itinerary.",
                styles["BodyTextCustom"]
            )
        )

        return

    if isinstance(weather_data, dict):

        summary = weather_data.get(
            "summary"
        )

        if summary:
            story.append(
                make_paragraph(
                    safe_value(summary),
                    styles["BodyTextCustom"]
                )
            )

        risk_score = weather_data.get(
            "weather_risk_score",
            weather_data.get(
                "risk_score"
            )
        )

        if risk_score is not None:

            story.append(
                make_paragraph(
                    f"<b>Weather Risk Score:</b> "
                    f"{safe_value(risk_score)}",
                    styles["BodyTextCustom"]
                )
            )

        recommendations = weather_data.get(
            "recommendations",
            []
        )

        if recommendations:

            story.append(
                make_paragraph(
                    "<b>Weather-based Recommendations</b>",
                    styles["SubHeading"]
                )
            )

            for recommendation in recommendations:

                story.append(
                    make_paragraph(
                        "• " + safe_value(recommendation),
                        styles["BodyTextCustom"]
                    )
                )

        story.append(
            make_paragraph(
                "<b>Note:</b> Weather information is based on "
                "available Open-Meteo forecast data. "
                "Forecast availability depends on the requested dates.",
                styles["SmallText"]
            )
        )


# ============================================================
# TIME OPTIMIZATION
# ============================================================

def build_time_analysis(story, data, styles):
    """
    Add time optimization information.
    """

    story.append(
        make_paragraph(
            "7. Time Optimization",
            styles["SectionHeading"]
        )
    )

    time_data = data.get(
        "time_optimization",
        data.get(
            "time_analysis",
            {}
        )
    )

    if not time_data:

        story.append(
            make_paragraph(
                "Time optimization information is unavailable.",
                styles["BodyTextCustom"]
            )
        )

        return

    if isinstance(time_data, dict):

        score = time_data.get(
            "time_optimization_score",
            time_data.get(
                "optimization_score",
                "N/A"
            )
        )

        story.append(
            make_paragraph(
                f"<b>Time Optimization Score:</b> "
                f"{safe_value(score)}",
                styles["BodyTextCustom"]
            )
        )

        summary = time_data.get(
            "summary"
        )

        if summary:

            story.append(
                make_paragraph(
                    safe_value(summary),
                    styles["BodyTextCustom"]
                )
            )

        conflicts = time_data.get(
            "conflicts",
            []
        )

        if conflicts:

            story.append(
                make_paragraph(
                    "<b>Detected Schedule Conflicts</b>",
                    styles["SubHeading"]
                )
            )

            for conflict in conflicts:

                story.append(
                    make_paragraph(
                        "• " + safe_value(conflict),
                        styles["BodyTextCustom"]
                    )
                )


# ============================================================
# CONSTRAINT OPTIMIZATION
# ============================================================

def build_constraint_analysis(story, data, styles):
    """
    Add constraint optimization information.
    """

    story.append(
        make_paragraph(
            "8. Constraint Optimization",
            styles["SectionHeading"]
        )
    )

    constraint_data = data.get(
        "constraint_analysis",
        data.get(
            "constraint_optimization",
            {}
        )
    )

    if not constraint_data:

        story.append(
            make_paragraph(
                "Constraint optimization information is unavailable.",
                styles["BodyTextCustom"]
            )
        )

        return

    if isinstance(constraint_data, dict):

        score = constraint_data.get(
            "overall_score",
            constraint_data.get(
                "constraint_score",
                "N/A"
            )
        )

        classification = constraint_data.get(
            "classification",
            "N/A"
        )

        story.append(
            make_paragraph(
                f"<b>Overall Constraint Score:</b> "
                f"{safe_value(score)}",
                styles["BodyTextCustom"]
            )
        )

        story.append(
            make_paragraph(
                f"<b>Optimization Classification:</b> "
                f"{safe_value(classification)}",
                styles["BodyTextCustom"]
            )
        )

        suggestions = constraint_data.get(
            "suggestions",
            []
        )

        if suggestions:

            story.append(
                make_paragraph(
                    "<b>Constraint Suggestions</b>",
                    styles["SubHeading"]
                )
            )

            for suggestion in suggestions:

                story.append(
                    make_paragraph(
                        "• " + safe_value(suggestion),
                        styles["BodyTextCustom"]
                    )
                )


# ============================================================
# EXPLAINABLE AI
# ============================================================

def build_explanation_analysis(story, data, styles):
    """
    Add Explainable AI information.
    """

    story.append(
        make_paragraph(
            "9. Explainable AI - Why These Activities Were Selected",
            styles["SectionHeading"]
        )
    )

    explanations = data.get(
        "explanations",
        data.get(
            "explanation_analysis",
            {}
        )
    )

    if not explanations:

        story.append(
            make_paragraph(
                "Detailed AI explanations are unavailable.",
                styles["BodyTextCustom"]
            )
        )

        return

    if isinstance(explanations, dict):

        final_explanation = explanations.get(
            "final_explanation"
        )

        if final_explanation:

            story.append(
                make_paragraph(
                    safe_value(final_explanation),
                    styles["ExplanationText"]
                )
            )

        activity_explanations = explanations.get(
            "activity_explanations",
            []
        )

        if isinstance(
            activity_explanations,
            list
        ):

            for item in activity_explanations:

                if not isinstance(item, dict):
                    continue

                activity_name = item.get(
                    "activity",
                    item.get(
                        "place",
                        "Activity"
                    )
                )

                explanation = item.get(
                    "explanation",
                    item.get(
                        "reason",
                        ""
                    )
                )

                story.append(
                    KeepTogether(
                        [
                            make_paragraph(
                                f"<b>{safe_value(activity_name)}</b>",
                                styles["SubHeading"]
                            ),
                            make_paragraph(
                                safe_value(explanation),
                                styles["ExplanationText"]
                            )
                        ]
                    )
                )

        day_explanations = explanations.get(
            "day_explanations",
            []
        )

        if isinstance(
            day_explanations,
            list
        ):

            for item in day_explanations:

                if not isinstance(item, dict):
                    continue

                day = item.get(
                    "day",
                    "Day"
                )

                explanation = item.get(
                    "explanation",
                    item.get(
                        "reason",
                        ""
                    )
                )

                if explanation:

                    story.append(
                        make_paragraph(
                            f"<b>Day {safe_value(day)}:</b> "
                            f"{safe_value(explanation)}",
                            styles["ExplanationText"]
                        )
                    )


# ============================================================
# ACCOMMODATION
# ============================================================

def build_accommodation(story, data, styles):
    """
    Add accommodation recommendations.
    """

    story.append(
        make_paragraph(
            "10. Accommodation Recommendations",
            styles["SectionHeading"]
        )
    )

    accommodations = data.get(
        "accommodation",
        []
    )

    if not accommodations:

        story.append(
            make_paragraph(
                "No accommodation recommendations available.",
                styles["BodyTextCustom"]
            )
        )

        return

    rows = [
        [
            make_paragraph(
                "Area",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Type",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Estimated Cost/Night",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Reason",
                styles["TableHeader"]
            )
        ]
    ]

    for item in accommodations:

        if not isinstance(item, dict):
            continue

        rows.append(
            [
                make_paragraph(
                    safe_value(item.get("area")),
                    styles["TableText"]
                ),
                make_paragraph(
                    safe_value(item.get("type")),
                    styles["TableText"]
                ),
                make_paragraph(
                    format_currency(
                        item.get(
                            "estimated_cost_per_night",
                            0
                        )
                    ),
                    styles["TableText"]
                ),
                make_paragraph(
                    safe_value(item.get("reason")),
                    styles["TableText"]
                )
            ]
        )

    table = Table(
        rows,
        colWidths=[
            35 * mm,
            30 * mm,
            40 * mm,
            55 * mm
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#17365D")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                )
            ]
        )
    )

    story.append(table)


# ============================================================
# FOOD
# ============================================================

def build_food(story, data, styles):
    """
    Add food recommendations.
    """

    story.append(
        make_paragraph(
            "11. Food Recommendations",
            styles["SectionHeading"]
        )
    )

    food_items = data.get(
        "food_recommendations",
        []
    )

    if not food_items:

        story.append(
            make_paragraph(
                "No food recommendations available.",
                styles["BodyTextCustom"]
            )
        )

        return

    rows = [
        [
            make_paragraph(
                "Food",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Type",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Estimated Cost",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Reason",
                styles["TableHeader"]
            )
        ]
    ]

    for item in food_items:

        if not isinstance(item, dict):
            continue

        rows.append(
            [
                make_paragraph(
                    safe_value(item.get("food")),
                    styles["TableText"]
                ),
                make_paragraph(
                    safe_value(item.get("type")),
                    styles["TableText"]
                ),
                make_paragraph(
                    format_currency(
                        item.get(
                            "estimated_cost",
                            0
                        )
                    ),
                    styles["TableText"]
                ),
                make_paragraph(
                    safe_value(item.get("reason")),
                    styles["TableText"]
                )
            ]
        )

    table = Table(
        rows,
        colWidths=[
            40 * mm,
            30 * mm,
            35 * mm,
            55 * mm
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#17365D")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                )
            ]
        )
    )

    story.append(table)


# ============================================================
# TRANSPORTATION
# ============================================================

def build_transportation(story, data, styles):
    """
    Add transportation recommendations.
    """

    story.append(
        make_paragraph(
            "12. Transportation Plan",
            styles["SectionHeading"]
        )
    )

    transportation = data.get(
        "transportation",
        []
    )

    if not transportation:

        story.append(
            make_paragraph(
                "No transportation recommendations available.",
                styles["BodyTextCustom"]
            )
        )

        return

    rows = [
        [
            make_paragraph(
                "Mode",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Estimated Cost",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Reason",
                styles["TableHeader"]
            )
        ]
    ]

    for item in transportation:

        if not isinstance(item, dict):
            continue

        rows.append(
            [
                make_paragraph(
                    safe_value(item.get("mode")),
                    styles["TableText"]
                ),
                make_paragraph(
                    format_currency(
                        item.get(
                            "estimated_cost",
                            0
                        )
                    ),
                    styles["TableText"]
                ),
                make_paragraph(
                    safe_value(item.get("reason")),
                    styles["TableText"]
                )
            ]
        )

    table = Table(
        rows,
        colWidths=[
            45 * mm,
            40 * mm,
            75 * mm
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#17365D")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                )
            ]
        )
    )

    story.append(table)


# ============================================================
# PACKING CHECKLIST
# ============================================================

def build_packing_checklist(story, data, styles):
    """
    Add packing checklist.
    """

    story.append(
        make_paragraph(
            "13. Packing Checklist",
            styles["SectionHeading"]
        )
    )

    checklist = data.get(
        "packing_checklist",
        []
    )

    if not checklist:

        story.append(
            make_paragraph(
                "No packing checklist generated.",
                styles["BodyTextCustom"]
            )
        )

        return

    for item in checklist:

        story.append(
            make_paragraph(
                "☐ " + safe_value(item),
                styles["BodyTextCustom"]
            )
        )


# ============================================================
# TRAVEL TIPS
# ============================================================

def build_travel_tips(story, data, styles):
    """
    Add travel tips.
    """

    story.append(
        make_paragraph(
            "14. AI Travel Tips",
            styles["SectionHeading"]
        )
    )

    tips = data.get(
        "travel_tips",
        []
    )

    if not tips:

        story.append(
            make_paragraph(
                "No additional travel tips generated.",
                styles["BodyTextCustom"]
            )
        )

        return

    for tip in tips:

        story.append(
            make_paragraph(
                "• " + safe_value(tip),
                styles["BodyTextCustom"]
            )
        )


# ============================================================
# OPTIMIZATION SUMMARY
# ============================================================

def build_optimization_summary(story, data, styles):
    """
    Add final optimization summary.
    """

    story.append(
        make_paragraph(
            "15. Final Optimization Summary",
            styles["SectionHeading"]
        )
    )

    optimization = data.get(
        "optimization_summary",
        {}
    )

    if not optimization:

        story.append(
            make_paragraph(
                "No optimization summary available.",
                styles["BodyTextCustom"]
            )
        )

        return

    rows = [
        [
            make_paragraph(
                "Optimization Area",
                styles["TableHeader"]
            ),
            make_paragraph(
                "Strategy",
                styles["TableHeader"]
            )
        ]
    ]

    labels = {
        "budget_strategy": "Budget",
        "location_strategy": "Location",
        "weather_strategy": "Weather",
        "time_strategy": "Time"
    }

    for key, label in labels.items():

        rows.append(
            [
                make_paragraph(
                    label,
                    styles["TableText"]
                ),
                make_paragraph(
                    safe_value(
                        optimization.get(key)
                    ),
                    styles["TableText"]
                )
            ]
        )

    table = Table(
        rows,
        colWidths=[
            50 * mm,
            110 * mm
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    HexColor("#17365D")
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.4,
                    colors.grey
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP"
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )

    story.append(table)


# ============================================================
# FINAL PAGE
# ============================================================

def build_final_page(story, styles):
    """
    Add final note.
    """

    story.append(PageBreak())

    story.append(
        Spacer(1, 35 * mm)
    )

    story.append(
        make_paragraph(
            "AI-Powered Travel Planning",
            styles["MainTitle"]
        )
    )

    story.append(
        make_paragraph(
            "This itinerary was generated using a combination of "
            "AI generation, recommendation scoring, weather analysis, "
            "budget optimization, location optimization, time "
            "optimization, constraint optimization and explainable AI.",
            styles["SubTitle"]
        )
    )

    story.append(
        Spacer(1, 15 * mm)
    )

    story.append(
        make_paragraph(
            "Important Disclaimer",
            styles["SectionHeading"]
        )
    )

    story.append(
        make_paragraph(
            "All costs, travel durations and recommendations are "
            "approximate. Actual prices, availability, traffic, "
            "weather and local conditions may change. Users should "
            "verify important travel information before making "
            "bookings or final travel decisions.",
            styles["BodyTextCustom"]
        )
    )


# ============================================================
# MAIN PDF GENERATION FUNCTION
# ============================================================

def generate_travel_pdf(
    itinerary_data,
    output_path="AI_Travel_Itinerary.pdf"
):
    """
    Generate the complete travel itinerary PDF.

    Parameters
    ----------
    itinerary_data : dict
        Final itinerary data generated by the AI system.

    output_path : str
        Location where the PDF should be saved.

    Returns
    -------
    dict
        Success status and generated file path.
    """

    try:

        if not isinstance(itinerary_data, dict):

            return {
                "success": False,
                "error": "Itinerary data must be a dictionary."
            }

        output_directory = os.path.dirname(
            os.path.abspath(output_path)
        )

        os.makedirs(
            output_directory,
            exist_ok=True
        )

        styles = create_pdf_styles()

        document = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=15 * mm,
            leftMargin=15 * mm,
            topMargin=15 * mm,
            bottomMargin=15 * mm,
            title="AI Travel Itinerary",
            author="AI Travel Itinerary Generator"
        )

        story = []

        # ----------------------------------------------------
        # COVER
        # ----------------------------------------------------

        build_cover_page(
            story,
            itinerary_data,
            styles
        )

        # ----------------------------------------------------
        # MAIN SECTIONS
        # ----------------------------------------------------

        build_trip_summary(
            story,
            itinerary_data,
            styles
        )

        build_daily_itinerary(
            story,
            itinerary_data,
            styles
        )

        build_recommendation_analysis(
            story,
            itinerary_data,
            styles
        )

        build_budget_analysis(
            story,
            itinerary_data,
            styles
        )

        build_location_analysis(
            story,
            itinerary_data,
            styles
        )

        build_weather_analysis(
            story,
            itinerary_data,
            styles
        )

        build_time_analysis(
            story,
            itinerary_data,
            styles
        )

        build_constraint_analysis(
            story,
            itinerary_data,
            styles
        )

        build_explanation_analysis(
            story,
            itinerary_data,
            styles
        )

        build_accommodation(
            story,
            itinerary_data,
            styles
        )

        build_food(
            story,
            itinerary_data,
            styles
        )

        build_transportation(
            story,
            itinerary_data,
            styles
        )

        build_packing_checklist(
            story,
            itinerary_data,
            styles
        )

        build_travel_tips(
            story,
            itinerary_data,
            styles
        )

        build_optimization_summary(
            story,
            itinerary_data,
            styles
        )

        build_final_page(
            story,
            styles
        )

        # ----------------------------------------------------
        # BUILD PDF
        # ----------------------------------------------------

        document.build(
            story,
            onFirstPage=add_page_number,
            onLaterPages=add_page_number
        )

        return {
            "success": True,
            "file_path": output_path,
            "message": "Travel itinerary PDF generated successfully."
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error)
        }


# ============================================================
# ALIAS FOR COMPATIBILITY
# ============================================================

def create_travel_pdf(
    itinerary_data,
    output_path="AI_Travel_Itinerary.pdf"
):
    """
    Compatibility wrapper.
    """

    return generate_travel_pdf(
        itinerary_data=itinerary_data,
        output_path=output_path
    )