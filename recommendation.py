import streamlit as st
import pandas as pd
import random
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Function to calculate distance between two geographical points (latitude, longitude)
def calculate_distance(point1, point2):
    return geodesic(point1, point2).kilometers

# Function to generate fake bus routes
def generate_bus_routes(num_routes):
    routes = []
    for i in range(num_routes):
        route_id = i + 1
        route_name = f"Route {route_id}"
        routes.append({'route_id': route_id, 'route_name': route_name})
    return routes

# Function to generate fake bus stops
def generate_bus_stops(num_stops):
    stops = []
    for i in range(num_stops):
        stop_id = i + 1
        latitude = round(random.uniform(0, 90), 6)  # Random latitude
        longitude = round(random.uniform(0, 180), 6)  # Random longitude
        stops.append({'stop_id': stop_id, 'latitude': latitude, 'longitude': longitude})
    return stops

# Function to generate fake bus timetable
def generate_bus_timetable(routes, stops):
    timetable = []
    for route in routes:
        for stop in stops:
            timetable.append({'route_id': route['route_id'], 'stop_id': stop['stop_id'], 'departure_time': generate_departure_time()})
    return timetable

# Function to generate fake departure time
def generate_departure_time():
    hour = random.randint(6, 21)  # Random hour between 6 AM and 9 PM
    minute = random.randint(0, 59)  # Random minute
    return f"{hour:02d}:{minute:02d}:00"

# Function to recommend available buses passing through the nearest stop to the user's location
def recommend_bus(user_location_name, stops_df, timetable_df):
    # Convert location name to geographical coordinates
    geolocator = Nominatim(user_agent="bus_recommendation_app")
    location = geolocator.geocode(user_location_name)
    if location:
        user_location = (location.latitude, location.longitude)
    else:
        return pd.DataFrame()  # Return an empty DataFrame if location not found
    
    # Calculate distances between user location and all bus stops
    stops_df['distance'] = stops_df.apply(lambda row: calculate_distance(user_location, (row['latitude'], row['longitude'])), axis=1)
    
    # Find the nearest bus stop
    nearest_stop = stops_df.loc[stops_df['distance'].idxmin()]
    
    # Find all buses passing through the nearest stop
    buses_passing_stop = timetable_df[timetable_df['stop_id'] == nearest_stop['stop_id']]
    
    # Convert departure_time column in timetable_df to datetime format
    buses_passing_stop['departure_time'] = pd.to_datetime(buses_passing_stop['departure_time'])
    
    # Get the list of available buses passing through the nearest stop
    current_time = pd.Timestamp.now()
    today_timetable = buses_passing_stop[buses_passing_stop['departure_time'].dt.date == current_time.date()]
    tomorrow_timetable = buses_passing_stop[buses_passing_stop['departure_time'].dt.date == (current_time + pd.Timedelta(days=1)).date()]
    available_buses = pd.concat([today_timetable, tomorrow_timetable])
    available_buses = available_buses[available_buses['departure_time'] > current_time]
    
    return available_buses

# Function to main Streamlit app
def main():
    st.title("Bus Recommendation System")

    # Generate fake bus routes, stops, and timetable
    num_routes = 110  # Increase the number of routes
    num_stops = 55  # Increase the number of stops
    routes = generate_bus_routes(num_routes)
    stops = generate_bus_stops(num_stops)
    timetable = generate_bus_timetable(routes, stops)

    # Create DataFrames
    routes_df = pd.DataFrame(routes)
    stops_df = pd.DataFrame(stops)
    timetable_df = pd.DataFrame(timetable)

    # List of custom cities
    custom_cities = [
        "Alandurai",
        "Anaimalai",
        "Annur",
        "Arasur, Coimbatore",
        "Chettipalayam",
        "Chinnavedampatti",
        "Coimbatore",
        "Dhaliyur",
        "Eachanari",
        "Ettimadai",
        "Gudalur (Coimbatore district)",
        "Idikarai",
        "Irugur",
        "Kangayampalayam",
        "Kaniyur, Coimbatore",
        "Kannampalayam",
        "Karamadai",
        "Karumathampatti",
        "Kinathukadavu",
        "Kottur-Malayandipattinam",
        "Kovaipudur",
        "Madukkarai",
        "Malumichampatti",
        "Marudhamalai",
        "Mettupalayam, Coimbatore",
        "Mopperipalayam",
        "Muthugoundenpudur",
        "Narasimhanaickenpalayam",
        "Neelambur",
        "Odaiyakulam",
        "Othakalmandapam",
        "Pallapalayam, Coimbatore",
        "Pattanam, Coimbatore",
        "Periya Negamam",
        "Periyanaickenpalayam",
        "Pollachi",
        "Pooluvapatti",
        "Samathur",
        "Saravanampatti",
        "Sarcarsamakulam",
        "Sirumugai",
        "Somayampalayam",
        "Suleeswaranpatti",
        "Sulur",
        "Thekkupalayam",
        "Thenkarai, Coimbatore",
        "Thirumalayampalayam",
        "Thondamuthur",
        "Uliyampalayam",
        "Valparai",
        "Vedapatti",
        "Veerapandi, Coimbatore",
        "Vellakinar",
        "Vettaikaranpudur",
        "Zamin Uthukuli"
    ]
    
    # Get user location name
    user_location_name = st.selectbox("Select your city:", custom_cities)

    if st.button("Recommend Bus"):
        available_buses = recommend_bus(user_location_name, stops_df, timetable_df)

        # Display available buses passing through the nearest stop to the user's location
        if available_buses.empty:
            st.write("No available buses passing through the nearest stop to your location at the moment.")
        else:
            st.write("Available Buses Passing Through the Nearest Stop:")
            st.write(available_buses)

# Run the Streamlit app
if __name__ == "__main__":
    main()