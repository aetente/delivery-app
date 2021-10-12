# i didn't get about the courier api
# because there are many services
# and I don't think there is one to generate timeslots
# or something like that
# so I just generated timeslots json file on my own

import json
import random
from datetime import datetime, timedelta
import os
import holidayapi

# type of places from google geocoding api docs:
# # https://developers.google.com/maps/documentation/places/web-service/supported_types
# it is to set which type of address the timeslot supports
PLACE_TYPES = [
    "accounting",
    "airport",
    "amusement_park",
    "aquarium",
    "art_gallery",
    "atm",
    "bakery",
    "bank",
    "bar",
    "beauty_salon",
    "bicycle_store",
    "book_store",
    "bowling_alley",
    "bus_station",
    "cafe",
    "campground",
    "car_dealer",
    "car_rental",
    "car_repair",
    "car_wash",
    "casino",
    "cemetery",
    "church",
    "city_hall",
    "clothing_store",
    "convenience_store",
    "courthouse",
    "dentist",
    "department_store",
    "doctor",
    "drugstore",
    "electrician",
    "electronics_store",
    "embassy",
    "fire_station",
    "florist",
    "funeral_home",
    "furniture_store",
    "gas_station",
    "gym",
    "hair_care",
    "hardware_store",
    "hindu_temple",
    "home_goods_store",
    "hospital",
    "insurance_agency",
    "jewelry_store",
    "laundry",
    "lawyer",
    "library",
    "light_rail_station",
    "liquor_store",
    "local_government_office",
    "locksmith",
    "lodging",
    "meal_delivery",
    "meal_takeaway",
    "mosque",
    "movie_rental",
    "movie_theater",
    "moving_company",
    "museum",
    "night_club",
    "painter",
    "park",
    "parking",
    "pet_store",
    "pharmacy",
    "physiotherapist",
    "plumber",
    "police",
    "post_office",
    "primary_school",
    "real_estate_agency",
    "restaurant",
    "roofing_contractor",
    "rv_park",
    "school",
    "secondary_school",
    "shoe_store",
    "shopping_mall",
    "spa",
    "stadium",
    "storage",
    "store",
    "subway_station",
    "supermarket",
    "synagogue",
    "taxi_stand",
    "tourist_attraction",
    "train_station",
    "transit_station",
    "travel_agency",
    "university",
    "veterinary_care",
    "zoo",
    "administrative_area_level_1",
    "administrative_area_level_2",
    "administrative_area_level_3",
    "administrative_area_level_4",
    "administrative_area_level_5",
    "archipelago",
    "colloquial_area",
    "continent",
    "country",
    "establishment",
    "finance",
    "floor",
    "food",
    "general_contractor",
    "geocode",
    "health",
    "intersection",
    "landmark",
    "locality",
    "natural_feature",
    "neighborhood",
    "place_of_worship",
    "plus_code",
    "point_of_interest",
    "political",
    "post_box",
    "postal_code",
    "postal_code_prefix",
    "postal_code_suffix",
    "postal_town",
    "premise",
    "room",
    "route",
    "street_address",
    "street_number",
    "sublocality",
    "sublocality_level_1",
    "sublocality_level_2",
    "sublocality_level_3",
    "sublocality_level_4",
    "sublocality_level_5",
    "subpremise",
    "town_square"
]

HOLIDAY_API = os.environ.get("HOLIDAY_API")
hapi = holidayapi.v1("a4f33a8e-43b3-4c75-8173-79f279e28f81")

WORKDAY_HOURS = 8
MAX_DELIVERIES_PER_DAY = 10
MAX_MINUTES_PER_SLOT = 60 * WORKDAY_HOURS / MAX_DELIVERIES_PER_DAY
NUMBER_OF_SUPPORTED_PLACE_TYPES = 5

parameters = {
    'country': 'IL',
    'year':    datetime.today().year - 1
}  # minus one because they don't allow free accounts to get current year's holidays, only for previous years

holidays = hapi.holidays(parameters)


def gen_json():
    todays_date = datetime.today()
    todays_date = todays_date.replace(
        hour=9, minute=0, second=0)  # starting from today

    the_timeslots = []  # timeslot for upcoming week
    start_time = todays_date  # start time for a timeslot
    pk = 0  # id
    for i in range(0, 7):  # days
        day_timeslots = []  # timeslots for a day

        is_holiday = False  # check for holidays this day
        for holiday in holidays["holidays"]:
            holiday_date = datetime.strptime(holiday["date"], '%Y-%m-%d')
            if (start_time.month == holiday_date.month and start_time.day == holiday_date.day):
                is_holiday = True
                break
        if (is_holiday):
            continue

        for j in range(0, MAX_DELIVERIES_PER_DAY):  # deliveries per day
            if (random.random() > 0.8):  # it doesn't have to be all 10 deliveries per day
                continue
            slot_work_time = round(MAX_MINUTES_PER_SLOT *
                                   (0.8 + random.random() * 0.2))  # random minutes in range
            # end time for the timeslot
            end_time = start_time + timedelta(minutes=slot_work_time)
            the_timeslots.append({
                "model": "deliveryapp.Timeslot",
                "pk": pk,
                "fields": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "type_of_address": ",".join(random.sample(PLACE_TYPES, NUMBER_OF_SUPPORTED_PLACE_TYPES))
                }
            })
            start_time = end_time  # next timeslot starts with the end time of previous time slot
            pk += 1  # next id
        # the_timeslots.append(day_timeslots)  # append timeslots for a day
        start_time = start_time + timedelta(days=1)  # next day
        start_time = start_time.replace(hour=9, minute=0, second=0)

    with open('deliveryapp/fixtures/timeslots.json', 'w') as outfile:  # write the json file
        json.dump(the_timeslots, outfile, default=str)


gen_json()
