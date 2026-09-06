import requests


# =================================================
# LOCATION API
# =================================================

def get_location(district, state):

    district = (district or "").strip()
    state = (state or "").strip()

    if not district or not state:
        print("District or state is empty.")
        return None

    # Andhra Pradesh district-level fallback coordinates
    # Used when the external geocoding service is unavailable.
    ap_coordinates = {
        "guntur": (16.3067, 80.4365),
        "krishna": (16.5449, 81.0640),
        "eluru": (16.7107, 81.0952),
        "ntr": (16.5062, 80.6480),
        "palnadu": (16.2354, 80.0499),
        "bapatla": (15.9044, 80.4675),
        "prakasam": (15.5057, 80.0499),
        "spsr nellore": (14.4426, 79.9865),
        "nellore": (14.4426, 79.9865),
        "tirupati": (13.6288, 79.4192),
        "chittoor": (13.2172, 79.1003),
        "annamayya": (14.0600, 78.7500),
        "ysr kadapa": (14.4674, 78.8241),
        "kadapa": (14.4674, 78.8241),
        "kurnool": (15.8281, 78.0373),
        "nandyal": (15.4786, 78.4831),
        "ananthapur": (14.6819, 77.6006),
        "anantapur": (14.6819, 77.6006),
        "sri sathya sai": (14.2306, 77.6141),
        "srikakulam": (18.2949, 83.8938),
        "vizianagaram": (18.1067, 83.3956),
        "visakhapatnam": (17.6868, 83.2185),
        "alluri sitharama raju": (17.7000, 81.9000),
        "anakapalli": (17.6913, 83.0039),
        "kakinada": (16.9891, 82.2475),
        "east godavari": (16.9891, 82.2475),
        "konaseema": (16.5800, 82.0000),
        "west godavari": (16.7107, 81.0952)
    }

    # First try the online geocoding service
    try:

        url = "https://geocoding-api.open-meteo.com/v1/search"

        params = {
            "name": f"{district}, {state}",
            "count": 10,
            "language": "en",
            "format": "json",
            "countryCode": "IN"
        }

        response = requests.get(
            url,
            params=params,
            timeout=8
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        print("Location API results:", len(results))

        state_lower = state.lower()

        for result in results:

            location_state = (
                result.get("admin1", "") or ""
            ).strip().lower()

            if location_state == state_lower:

                location = {
                    "name": result.get("name"),
                    "state": result.get("admin1"),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude")
                }

                print(
                    "Location found:",
                    location["name"],
                    "-",
                    location["state"]
                )

                return location

    except Exception as e:

        print(
            "Online location service unavailable:",
            repr(e)
        )

    # Fallback for Andhra Pradesh
    if state.lower() in [
        "andhra pradesh",
        "andhrapradesh"
    ]:

        district_key = district.lower()

        if district_key in ap_coordinates:

            latitude, longitude = ap_coordinates[district_key]

            location = {
                "name": district,
                "state": "Andhra Pradesh",
                "latitude": latitude,
                "longitude": longitude
            }

            print(
                "Using Andhra Pradesh district fallback:",
                district,
                latitude,
                longitude
            )

            return location

    print("Location not found.")

    return None

# =================================================
# WEATHER API
# =================================================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code"
        ),
        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum"
        ),
        "forecast_days": 3,
        "timezone": "auto"
    }

    try:

        print(
            "REQUESTING WEATHER:",
            latitude,
            longitude
        )

        response = requests.get(
            url,
            params=params,
            headers={
                "User-Agent": "RuralBusinessAdvisor/1.0"
            },
            timeout=15
        )

        print(
            "Weather API status:",
            response.status_code
        )

        response.raise_for_status()

        data = response.json()

        current = data.get("current", {})
        daily = data.get("daily", {})

        weather = {
            "temperature": current.get(
                "temperature_2m"
            ),

            "humidity": current.get(
                "relative_humidity_2m"
            ),

            "precipitation": current.get(
                "precipitation"
            ),

            "weather_code": current.get(
                "weather_code"
            ),

            "max_temperature": daily.get(
                "temperature_2m_max",
                [None]
            )[0],

            "min_temperature": daily.get(
                "temperature_2m_min",
                [None]
            )[0],

            "rain_forecast": daily.get(
                "precipitation_sum",
                [None]
            )[0]
        }

        print(
            "WEATHER RESULT:",
            weather
        )

        return weather

    except requests.exceptions.Timeout:

        print("Weather API timed out.")
        return None

    except requests.exceptions.RequestException as e:

        print(
            "Weather API request error:",
            repr(e)
        )

        return None

    except ValueError:

        print(
            "Weather API returned invalid JSON."
        )

        return None

    except Exception as e:

        print(
            "Unexpected weather error:",
            repr(e)
        )

        return None

