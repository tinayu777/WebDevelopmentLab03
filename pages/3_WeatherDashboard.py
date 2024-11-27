import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Title and Introduction
st.title("Real-Time Weather Dashboard 🌦")
st.markdown(
    """
    This app provides current weather data and a simulated temperature trend for your selected location.
    Built with the OpenWeatherMap API, it offers dynamic insights based on user preferences.
    """
)

# Input Section
API_KEY = "579ca185eb5c3e9e35f93b2664bd0380"  # Replace with your actual API key

st.sidebar.header("User Input")
location = st.sidebar.text_input("Enter a city name (e.g., London):", "Atlanta")  # Input 1
metric = st.sidebar.radio("Choose temperature unit:", ("Celsius", "Fahrenheit"))  # Input 2

# Fetch Weather Data
if location:
    unit = "metric" if metric == "Celsius" else "imperial"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid={API_KEY}"
    response = requests.get(url).json()

    if response.get("cod") == 200:
        # Extract Data
        weather_data = {
            "City": response["name"],
            "Temperature": response["main"]["temp"],
            "Humidity": response["main"]["humidity"],
            "Weather Condition": response["weather"][0]["description"].title(),
        }

        # Display Weather Metrics
        st.header(f"Current Weather in {weather_data['City']}")
        st.metric("Temperature", f"{weather_data['Temperature']}° {metric}")
        st.metric("Humidity", f"{weather_data['Humidity']}%")
        st.write(f"Weather Condition: {weather_data['Weather Condition']}")

        # Simulated Temperature Trend
        st.subheader("Simulated 7-Day Temperature Trend")
        days = list(range(1, 8))
        temps = [weather_data["Temperature"] - i for i in days]  # Simulate trend

        # Create DataFrame for Visualization
        trend_data = pd.DataFrame({"Day": days, "Temperature": temps})

        # Visualization
        fig, ax = plt.subplots()
        ax.plot(trend_data["Day"], trend_data["Temperature"], marker="o")
        ax.set_title("Simulated Temperature Trend")
        ax.set_xlabel("Day")
        ax.set_ylabel(f"Temperature ({metric})")
        st.pyplot(fig)  # NEW: Dynamic visualization using matplotlib

    else:
        st.error("City not found. Please try a different location.")
else:
    st.warning("Please enter a city name to get started.")
