from openai import OpenAI
import os


# =================================================
# OPENAI API KEY
# =================================================

API_KEY = os.getenv("OPENAI_API_KEY")


client = OpenAI(
    api_key=API_KEY
)


# =================================================
# AI BUSINESS ADVISOR
# =================================================

def get_ai_recommendation(
    name,
    village,
    district,
    state,
    business,
    investment,
    experience,
    goal,
    finance,
    location,
    weather,
    nearby,
    government_schemes=None,
    market_data=None
):

    # -------------------------------------------------
    # LOCATION
    # -------------------------------------------------

    if location:

        location_info = f"""
Location: {location.get("name", "N/A")}
State: {location.get("state", "N/A")}
Latitude: {location.get("latitude", "N/A")}
Longitude: {location.get("longitude", "N/A")}
"""

    else:

        location_info = "Location information unavailable."


    # -------------------------------------------------
    # WEATHER
    # -------------------------------------------------

    if weather:

        weather_info = f"""
Temperature: {weather.get("temperature", "N/A")} °C
Humidity: {weather.get("humidity", "N/A")} %
Precipitation: {weather.get("precipitation", "N/A")} mm
Maximum Temperature: {weather.get("max_temperature", "N/A")} °C
Minimum Temperature: {weather.get("min_temperature", "N/A")} °C
Rain Forecast: {weather.get("rain_forecast", "N/A")} mm
"""

    else:

        weather_info = "Weather information unavailable."


    # -------------------------------------------------
    # NEARBY MARKET
    # -------------------------------------------------

    if nearby:

        nearby_info = f"""
Marketplaces: {nearby.get("marketplaces", "N/A")}
Dairy Shops: {nearby.get("dairy_shops", "N/A")}
Farm Shops: {nearby.get("farm_shops", "N/A")}
Total Places: {nearby.get("total_places", "N/A")}
"""

    else:

        nearby_info = "Nearby market information unavailable."


    # -------------------------------------------------
    # FINANCIAL DATA
    # -------------------------------------------------

    if finance:

        finance_info = f"""
Required Investment: ₹{finance.get("required_investment", "N/A")}
Available Investment: ₹{investment}
Monthly Revenue: ₹{finance.get("monthly_revenue", "N/A")}
Monthly Expense: ₹{finance.get("monthly_expense", "N/A")}
Monthly Profit: ₹{finance.get("monthly_profit", "N/A")}
Annual Profit: ₹{finance.get("annual_profit", "N/A")}
Funding Gap: ₹{finance.get("funding_gap", "N/A")}
Profit Margin: {finance.get("profit_margin", "N/A")}%
ROI: {finance.get("roi", "N/A")}%
Break-Even: {finance.get("break_even", "N/A")} months
Viability Score: {finance.get("viability_score", "N/A")}/100
Risk Level: {finance.get("risk_level", "N/A")}
Financial Recommendation: {finance.get("recommendation", "N/A")}
Funding Status: {finance.get("funding_status", "N/A")}
"""

    else:

        finance_info = "Financial information unavailable."


    # -------------------------------------------------
    # GOVERNMENT SCHEMES
    # -------------------------------------------------

    if government_schemes:

        government_info = ""

        for scheme in government_schemes:

            if isinstance(scheme, dict):

                government_info += f"""
Scheme: {scheme.get("name", "N/A")}
Description: {scheme.get("description", "N/A")}
Reason: {scheme.get("reason", "N/A")}
"""

            else:

                government_info += f"""
Scheme: {scheme}
"""

    else:

        government_info = (
            "No government scheme information available."
        )


    # -------------------------------------------------
    # GOVERNMENT MARKET DATA
    # -------------------------------------------------

    if market_data:

        market_data_info = str(
            market_data
        )

    else:

        market_data_info = (
            "Government market price data "
            "is currently unavailable."
        )


    # =================================================
    # AI PROMPT
    # =================================================

    prompt = f"""
You are an AI business advisor for rural
micro-entrepreneurs in India.

Your task is to analyze the entrepreneur using
the available financial, geographical, weather,
local market and government scheme information.

Do not invent missing information.

ENTREPRENEUR

Name: {name}
Village: {village}
District: {district}
State: {state}

BUSINESS

Business Type: {business}
Available Investment: ₹{investment}
Experience: {experience}
Business Goal: {goal}


=================================================
FINANCIAL ANALYSIS
=================================================

{finance_info}


=================================================
LOCATION DATA
=================================================

{location_info}


=================================================
WEATHER DATA
=================================================

{weather_info}


=================================================
NEARBY MARKET DATA
=================================================

{nearby_info}


=================================================
GOVERNMENT SCHEME INFORMATION
=================================================

{government_info}


=================================================
GOVERNMENT MARKET DATA
=================================================

{market_data_info}


=================================================
TASK
=================================================

Give practical, simple and personalized advice.

Use the following sections:


1. BUSINESS RECOMMENDATION

Explain whether the selected business appears
financially and locally suitable.


2. WHY THIS BUSINESS

Give 3 reasons based only on the available data.


3. BUSINESS STRATEGY

Give practical steps for starting or improving
the business.


4. FINANCIAL ADVICE

Explain:

- Required investment
- Available investment
- Funding gap
- Monthly revenue
- Monthly expense
- Monthly profit
- Profit margin
- ROI
- Break-even
- Viability score


5. LOCAL OPPORTUNITY

Explain how the location, nearby businesses,
weather and local conditions may affect the
business.


6. GOVERNMENT SUPPORT

Mention only the government schemes provided
in the scheme information.

Explain how they may help.

Do not claim guaranteed eligibility.


7. RISKS

Identify important business risks and explain
how to reduce them.


8. NEXT STEPS

Give exactly 5 practical actions the entrepreneur
can take.


IMPORTANT RULES:

- Do not invent exact market prices.
- Do not invent government schemes.
- Do not claim guaranteed government eligibility.
- Do not treat unavailable information as fact.
- Clearly mention when information is unavailable.
- Use simple language.
- Keep recommendations practical.
- Base financial conclusions on the supplied
  financial analysis.
"""


    # =================================================
    # CALL AI
    # =================================================

    try:

        response = client.responses.create(

            model="gpt-5.6-luna",

            input=prompt

        )

        return response.output_text


    except Exception as e:

        print("OPENAI API ERROR:")

        print(e)

        return (
            "AI recommendation could not be generated. "
            "Please check the OpenAI API key and connection."
        )