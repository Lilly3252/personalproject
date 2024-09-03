from flask import Flask, render_template_string
import requests

app = Flask(__name__)

# Function to search for houses
def search_houses(api_key, latitude_max, latitude_min, longitude_max, longitude_min, current_page=1, records_per_page=10, sort_order='A', sort_by='1', culture_id='1', number_of_days='0', bed_range='0-0', bath_range='0-0', price_min='0',price_max="",transaction_type_id="2",property_search_type_id="1"):
    url = "https://realty-in-ca1.p.rapidapi.com/properties/list-residential"
    querystring = {
        "LatitudeMax": latitude_max,
        "LatitudeMin": latitude_min,
        "LongitudeMax": longitude_max,
        "LongitudeMin": longitude_min,
        "CurrentPage": current_page,
        "RecordsPerPage": records_per_page,
        "SortOrder": sort_order,
        "SortBy": sort_by,
        "CultureId": culture_id,
        "NumberOfDays": number_of_days,
        "BedRange": bed_range,
        "BathRange": bath_range,
        "PriceMin":price_min,
        "PriceMax":price_max,
        "TransactionType":transaction_type_id,
        "property_search_type_id":property_search_type_id
    }
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "realty-in-ca1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

# Your API key
api_key = ''

@app.route('/')
def home():
    latitude_max = "45.652"
    latitude_min = "45.112"
    longitude_max = "-71.587"
    longitude_min = "-72.354"
    current_page = "1"
    records_per_page = "200"
    sort_order = "A"
    sort_by = "1"
    culture_id = "2"
    number_of_days = "0"
    transaction_type_id = "2"
    property_search_type_id = "1"
    bed_range = "2-0"
    bath_range = "0-0"
    price_min = "60000"
    price_max = "200000"

    houses = search_houses(api_key, latitude_max, latitude_min, longitude_max, longitude_min, current_page, records_per_page, sort_order, sort_by, culture_id, number_of_days, bed_range, bath_range, price_min, price_max, transaction_type_id, property_search_type_id)

    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>House Listings</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }
            .container {
                width: 80%;
                margin: 0 auto;
                padding: 20px;
            }
            .house {
                display: flex;
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            .house img {
                max-width: 300px;
                height: auto;
                border-radius: 5px;
                margin-right: 20px;
            }
            .house-details {
                flex: 1;
                padding-right: 20px;
            }
            .house-extra {
                flex: 1;
                padding-left: 20px;
                border-left: 1px solid #ddd;
            }
            .house h2 {
                margin-top: 0;
            }
            .house p {
                margin: 5px 0;
            }
            .house a {
                color: #007BFF;
                text-decoration: none;
            }
            .house a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>House Listings</h1>
            {% for house in houses %}
            <div class="house">
                {% if house['Property']['Photo'] %}
                <img src="{{ house['Property']['Photo'][0]['HighResPath'] }}" alt="House Image">
                {% endif %}
                <div class="house-details">
                    <h2>{{ house['Property']['Address']['AddressText'] }}</h2>
                    <p><strong>Price:</strong> {{ house['Property']['Price'] }}</p>
                    <p><strong>Bathrooms:</strong> {{ house['Building'].get('BathroomTotal', 'N/A') }}</p>
                    <p><strong>Bedrooms:</strong> {{ house['Building'].get('Bedrooms', 'N/A') }}</p>
                    <p><strong>House Type:</strong> {{ house['Property']['Type'] }}</p>
                    <p><strong>Link:</strong> <a href="https://www.realtor.ca{{ house['RelativeDetailsURL'] }}">More Info</a></p>
                </div>
                <div class="house-extra">
                    <p><strong>Property Size:</strong> {{ house['Land'].get('SizeTotal', 'N/A') }}</p>
                    <p><strong>Amenities Nearby:</strong> {{ house['Property'].get('AmmenitiesNearBy', 'N/A') }}</p>
                    <p><strong>Map View:</strong> <a href="https://www.google.com/maps/search/?api=1&query={{ house['Property']['Address']['Latitude'] }},{{ house['Property']['Address']['Longitude'] }}" target="_blank">View on Map</a></p>
                </div>
            </div>
            {% endfor %}
        </div>
    </body>
    </html>
    '''

    return render_template_string(html_template, houses=houses['Results'])

if __name__ == '__main__':
    app.run(debug=True)
