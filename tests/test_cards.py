import pytest

from blackjack_unleashed.cards import Card, parse_deck
from blackjack_unleashed.errors import InvalidCardError, InvalidDeckError


def test_card_from_json_scores_and_displays_card() -> None:
    card = Card.from_json({"suit": "SPADES", "value": "7"})

    assert card.score_value == 7
    assert card.display == "S7"


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        ({"suit": "STARS", "value": "7"}, "Invalid card suit"),
        ({"suit": "SPADES", "value": "1"}, "Invalid card value"),
        ("not-a-card", "Card must be a JSON object"),
    ],
)
def test_card_from_json_rejects_invalid_cards(payload: object, message: str) -> None:
    with pytest.raises(InvalidCardError, match=message):
        Card.from_json(payload)


def test_parse_deck_rejects_non_list_payload() -> None:
    with pytest.raises(InvalidDeckError, match="JSON list"):
        parse_deck({"suit": "HEARTS", "value": "5"})


def test_parse_deck_wraps_invalid_card_errors() -> None:
    with pytest.raises(InvalidDeckError, match="Invalid card value"):
        parse_deck([{"suit": "HEARTS", "value": "11"}])
