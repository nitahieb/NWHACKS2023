import config
import googlemaps
from datetime import datetime
import geocoder
g = geocoder.ip('me')
print(g.latlng)

google_key = config.google_key

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

print(directions_result)
def print_directions(response):
    if type(response) == list:
        for i in response:
            print_directions(i)
        return
    if type(response) == dict:
        for key in response.keys():
            if key == "steps" or key=="html_instructions" or key=="legs"  or key=="distance" or key=="transit_details" or key== "duration"or key=="text" or key=="short_name" or key=="line" or key=="arrival_stop" or key=='name' or key=="num_stops":
                print_directions(response[key])
        return
    print(response)

                

        

print_directions(directions_result)

# Validate an address with address validation
addressvalidation_result =  gmaps.addressvalidation(['1600 Amphitheatre Pk'], 
                                                    regionCode='US',
                                                    locality='Mountain View', 
                                                    enableUspsCass=True)