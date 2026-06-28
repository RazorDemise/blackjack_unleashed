from typing import Any

import pytest
import requests

from blackjack_unleashed.deck_client import REQUEST_TIMEOUT_SECONDS, fetch_deck
from blackjack_unleashed.errors import DeckFetchError


class FakeResponse:
    def __init__(
        self,
        payload: Any = None,
        json_error: ValueError | None = None,
        http_error: requests.HTTPError | None = None,
    ) -> None:
        self._payload = payload
        self._json_error = json_error
        self._http_error = http_error

    def raise_for_status(self) -> None:
        if self._http_error is not None:
            raise self._http_error

    def json(self) -> Any:
        if self._json_error is not None:
            raise self._json_error
        return self._payload


def test_fetch_deck_returns_parsed_cards(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        assert url == "https://example.test/deck"
        assert timeout == REQUEST_TIMEOUT_SECONDS
        return FakeResponse([{"suit": "HEARTS", "value": "5"}])

    monkeypatch.setattr("blackjack_unleashed.deck_client.requests.get", fake_get)

    deck = fetch_deck("https://example.test/deck")

    assert deck[0].display == "H5"


def test_fetch_deck_wraps_network_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        raise requests.Timeout(f"{url} timed out after {timeout} seconds")

    monkeypatch.setattr("blackjack_unleashed.deck_client.requests.get", fake_get)

    with pytest.raises(DeckFetchError, match="Could not fetch deck"):
        fetch_deck("https://example.test/deck")


def test_fetch_deck_wraps_http_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        return FakeResponse(http_error=requests.HTTPError(f"{url} returned 500"))

    monkeypatch.setattr("blackjack_unleashed.deck_client.requests.get", fake_get)

    with pytest.raises(DeckFetchError, match="Could not fetch deck"):
        fetch_deck("https://example.test/deck")


def test_fetch_deck_wraps_invalid_json(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        return FakeResponse(json_error=ValueError(f"{url} was not JSON"))

    monkeypatch.setattr("blackjack_unleashed.deck_client.requests.get", fake_get)

    with pytest.raises(DeckFetchError, match="not valid JSON"):
        fetch_deck("https://example.test/deck")


def test_fetch_deck_wraps_invalid_deck_payload(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_get(url: str, timeout: int) -> FakeResponse:
        return FakeResponse({"suit": "HEARTS", "value": "5"})

    monkeypatch.setattr("blackjack_unleashed.deck_client.requests.get", fake_get)

    with pytest.raises(DeckFetchError, match="Deck response .* was invalid"):
        fetch_deck("https://example.test/deck")
