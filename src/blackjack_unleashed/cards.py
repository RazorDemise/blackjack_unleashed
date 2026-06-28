"""Card parsing, scoring, and display helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, ClassVar

from blackjack_unleashed.errors import InvalidCardError, InvalidDeckError


@dataclass(frozen=True, slots=True)
class Card:
    """A single Blackjack card."""

    suit: str
    value: str

    SUITS: ClassVar[dict[str, str]] = {
        "HEARTS": "H",
        "CLUBS": "C",
        "SPADES": "S",
        "DIAMONDS": "D",
    }
    VALUES: ClassVar[set[str]] = {
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "J",
        "Q",
        "K",
        "A",
    }

    @classmethod
    def from_json(cls, payload: Any) -> Card:
        if not isinstance(payload, dict):
            raise InvalidCardError("Card must be a JSON object.")

        suit = payload.get("suit")
        value = payload.get("value")
        if not isinstance(suit, str) or suit not in cls.SUITS:
            raise InvalidCardError(f"Invalid card suit: {suit!r}.")
        if not isinstance(value, str) or value not in cls.VALUES:
            raise InvalidCardError(f"Invalid card value: {value!r}.")

        return cls(suit=suit, value=value)

    @property
    def score_value(self) -> int:
        if self.value in {"J", "Q", "K"}:
            return 10
        if self.value == "A":
            return 11
        return int(self.value)

    @property
    def display(self) -> str:
        return f"{self.SUITS[self.suit]}{self.value}"


def parse_deck(payload: Any) -> list[Card]:
    if not isinstance(payload, list):
        raise InvalidDeckError("Deck response must be a JSON list.")

    try:
        return [Card.from_json(item) for item in payload]
    except InvalidCardError as exc:
        raise InvalidDeckError(str(exc)) from exc
