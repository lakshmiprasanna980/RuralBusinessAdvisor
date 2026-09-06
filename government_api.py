import requests


# =================================================
# DATA.GOV.IN API CONFIGURATION
# =================================================

DATA_GOV_API_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"

MANDI_RESOURCE_ID = (
    "9ef84268-d588-465a-a308-a864a43d0070"
)


# =================================================
# GOVERNMENT SCHEME RECOMMENDATIONS
# =================================================

def get_government_schemes(
    business,
    investment,
    state
):

    schemes = []


    # =================================================
    # PMEGP
    # =================================================

    if business in [
        "Dairy Farming",
        "Poultry Farming",
        "Food Processing",
        "Handicrafts",
        "Retail Shop"
    ]:

        schemes.append({

            "name":
                "Prime Minister's Employment "
                "Generation Programme (PMEGP)",

            "description":
                "A Government of India programme "
                "that supports eligible new "
                "micro-enterprises.",

            "reason":
                "Your selected business may "
                "qualify as a micro-enterprise.",

            "source":
                "Government of India / KVIC"

        })


    # =================================================
    # MUDRA
    # =================================================

    if investment <= 1000000:

        schemes.append({

            "name":
                "Pradhan Mantri Mudra Yojana (PMMY)",

            "description":
                "A financing scheme intended to "
                "support eligible micro and small "
                "business activities.",

            "reason":
                "Your reported investment is "
                "within a range worth checking "
                "for suitable financing.",

            "source":
                "Government of India / myScheme"

        })


    # =================================================
    # FOOD PROCESSING
    # =================================================

    if business == "Food Processing":

        schemes.append({

            "name":
                "Food Processing Support",

            "description":
                "Explore government programmes "
                "available to eligible food "
                "processing enterprises.",

            "reason":
                "You selected Food Processing "
                "as your business.",

            "source":
                "Check official government portals"

        })


    # =================================================
    # HANDICRAFTS
    # =================================================

    if business == "Handicrafts":

        schemes.append({

            "name":
                "Handicraft Entrepreneurship Support",

            "description":
                "Explore government support "
                "available to eligible artisans "
                "and handicraft entrepreneurs.",

            "reason":
                "You selected Handicrafts "
                "as your business.",

            "source":
                "Check official government portals"

        })


    return schemes


# =================================================
# GOVERNMENT MANDI DATA
# =================================================

def get_mandi_data(
    state=None,
    district=None,
    commodity=None,
    limit=10
):

    """
    Fetch mandi price data from Data.gov.in.

    This function returns an empty list instead
    of crashing if the API is unavailable.
    """

    url = (
        "https://api.data.gov.in/resource/"
        + MANDI_RESOURCE_ID
    )


    params = {

        "api-key":
            DATA_GOV_API_KEY,

        "format":
            "json",

        "limit":
            limit

    }


    # =================================================
    # STATE FILTER
    # =================================================

    if state:

        params["filters[state]"] = state


    # =================================================
    # DISTRICT FILTER
    # =================================================

    if district:

        params["filters[district]"] = district


    # =================================================
    # COMMODITY FILTER
    # =================================================

    if commodity:

        params["filters[commodity]"] = commodity


    try:

        print(
            "Requesting Data.gov.in mandi data..."
        )

        response = requests.get(

            url,

            params=params,

            timeout=20

        )


        print(
            "Data.gov.in status:",
            response.status_code
        )


        response.raise_for_status()


        data = response.json()


        records = data.get(
            "records",
            []
        )


        if not records:

            print(
                "No mandi records found."
            )

            return []


        print(
            "Mandi records received:",
            len(records)
        )


        return records


    except requests.exceptions.Timeout:

        print(
            "Data.gov.in API timed out."
        )

        return []


    except requests.exceptions.RequestException as e:

        print(
            "Data.gov.in API error:",
            e
        )

        return []


    except ValueError:

        print(
            "Data.gov.in returned invalid JSON."
        )

        return []