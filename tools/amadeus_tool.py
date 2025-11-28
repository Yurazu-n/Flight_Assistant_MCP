import os
import requests
from dotenv import load_dotenv

load_dotenv()

AMADEUS_KEY = "phe88Th5Qu00fYAxo7XfQKMQKNWViDxC"
AMADEUS_SECRET = "SNb1qoG2tWzu6n4c"

def get_amadeus_token():
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"

    payload = {
        "grant_type": "client_credentials",
        "client_id": AMADEUS_KEY,
        "client_secret": AMADEUS_SECRET,
    }

    response = requests.post(url, data=payload)

    if response.status_code != 200:
        raise Exception(f"Error al obtener token: {response.text}")

    return response.json()["access_token"]


def search_flights(origin: str, destination: str, date: str, adults: int = 1, max_results: int = 5):
    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v2/shopping/flight-offers"

    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": date,
        "adults": adults,
        "max": max_results,
        "currencyCode": "EUR",
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Flight Search: {response.text}")

    return response.json()


def price_flight_offer(offer):
    """
    Valida y devuelve el precio final de una flight offer usando Flight Offers Price API.
    
    Parámetro:
    - offer: el objeto JSON EXACTO devuelto por Flight Offers Search.
    """

    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v1/shopping/flight-offers/pricing"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    body = {
        "data": {
            "type": "flight-offers-pricing",
            "flightOffers": [offer]
        }
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error al obtener precio: {response.text}")

    return response.json()


def search_flight_availability(origin: str, destination: str, date: str, adults: int = 1):
    token = get_amadeus_token()

    url = "https://test.api.amadeus.com/v1/shopping/availability/flight-availabilities"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # El formato requerido para availability
    body = {
        "originDestinations": [
            {
                "id": "1",
                "originLocationCode": origin,
                "destinationLocationCode": destination,
                "departureDateTime": {
                    "date": date
                }
            }
        ],
        "travelers": [
            {
                "id": "1",
                "travelerType": "ADULT"
            }
        ],
        "sources": ["GDS"]
    }

    response = requests.post(url, json=body, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error en Flight Availability: {response.text}")

    return response.json()


def availability_from_offer(offer):
    seg = offer["itineraries"][0]["segments"][0]

    origin = seg["departure"]["iataCode"]
    destination = seg["arrival"]["iataCode"]
    date, time = seg["departure"]["at"].split("T")

    return search_flight_availability(origin, destination, date, time)


if __name__ == "__main__":
    print("Probando búsqueda de vuelos con Amadeus API...\n")
    """
    results = search_flights("MAD", "PAR", "2025-12-20")
    first_offer = results["data"][0]
    price = price_flight_offer(first_offer)
    print(results)
    print("------------")
    print(price)"""

    """availability = search_flight_availability("MAD", "PAR", "2025-12-20", adults=1)

    print(availability)"""
    """
    # SELECCIONAR UNA OFFER CONCRETA
    results = search_flights("MAD", "PAR", "2025-12-20")
    first_offer = results["data"][0]   # primera oferta disponible

    print("✔ Primera Flight Offer obtenida:")
    print(first_offer)


    # USAR ESA OFFER PARA CONSULTAR DISPONIBILIDAD
    print("\n Consultando disponibilidad del vuelo...")

    availability = availability_from_offer(first_offer)

    print("\n Resultado de Availability Search:")
    print(availability)"""
