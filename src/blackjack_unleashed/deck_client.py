"""Fetch and parse decks from the shuffle endpoint."""

from __future__ import annotations

from typing import Any

import requests

from blackjack_unleashed.cards import Card, parse_deck
from blackjack_unleashed.errors import DeckFetchError, InvalidDeckError

DEFAULT_DECK_URL = "https://sandbox.getunleash.io/blackjack/shuffle"
REQUEST_TIMEOUT_SECONDS = 10


def fetch_deck(url: str) -> list[Card]:
    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        payload: Any = response.json()
    except requests.RequestException as exc:
        raise DeckFetchError(f"Could not fetch deck from {url}: {exc}") from exc
    except ValueError as exc:
        raise DeckFetchError(f"Deck response from {url} was not valid JSON.") from exc

    try:
        return parse_deck(payload)
    except InvalidDeckError as exc:
        raise DeckFetchError(f"Deck response from {url} was invalid: {exc}") from exc
