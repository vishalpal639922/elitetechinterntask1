import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator

# Function to fetch weather data
def fetch_weather_data(api_key, city_list):
    api_key ='6e81be8decaf6ac890fcff457e1daf74'
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    weather_data = []
    
    for city in city_list:
        try:
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'  # Get temperature in Celsius
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raises exception for HTTP errors
            
            data = response.json()
            
            # Extract relevant weather information
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'wind_speed': data['wind']['speed'],
                'weather_condition': data['weather'][0]['main'],
                'cloudiness': data['clouds']['all'] if 'clouds' in data else None
            }
            weather_data.append(weather_info)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {city}: {e}")
    
    return pd.DataFrame(weather_data)

# Function to create visualizations
def create_visualizations(df):
    # Set the style for all visualizations
    sns.set_style("whitegrid")
    sns.set_palette("tab10")
    plt.figure(figsize=(10, 5))
    
    # Visualization 1: Temperature Comparison
    plt.subplot(1, 2, 1)
    temp_plot = sns.barplot(x='city', y='temperature', data=df, edgecolor='black')
    plt.title('Current Temperature by City', pad=20)
    plt.xlabel('City', labelpad=10)
    plt.ylabel('Temperature (°C)', labelpad=10)
    temp_plot.yaxis.set_major_locator(MaxNLocator(integer=True))  # Use integer y-axis
    
    # Add temperature values on top of bars
    for p in temp_plot.patches:
        temp_plot.annotate(f"{p.get_height():.1f}°", 
                          (p.get_x() + p.get_width() / 2., p.get_height()),
                          ha='center', va='center', 
                          xytext=(0, 7), 
                          textcoords='offset points')
    
    # Visualization 2: Humidity Comparison
    plt.subplot(1, 2, 2)
    hum_plot = sns.barplot(x='city', y='humidity', data=df, edgecolor='black')
    plt.title('Current Humidity by City', pad=20)
    plt.xlabel('City', labelpad=10)
    plt.ylabel('Humidity (%)', labelpad=10)
    
    # Add humidity values on top of bars
    for p in hum_plot.patches:
        hum_plot.annotate(f"{p.get_height():.1f}%", 
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center', 
                         xytext=(0, 7), 
                         textcoords='offset points')
    
    plt.tight_layout()
    plt.show()
    
    # Visualization 3: Weather Conditions Pie Chart
    condition_counts = df['weather_condition'].value_counts()
    plt.figure(figsize=(8, 6))
    plt.pie(condition_counts, 
            labels=condition_counts.index, 
            autopct='%1.1f%%',
            shadow=True,
            explode=[0.1] * len(condition_counts))
    plt.title('Weather Condition Distribution Across Cities')
    plt.show()

# Main program
if __name__ == "__main__":
    print("Weather Data Visualization Program")
    print("---------------------------------")
    
    # Get API key from user
    api_key = input("Enter your OpenWeatherMap API key: ").strip()
    
    # List of cities to compare
    cities = ["London", "New York", "Tokyo", "Sydney", "Dubai", "Paris"]
    
    print("\nFetching weather data...")
    weather_df = fetch_weather_data(api_key, cities)
    
    if weather_df.empty:
        print("No data retrieved. Please check your API key and internet connection.")
    else:
        print("\nWeather Data Retrieved:")
        print(weather_df[['city', 'country', 'temperature', 'humidity', 'weather_condition']])
        
        print("\nCreating visualizations...")
        create_visualizations(weather_df)
