from .config import google_key
import googlemaps
from datetime import datetime
import geocoder
import random


level1 = [(49.3102532, -123.1354091, 2),(49.2782907, -123.2116968, 1.25),(49.2090777302915,  -123.1492562697085, 2),(49.2438900802915,  -123.1954874697085, 3.5),(49.2310237302915,  -123.1893038197085, 0),(49.21826628029149,  -123.2035735197085, 2)]
level2 = [(49.2450285802915,  -123.2110626197085, 4),(49.4294044802915,  -123.2047621197085, 2.6),(49.2587252302915,  -123.2301433197085, 1.3
),(49.2826071,  -123.2257202, 1.6),(49.39468228029151,  -122.9430954197085, 5),(49.2379625302915,  -123.1955518697085, 3)]
level3 = [(49.3574806802915,  -123.0356026197085, 4),(49.3793121,  -123.0825127, 5.5)]

gmaps = googlemaps.Client(key=google_key)

# Geocoding an address
geocode_result = gmaps.geocode('1333 E.55th ave vancouver')
print(geocode_result[0]['formatted_address'])
#print(geocode_result)
# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("UBC bus loop",
                                     "1333 E.55th ave, vancouver BC, canada",
                                     mode="transit",
                                     departure_time=now)
directions2 = []
#print(directions_result)
def print_directions(response,directions):
    if type(response) == list:
        for i in response:
            print_directions(i,directions)
        return directions
    if type(response) == dict:
        for key in response.keys():
            if key == "steps" or key=="html_instructions" or key=="legs"  or key=="distance" or key=="transit_details" or key== "duration"or key=="text" or key=="short_name" or key=="line" or key=="arrival_stop" or key=='name' or key=="num_stops":
                print_directions(response[key],directions)
        return directions
    directions.append(response)
    return directions

def find_valid_location(level,location):
    valid = []
    if level == 1:
        locations = level1
    if level == 2:
        locations = level2
    if level == 3:
        locations = level3
    for i in range(len(locations)):
        if not abs(locations[i][0] - location["lat"]) > 0.5 and not abs(locations[i][1] - location["lng"]) > 0.5: 
            valid.append(locations[i])
    return valid

def timeconversion(time):
    split = time.split()
    if len(split)>2:
        return int(split[0]) + int(split[2])/60
    else:
        return int(split[0])/60

def returninfo(level,location,time):
    coords = gmaps.geocode(location)[0]['geometry']['viewport']['northeast']
    possibilities = find_valid_location(level,coords)
    valid = []
    
    for possible in possibilities:
        directions_result = print_directions(gmaps.directions(coords,
                                        possible,
                                        mode="transit",
                                        departure_time=now),[])
        if not directions_result:
            continue
        if timeconversion(directions_result[1])*2+possible[2] < time:
            valid.append(possible)

    finallocation = random.choice(valid)
    directions_result = gmaps.directions(coords,
                                    finallocation,
                                    mode="transit",
                                    departure_time=now)
    return print_directions(directions_result,[])
    


                

# directions = print_directions(directions_result,directions2)
# distance = directions[0].split('\n')[0]
# print(f'The trip to your location will be {distance} and take {directions[1]}')
# print(returninfo(1,"UBC nest",3))

# Validate an address with address validation
addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
                                                    regionCode='US',
                                                    locality='Mountain View', 
                                                    enableUspsCass=True)