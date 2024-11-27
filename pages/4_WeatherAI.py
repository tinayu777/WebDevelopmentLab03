import openai  # If using OpenAI, or similar library if using Gemini
import json

# Set your API key for the Google Gemini or OpenAI LLM
API_KEY = 'your_api_key_here'
openai.api_key = API_KEY

def generate_weather_report(weather_data):
    prompt = f"Generate a weather forecast based on the following data: {weather_data}"
    
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # or "google-gemini" if using Gemini
            prompt=prompt,
            max_tokens=150
        )
        report = response.choices[0].text.strip()
        return report
    except Exception as e:
        return f"Error generating report: {str(e)}"

import streamlit as st
import requests
import openai

# Your OpenWeatherMap API key
API_KEY = "your_openweathermap_api_key_here"

# Streamlit setup
st.title("Weather Analysis with LLM 🌤")
st.markdown("Generate weather reports or interact with a weather chatbot based on real-time data.")

# User inputs
location = st.text_input("Enter city:", "Atlanta")
forecast_date = st.date_input("Select date for forecast:", None)

# Fetch weather data for the selected city
def fetch_weather_data(location, date=None):
    unit = "metric"  # Default to Celsius
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid={API_KEY}"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            return response
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

weather_data = fetch_weather_data(location)

# If weather data is available, pass it to LLM for report generation
if weather_data:
    weather_report = generate_weather_report(weather_data)
    st.subheader("Generated Weather Report")
    st.write(weather_report)
def generate_chatbot_response(question, weather_data):
    prompt = f"Given the weather data: {weather_data}, answer the following question: {question}"

    try:
        response = openai.Completion.create(
            engine="gpt-4",  # Replace with Gemini if needed
            prompt=prompt,
            max_tokens=100
        )
        chatbot_response = response.choices[0].text.strip()
        return chatbot_response
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Chatbot interface
user_question = st.text_input("Ask the weather chatbot:", "")
if user_question:
    response = generate_chatbot_response(user_question, weather_data)
    st.write(f"Chatbot: {response}")
try:
    weather_data = fetch_weather_data(location)
    if weather_data:
        weather_report = generate_weather_report(weather_data)
except Exception as e:
    st.error(f"An error occurred: {str(e)}")

