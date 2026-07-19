import re

# Disaster Mapping Dictionary

DISASTER_MAPPING = {

    "411001": "Flood",
    "411002": "Flood",
    "400001": "Fire",
    "422001": "Heatwave",
    "415001": "Cyclone",
    "440001": "Earthquake"

}


# Validate Pincode

def validate_pincode(pincode):

    pattern = r"^[1-9][0-9]{5}$"

    if not re.match(pattern, pincode):

        raise Exception("Invalid Pincode Format")

    return True


# Get Disaster

def get_disaster(pincode):

    validate_pincode(pincode)

    if pincode not in DISASTER_MAPPING:

        raise Exception("Unknown Pincode")

    return DISASTER_MAPPING[pincode]