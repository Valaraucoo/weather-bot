import json
import random
from typing import Dict, Final

import boto3
import requests

page_id: Final[str] = "205621463221358"
city: Final[str] = "Gorlice"

region_name: Final[str] = "eu-central-1"

additional_emojis: Final[Dict[str, str]] = {
    "rain": "๐งโ๏ธ๐ฌ๏ธ๐ฅ๐๐งโ๏ธโฑ๏ธ",
    "sun": "โ๏ธ๐๐ค๏ธ๐ฅ๏ธ๐ฆ๏ธ๐๐ป๐๐๐๐๐๐๐๐",
}


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


def random_emoji(key: str) -> str:
    if random.random() < 0.2:
        return ""
    return random.choice(additional_emojis[key])


def build_message() -> str:
    weather = retrieve_weather()
    current = weather["current"]
    condition = current["condition"]["text"]

    sun_emoji = random_emoji("sun")
    rain_emoji = random_emoji("rain")

    if condition == "Sunny":
        return "Nie โ๏ธ" + sun_emoji
    elif condition == "Clear":
        return "Nie โ๏ธ" + sun_emoji
    elif condition == "Partly cloudy":
        return "Nie ๐ค" + sun_emoji
    elif condition == "Cloudy":
        return "Nie ๐ฅ" + sun_emoji
    elif condition == "Overcast":
        return "Nie ๐ฅ" + sun_emoji
    elif condition == "Mist":
        return "Nie ๐ซ" + sun_emoji
    elif condition == "Patchy rain possible":
        return "Nie, ale moลผe padaฤ ๐ง"
    elif condition == "Patchy snow possible":
        return "Nie, ale moลผe padaฤ ๐จ"
    elif "rain" in condition.lower():
        return "Tak ๐ง" + rain_emoji
    return "Nie" + sun_emoji


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
