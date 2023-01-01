import json
from typing import Dict, Final

import boto3
import requests

page_id: Final[str] = "205621463221358"
city: Final[str] = "Gorlice"

region_name: Final[str] = "eu-central-1"


session = boto3.session.Session()
client = session.client(
    service_name="secretsmanager",
    region_name=region_name
)

def retrieve_secret(secret_name: str) -> Dict:
    secret_response = client.get_secret_value(
        SecretId=secret_name
    )
    secret = json.loads(secret_response["SecretString"])
    return secret


def retrieve_fb_access_key() -> str:
    return retrieve_secret("Facebook-API-Access-Key")["ACCESS_KEY"]


def retrieve_weather_api_access_key() -> str:
    return retrieve_secret("WeatherAPI-Access-Key")["ACCESS_KEY"]

def retrieve_weather() -> Dict:
    access_key = retrieve_weather_api_access_key()
    response = requests.get(f"https://api.weatherapi.com/v1/current.json?key={access_key}&q={city}&aqi=no")
    return response.json()


def build_message() -> str:
    weather = retrieve_weather()
    current = weather["current"]
    condition = current["condition"]["text"]

    if condition == "Sunny":
        return "Nie ☀️"
    elif condition == "Clear":
        return "Nie ☀️"
    elif condition == "Partly cloudy":
        return "Nie 🌤"
    elif condition == "Cloudy":
        return "Nie 🌥"
    elif condition == "Overcast":
        return "Nie 🌥"
    elif condition == "Mist":
        return "Nie 🌫"
    elif condition == "Patchy rain possible":
        return "Nie, ale może padać 🌧"
    elif condition == "Patchy snow possible":
        return "Nie, ale może padać 🌨"
    elif "rain" in condition.lower():
        return "Tak 🌧"
    return "Nie"


def publish_post() -> Dict:
    access_key = retrieve_fb_access_key()
    message = build_message()
    response = requests.post(f"https://graph.facebook.com/{page_id}/feed?access_token={access_key}&message={message}")
    return response.json()


def lambda_handler(event: Dict, context: Dict) -> Dict:
    response = publish_post()
    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }
