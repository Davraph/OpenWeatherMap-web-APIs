import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

#hourly weather forecast

WEATHER_ENDPOINTS = 'https://api.openweathermap.org/data/2.5/onecall'
api_key = os.environ.get('API_KEY')
account_sid = "YOUR ACCOUNT SID"
auth_token = os.environ.get("AUTH_TOKEN")

weather_params = {
    "lat": 52.229675,
    "lon": 21.012230,
    "appid": api_key,
    "exlude": "current,minutely, daily"
}


response = requests.get(WEATHER_ENDPOINTS, params=weather_params)
response.raise_for_status()
weather_data = response.json()

#using python slice function tap into 12 hour weather condtions and weather first id
weather_slice = weather_data["hourly"][:12]

will_rain = False
be_Sunny = False
will_snow = False

for hour_data in weather_slice:
    condition_weather_code = hour_data["weather"][0]["id"]
    if int(condition_weather_code) < 600:
        will_rain = True

    if int(condition_weather_code) > 800:
        be_sunny = True
    else:
        will_snow = True

if will_rain:
    print("Bring an Umbrella")


if be_sunny:
    print("It sunny today Enjoy the weather!!")

#Using Twillio api sms alert using a api that allow to send sms , phone call ,virtual phone number Read about Twillio
# print(weather_data['hourly'][0]["weather"][0]["id"])

if be_sunny:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
        body="It's not going to rain today. sunny outside enjoy the weather 😎🆒️",
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL NUMBER"
    )
    print(message.status)