import requests


# =================================================
# LOCATION API
# =================================================

def get_location(district, state):

    url = (
        "https://geocoding-api.open-meteo.com/"
        "v1/search"
    )

    # Clean user input
    district = (district or "").strip()
    state = (state or "").strip()

    if not district or not state:

        print(
            "District or state is empty."
        )

        return None

    # First search: district + state
    search_name = f"{district}, {state}"

    params = {
        "name": search_name,
        "count": 10,
        "language": "en",
        "format": "json",
        "countryCode": "IN"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        results = data.get(
            "results",
            []
        )

        print(
            "Location API results:",
            len(results)
        )


        # =================================================
        # FALLBACK SEARCH
        # =================================================

        if not results:

            print(
                "Trying district-only location search..."
            )

            params["name"] = district

            response = requests.get(
                url,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            results = data.get(
                "results",
                []
            )

            print(
                "Fallback location results:",
                len(results)
            )


        if not results:

            print(
                "Location not found."
            )

            return None


        # =================================================
        # FIND STATE MATCH
        # =================================================

        state_lower = (
            state
            .strip()
            .lower()
        )

        for result in results:

            location_name = (
                result.get(
                    "name",
                    ""
                )
                or ""
            )

            location_state = (
                result.get(
                    "admin1",
                    ""
                )
                or ""
            )

            country = (
                result.get(
                    "country",
                    ""
                )
                or ""
            )

            print(
                "Checking location:",
                location_name,
                "| State:",
                location_state,
                "| Country:",
                country
            )

            location_state_lower = (
                location_state
                .strip()
                .lower()
            )


            # Exact state match
            if (
                location_state_lower
                ==
                state_lower
            ):

                location = {

                    "name":
                        location_name,

                    "state":
                        location_state,

                    "latitude":
                        result.get(
                            "latitude"
                        ),

                    "longitude":
                        result.get(
                            "longitude"
                        )
                }

                print(
                    "Location found:",
                    location["name"],
                    "-",
                    location["state"]
                )

                return location


        # =================================================
        # STATE ALIAS CHECK
        # =================================================

        state_aliases = {

            "andhra pradesh":
                [
                    "andhra pradesh"
                ],

            "telangana":
                [
                    "telangana"
                ],

            "tamil nadu":
                [
                    "tamil nadu",
                    "tamil nadu state"
                ],

            "karnataka":
                [
                    "karnataka"
                ],

            "kerala":
                [
                    "kerala"
                ],

            "odisha":
                [
                    "odisha",
                    "orissa"
                ],

            "west bengal":
                [
                    "west bengal"
                ],

            "uttar pradesh":
                [
                    "uttar pradesh"
                ],

            "madhya pradesh":
                [
                    "madhya pradesh"
                ],

            "maharashtra":
                [
                    "maharashtra"
                ],

            "gujarat":
                [
                    "gujarat"
                ],

            "rajasthan":
                [
                    "rajasthan"
                ],

            "bihar":
                [
                    "bihar"
                ],

            "punjab":
                [
                    "punjab"
                ],

            "haryana":
                [
                    "haryana"
                ],

            "assam":
                [
                    "assam"
                ],

            "jharkhand":
                [
                    "jharkhand"
                ],

            "chhattisgarh":
                [
                    "chhattisgarh"
                ]
        }


        aliases = state_aliases.get(
            state_lower,
            [state_lower]
        )


        for result in results:

            location_state = (
                result.get(
                    "admin1",
                    ""
                )
                or ""
            )

            location_state_lower = (
                location_state
                .strip()
                .lower()
            )

            if any(
                alias in location_state_lower
                or
                location_state_lower in alias
                for alias in aliases
            ):

                location = {

                    "name":
                        result.get(
                            "name"
                        ),

                    "state":
                        result.get(
                            "admin1"
                        ),

                    "latitude":
                        result.get(
                            "latitude"
                        ),

                    "longitude":
                        result.get(
                            "longitude"
                        )
                }

                print(
                    "Location found using state alias:",
                    location["name"],
                    "-",
                    location["state"]
                )

                return location


        # =================================================
        # FINAL FALLBACK
        # =================================================

        result = results[0]

        location = {

            "name":
                result.get(
                    "name"
                ),

            "state":
                result.get(
                    "admin1"
                ),

            "latitude":
                result.get(
                    "latitude"
                ),

            "longitude":
                result.get(
                    "longitude"
                )
        }

        print(
            "Location found using fallback:",
            location["name"],
            "-",
            location["state"]
        )

        return location


    except requests.exceptions.Timeout:

        print(
            "Location API timed out."
        )

        return None


    except requests.exceptions.RequestException as e:

        print(
            "Location API error:",
            e
        )

        return None


    except ValueError:

        print(
            "Location API returned invalid JSON."
        )

        return None


# =================================================
# WEATHER API
# =================================================

def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/"
        "v1/forecast"
    )

    params = {

        "latitude": latitude,

        "longitude": longitude,

        "current":
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "weather_code",

        "daily":
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum",

        "forecast_days": 3,

        "timezone": "auto"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        current = data.get(
            "current",
            {}
        )

        daily = data.get(
            "daily",
            {}
        )


        print(
            "Weather data received."
        )


        return {

            "temperature":
                current.get(
                    "temperature_2m"
                ),

            "humidity":
                current.get(
                    "relative_humidity_2m"
                ),

            "precipitation":
                current.get(
                    "precipitation"
                ),

            "weather_code":
                current.get(
                    "weather_code"
                ),

            "max_temperature":
                daily.get(
                    "temperature_2m_max",
                    [None]
                )[0],

            "min_temperature":
                daily.get(
                    "temperature_2m_min",
                    [None]
                )[0],

            "rain_forecast":
                daily.get(
                    "precipitation_sum",
                    [None]
                )[0]
        }


    except requests.exceptions.Timeout:

        print(
            "Weather API timed out."
        )

        return None


    except requests.exceptions.RequestException as e:

        print(
            "Weather API error:",
            e
        )

        return None


    except ValueError:

        print(
            "Weather API returned invalid JSON."
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