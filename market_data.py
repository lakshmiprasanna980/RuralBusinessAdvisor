# market_data.py

MARKET_DATA = [

    {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "business": "Farmer",
        "commodity": "Chilli",
        "market": "Guntur Market",
        "price": 18000,
        "unit": "quintal",
        "trend": "Rising"
    },
    {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "business": "Farmer",
        "commodity": "Cotton",
        "market": "Guntur Market",
        "price": 7000,
        "unit": "quintal",
        "trend": "Stable"
    },
    {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "business": "Farmer",
        "commodity": "Turmeric",
        "market": "Guntur Market",
        "price": 12000,
        "unit": "quintal",
        "trend": "Rising"
    },

    {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "business": "Retail",
        "commodity": "Groceries",
        "market": "Guntur Retail Market",
        "price": 45000,
        "unit": "monthly demand index",
        "trend": "Rising"
    },

    {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "business": "Handicrafts",
        "commodity": "Handicraft Products",
        "market": "Guntur Local Market",
        "price": 850,
        "unit": "average item",
        "trend": "Stable"
    },

    {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "business": "Poultry Farming",
        "commodity": "Broiler Chicken",
        "market": "Guntur Poultry Market",
        "price": 190,
        "unit": "kg",
        "trend": "Rising"
    },

    {
        "state": "Andhra Pradesh",
        "district": "Krishna",
        "business": "Farmer",
        "commodity": "Paddy",
        "market": "Vijayawada Market",
        "price": 2400,
        "unit": "quintal",
        "trend": "Stable"
    },

    {
        "state": "Andhra Pradesh",
        "district": "Krishna",
        "business": "Farmer",
        "commodity": "Cotton",
        "market": "Vijayawada Market",
        "price": 6800,
        "unit": "quintal",
        "trend": "Rising"
    },

    {
        "state": "Andhra Pradesh",
        "district": "Visakhapatnam",
        "business": "Farmer",
        "commodity": "Paddy",
        "market": "Visakhapatnam Market",
        "price": 2300,
        "unit": "quintal",
        "trend": "Stable"
    }
]


def normalize_business(business):

    business = str(business).strip().lower()

    aliases = {
        "farmer": "farmer",
        "farming": "farmer",
        "agriculture": "farmer",
        "agriculture farming": "farmer",

        "poultry": "poultry farming",
        "poultry farming": "poultry farming",

        "handicraft": "handicrafts",
        "handicrafts": "handicrafts",

        "retail": "retail"
    }

    return aliases.get(business, business)


def get_business_market_data(business, state, district):

    business = normalize_business(business)
    state = str(state).strip().lower()
    district = str(district).strip().lower()

    results = []

    for record in MARKET_DATA:

        record_business = normalize_business(
            record["business"]
        )

        record_state = record["state"].strip().lower()
        record_district = record["district"].strip().lower()

        if (
            record_business == business
            and record_state == state
            and record_district == district
        ):
            results.append(record)

    return results


def get_business_commodities(business, state, district):

    return get_business_market_data(
        business,
        state,
        district
    )