import googlemaps

# Replace 'YOUR_API_KEY' with your actual Google Maps API key
gmaps = googlemaps.Client(key='AIzaSyDgGcbEA19O2Pkj6ubXfz5RStdNONvSO0A')


def get_coords_by_name(name):
    # Replace 'Place Name' with the name of the location you want coordinates for
    geocode_result = gmaps.geocode(name)

    # Extract latitude and longitude
    if geocode_result:
        return [geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']]
    else:
        []


def compute_route(origin, destination):
    directions_result = gmaps.directions(origin, destination, mode="driving")
    # Assuming the route is found and we use the first suggested route
    if directions_result:
        route = directions_result[0]['overview_polyline']['points']

        # Generate a static map URL with the encoded route
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?size=500x500&path=enc:{route}&key=AIzaSyDgGcbEA19O2Pkj6ubXfz5RStdNONvSO0A"

        # This URL can be used to view the image in a browser or to download the image programmatically
        return map_url
    else:
        return None


if __name__ == "__main__":
    print(compute_route('51.093111, 71.405951',
                        '51.13967479999999, 71.47695949999999'))
