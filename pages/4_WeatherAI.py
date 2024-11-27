import openai  # For OpenAI API integration
import streamlit as st
import requests
import json

# Set your API key for the OpenAI (or Google Gemini) LLM
API_KEY = '579ca185eb5c3e9e35f93b2664bd0380'  # Replace with your actual OpenAI API key
openai.api_key = API_KEY

# Function to generate a weather report using OpenAI's GPT model
def generate_weather_report(weather_data):
    prompt = f"Generate a weather forecast based on the following data: {weather_data}"
    
    try:
        # Adjust API call to match OpenAI's new API interface
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or use "google-gemini" if you're using Gemini
            messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                      {"role": "user", "content": prompt}],
            max_tokens=150
        )
        report = response['choices'][0]['message']['content'].strip()
        return report
    except Exception as e:
        return f"Error generating report: {str(e)}"

# Function to fetch weather data from OpenWeatherMap API
def fetch_weather_data(location):
    unit = "metric"  # Default to Celsius
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units={unit}&appid=your_openweathermap_api_key_here"
    
    try:
        response = requests.get(url).json()
        if response.get("cod") == 200:
            return response
        else:
            return None
    except Exception as e:
        st.error(f"Error fetching weather data: {str(e)}")
        return None

# Function to generate chatbot responses
def generate_chatbot_response(question, weather_data):
    prompt = f"Given the weather data: {weather_data}, answer the following question: {question}"
    
    try:
        # Adjust API call to match OpenAI's new API interface
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or use "google-gemini" if you're using Gemini
            messages=[{"role": "system", "content": "You are a helpful assistant."}, 
                      {"role": "user", "content": prompt}],
            max_tokens=100
        )
        chatbot_response = response['choices'][0]['message']['content'].strip()
        return chatbot_response
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Streamlit setup
st.title("Weather Analysis with LLM 🌤")
st.markdown("Generate weather reports or interact with a weather chatbot based on real-time data.")

# User inputs for city and forecast date
location = st.text_input("Enter city:", "Atlanta")
forecast_date = st.date_input("Select date for forecast:", None)

# Fetch weather data for the selected city
weather_data = fetch_weather_data(location)

# If weather data is available, pass it to LLM for report generation
if weather_data:
    weather_report = generate_weather_report(weather_data)
    st.subheader("Generated Weather Report")
    st.write(weather_report)

# Chatbot interface for weather-related questions
user_question = st.text_input("Ask the weather chatbot:", "")
if user_question:
    if weather_data:
        chatbot_response = generate_chatbot_response(user_question, weather_data)
        st.write(f"Chatbot: {chatbot_response}")
    else:
        st.write("Sorry, no weather data available to answer your question.")