# =================================================
# LOCAL MARKET / NEARBY PLACES
# =================================================

def get_nearby_market(latitude, longitude):

    url = (
        "https://overpass-api.de/"
        "api/interpreter"
    )

    query = f"""
    [out:json][timeout:10];

    (
        node["amenity"="marketplace"]
        (around:10000,{latitude},{longitude});

        way["amenity"="marketplace"]
        (around:10000,{latitude},{longitude});

        node["shop"="farm"]
        (around:10000,{latitude},{longitude});

        node["shop"="dairy"]
        (around:10000,{latitude},{longitude});

        node["shop"="greengrocer"]
        (around:10000,{latitude},{longitude});
    );

    out center tags;
    """


    try:

        print(
            "Searching for nearby markets..."
        )


        response = requests.get(

            url,

            params={
                "data": query
            },

            headers={
                "User-Agent":
                    "RuralBusinessAdvisor/1.0"
            },

            timeout=20
        )


        print(
            "Market API status:",
            response.status_code
        )


        response.raise_for_status()

        data = response.json()

        elements = data.get(
            "elements",
            []
        )


        marketplaces = []

        farm_shops = []

        dairy_shops = []

        vegetable_shops = []


        # =================================================
        # PROCESS PLACES
        # =================================================

        for place in elements:

            tags = place.get(
                "tags",
                {}
            )

            name = tags.get(
                "name"
            )


            if not name:

                continue


            place_type = (

                tags.get(
                    "amenity"
                )

                or

                tags.get(
                    "shop"
                )

                or

                "market"

            )


            market_item = {

                "name":
                    name,

                "type":
                    place_type
            }


            if (
                tags.get("amenity")
                ==
                "marketplace"
            ):

                marketplaces.append(
                    market_item
                )


            elif (
                tags.get("shop")
                ==
                "farm"
            ):

                farm_shops.append(
                    market_item
                )


            elif (
                tags.get("shop")
                ==
                "dairy"
            ):

                dairy_shops.append(
                    market_item
                )


            elif (
                tags.get("shop")
                ==
                "greengrocer"
            ):

                vegetable_shops.append(
                    market_item
                )


        # =================================================
        # REMOVE DUPLICATES
        # =================================================

        def remove_duplicates(items):

            result = []

            seen = set()


            for item in items:

                name = item["name"]

                name_key = (
                    name
                    .strip()
                    .lower()
                )


                if name_key not in seen:

                    seen.add(
                        name_key
                    )

                    result.append(
                        item
                    )


            return result


        marketplaces = remove_duplicates(
            marketplaces
        )

        farm_shops = remove_duplicates(
            farm_shops
        )

        dairy_shops = remove_duplicates(
            dairy_shops
        )

        vegetable_shops = remove_duplicates(
            vegetable_shops
        )


        # =================================================
        # COMBINE ALL MARKETS
        # =================================================

        all_markets = (

            marketplaces

            +

            farm_shops

            +

            dairy_shops

            +

            vegetable_shops

        )


        print(
            "Nearby markets found:",
            len(all_markets)
        )


        return {

            "marketplaces":
                marketplaces,

            "farm_shops":
                farm_shops,

            "dairy_shops":
                dairy_shops,

            "vegetable_shops":
                vegetable_shops,

            "markets":
                all_markets,

            "total_places":
                len(all_markets)
        }


    except requests.exceptions.Timeout:

        print(
            "Nearby market API timed out."
        )

        return None


    except requests.exceptions.RequestException as e:

        print(
            "Nearby market API error:",
            e
        )

        return None


    except ValueError:

        print(
            "Nearby market API returned "
            "invalid JSON."
        )

        return None