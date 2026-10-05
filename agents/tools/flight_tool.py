import os
import requests
from dotenv import load_dotenv

load_dotenv()

AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "CMB")

def get_flights_from_origin(origin_iata: str):
    url = "http://api.aviationstack.com/v1/flights"

    params = {
        "access_key": AVIATIONSTACK_API_KEY,
        "dep_iata": origin_iata,
        "limit": 5,
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()

def format_flights(data):
    results = []

    for flight in data.get("data", []):
        airline = flight.get("airline", {}).get("name", "Unknown")
        flight_number = flight.get("flight", {}).get("iata", "N/A")
        status = flight.get("flight_status", "Unknown")

        departure = flight.get("departure", {})
        arrival = flight.get("arrival", {})

        results.append(
            f"""
Airline: {airline}
Flight: {flight_number}
Status: {status}

Departure:
- Airport: {departure.get('airport', 'N/A')}
- IATA: {departure.get('iata', 'N/A')}
- Terminal: {departure.get('terminal', 'N/A')}
- Gate: {departure.get('gate', 'N/A')}
- Scheduled: {departure.get('scheduled', 'N/A')}

Arrival:
- Airport: {arrival.get('airport', 'N/A')}
- IATA: {arrival.get('iata', 'N/A')}
- Terminal: {arrival.get('terminal', 'N/A')}
- Gate: {arrival.get('gate', 'N/A')}
- Scheduled: {arrival.get('scheduled', 'N/A')}
"""
        )

    return "\n---\n".join(results)

def search_flights(origin_iata: str = None) -> str:
    origin = origin_iata or DEFAULT_ORIGIN_IATA

    data = get_flights_from_origin(origin)

    return format_flights(data)