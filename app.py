from flask import Flask, render_template, request

from finance import calculate_finance

from api_services import (
    get_location,
    get_weather,
    get_nearby_market
)

from government_api import (
    get_government_schemes
)

from ai_advisor import (
    get_ai_recommendation
)

from database import (
    save_entrepreneur
)

import market_data

from market_data import (
    get_business_market_data
)


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(__name__)

print("============================================")
print("MARKET DATA DEBUG TEST")
print("============================================")

print("market_data.py loaded from:")
print(market_data.__file__)

print("Number of records in MARKET_DATA:")
print(len(market_data.MARKET_DATA))

print("Testing Farmer + Andhra Pradesh + Guntur:")

test_result = market_data.get_business_market_data(
    business="Farmer",
    state="Andhra Pradesh",
    district="Guntur"
)

print("TEST RESULT COUNT:", len(test_result))

print("============================================")


# ============================================================
# CHECK MARKET DATA MODULE
# ============================================================

print()
print("============================================")
print("       MARKET DATA MODULE CHECK")
print("============================================")
print("Using market_data.py from:")
print(market_data.__file__)
print("============================================")
print()


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# ============================================================
# ANALYZE BUSINESS
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def analyze():

    # ========================================================
    # GET FORM DATA
    # ========================================================

    name = request.form.get(
        "name",
        ""
    ).strip()

    village = request.form.get(
        "village",
        ""
    ).strip()

    district = request.form.get(
        "district",
        ""
    ).strip()

    state = request.form.get(
        "state",
        ""
    ).strip()

    business = request.form.get(
        "business",
        ""
    ).strip()

    experience = request.form.get(
        "experience",
        ""
    ).strip()

    goal = request.form.get(
        "goal",
        ""
    ).strip()


    # ========================================================
    # FORM DEBUG
    # ========================================================

    print()
    print("============================================")
    print("             FORM DATA")
    print("============================================")

    print("Name       :", repr(name))
    print("Village    :", repr(village))
    print("District   :", repr(district))
    print("State      :", repr(state))
    print("Business   :", repr(business))
    print("Experience :", repr(experience))
    print("Goal       :", repr(goal))

    print("============================================")
    print()


    # ========================================================
    # INVESTMENT
    # ========================================================

    try:

        investment = float(
            request.form.get(
                "investment",
                0
            )
        )

    except (ValueError, TypeError):

        investment = 0


    print(
        "Investment:",
        investment
    )


    # ========================================================
    # SAVE ENTREPRENEUR
    # ========================================================

    entrepreneur_id = None

    try:

        entrepreneur_id = save_entrepreneur(

            name,
            village,
            district,
            state,
            business,
            investment,
            experience,
            goal

        )

        print(
            "Entrepreneur saved with ID:",
            entrepreneur_id
        )

    except Exception as e:

        print(
            "Database save error:",
            repr(e)
        )


    # ========================================================
    # FINANCIAL ANALYSIS
    # ========================================================

    finance = None

    try:

        finance = calculate_finance(

            business,
            investment

        )

        print(
            "Financial analysis completed."
        )

    except Exception as e:

        print(
            "Finance error:",
            repr(e)
        )


    # ========================================================
    # LOCATION
    # ========================================================

    location = None

    try:

        print()
        print(
            "Searching location..."
        )

        location = get_location(

            district,
            state

        )

        if location:

            print(
                "Location found:",
                location.get(
                    "name",
                    "Unknown"
                )
            )

        else:

            print(
                "Location not found."
            )

    except Exception as e:

        print(
            "Location API error:",
            repr(e)
        )


    # ========================================================
    # WEATHER
    # ========================================================
    print("LOCATION RESULT FOR WEATHER:", location)
    weather = None

    if location:

        try:

            weather = get_weather(

                location["latitude"],
                location["longitude"]

            )

            print(
                "Weather data received."
            )

        except Exception as e:

            print(
                "Weather API error:",
                repr(e)
            )

    else:

        print(
            "Weather skipped because "
            "location is unavailable."
        )


    # ========================================================
    # NEARBY MARKET
    # ========================================================

    nearby = None

    if location:

        try:

            print()
            print(
                "Searching for nearby "
                "market information..."
            )

            nearby = get_nearby_market(

                location["latitude"],
                location["longitude"]

            )

            if nearby:

                print(
                    "Local market information "
                    "received."
                )

                print(
                    "Total nearby places:",
                    nearby.get(
                        "total_places",
                        0
                    )
                )

            else:

                print(
                    "No local market information "
                    "found."
                )

        except Exception as e:

            print(
                "Local market API error:",
                repr(e)
            )

    else:

        print(
            "Local market search skipped "
            "because location is unavailable."
        )


    # ========================================================
    # GOVERNMENT SCHEMES
    # ========================================================

    government_schemes = []

    try:

        government_schemes = (
            get_government_schemes(

                business,

                investment,

                state

            )
        )

        print(
            "Government scheme analysis completed."
        )

    except Exception as e:

        print(
            "Government scheme error:",
            repr(e)
        )

        government_schemes = []


    # ========================================================
    # LOCAL MARKET INTELLIGENCE
    # ========================================================

    market_data_result = []

    try:

        print()
        print("============================================")
        print("       LOCAL MARKET INTELLIGENCE")
        print("============================================")

        print(
            "Searching local market intelligence..."
        )

        print(
            "Business:",
            repr(business)
        )

        print(
            "State:",
            repr(state)
        )

        print(
            "District:",
            repr(district)
        )


        # ----------------------------------------------------
        # GET BUSINESS MARKET DATA
        # ----------------------------------------------------

        market_data_result = get_business_market_data(

            business=business,

            state=state,

            district=district

        )


        # ----------------------------------------------------
        # CHECK RESULTS
        # ----------------------------------------------------

        if market_data_result:

            print()
            print(
                "Local market intelligence "
                "received."
            )

            print(
                "Total market records:",
                len(market_data_result)
            )

            print()
            print(
                "--------- MARKET RESULTS ---------"
            )

            for record in market_data_result:

                print(
                    record.get(
                        "commodity",
                        "Unknown"
                    ),
                    "-",
                    record.get(
                        "price",
                        "N/A"
                    ),
                    "/",
                    record.get(
                        "unit",
                        ""
                    ),
                    "-",
                    record.get(
                        "trend",
                        "Unknown"
                    )
                )

            print(
                "----------------------------------"
            )

        else:

            print()
            print(
                "No local market intelligence "
                "found."
            )

        print(
            "============================================"
        )
        print()


    except Exception as e:

        print()
        print(
            "Market data error:",
            repr(e)
        )

        market_data_result = []


    # ========================================================
    # AI BUSINESS ADVISOR
    # ========================================================

    ai_recommendation = None

    try:

        ai_recommendation = (
            get_ai_recommendation(

                name=name,

                village=village,

                district=district,

                state=state,

                business=business,

                investment=investment,

                experience=experience,

                goal=goal,

                finance=finance,

                location=location,

                weather=weather,

                nearby=nearby,

                government_schemes=government_schemes,

                market_data=market_data_result

            )
        )

        print(
            "AI recommendation generated."
        )

    except Exception as e:

        print(
            "AI recommendation error:",
            repr(e)
        )

        ai_recommendation = (
            "AI recommendation is "
            "currently unavailable."
        )


    # ========================================================
    # DISPLAY ANALYSIS PAGE
    # ========================================================

    return render_template(

        "analysis.html",

        # ----------------------------------------------------
        # ENTREPRENEUR DETAILS
        # ----------------------------------------------------

        name=name,

        village=village,

        district=district,

        state=state,

        business=business,

        investment=investment,

        experience=experience,

        goal=goal,

        entrepreneur_id=entrepreneur_id,


        # ----------------------------------------------------
        # FINANCE
        # ----------------------------------------------------

        finance=finance,


        # ----------------------------------------------------
        # LOCATION
        # ----------------------------------------------------

        location=location,


        # ----------------------------------------------------
        # WEATHER
        # ----------------------------------------------------

        weather=weather,


        # ----------------------------------------------------
        # NEARBY MARKET
        # ----------------------------------------------------

        nearby=nearby,


        # ----------------------------------------------------
        # GOVERNMENT SCHEMES
        # ----------------------------------------------------

        government_schemes=government_schemes,


        # ----------------------------------------------------
        # LOCAL MARKET INTELLIGENCE
        # ----------------------------------------------------

        market_data=market_data_result,


        # ----------------------------------------------------
        # AI RECOMMENDATION
        # ----------------------------------------------------

        ai_recommendation=ai_recommendation

    )


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print()
    print(
        "========================================"
    )

    print(
        "       RURAL BUSINESS ADVISOR"
    )

    print(
        "       FLASK SERVER STARTING"
    )

    print(
        "========================================"
    )

    print()

    print(
        "Open the following URL:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    app.run(

        host="127.0.0.1",

        port=5000,

        debug=False,

        use_reloader=False

    )