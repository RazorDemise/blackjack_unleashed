from io import StringIO

import pytest

from blackjack_unleashed.cards import Card
from blackjack_unleashed.cli import DEFAULT_PLAYER_NAME, main
from blackjack_unleashed.errors import DeckFetchError


def card(value: str, suit: str = "SPADES") -> Card:
    return Card(suit=suit, value=value)


def test_main_prints_game_output_with_default_player_name(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fake_fetch_deck(url: str) -> list[Card]:
        assert url == "https://example.test/deck"
        return [
            card("10", "HEARTS"),
            card("7", "CLUBS"),
            card("9", "DIAMONDS"),
            card("7", "SPADES"),
            card("2", "CLUBS"),
        ]

    stdout = StringIO()
    stderr = StringIO()
    monkeypatch.setattr("blackjack_unleashed.cli.fetch_deck", fake_fetch_deck)

    exit_code = main(["https://example.test/deck"], stdout=stdout, stderr=stderr)

    assert exit_code == 0
    assert stderr.getvalue() == ""
    assert stdout.getvalue() == (
        f"Winner: Dealer\nDealer | 18 | D9,S7,C2\n{DEFAULT_PLAYER_NAME} | 17 | H10,C7\n"
    )


def test_main_uses_custom_player_name(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch_deck(url: str) -> list[Card]:
        assert url == "https://example.test/deck"
        return [
            card("A", "HEARTS"),
            card("10", "CLUBS"),
            card("9", "DIAMONDS"),
            card("8", "SPADES"),
        ]

    stdout = StringIO()
    stderr = StringIO()
    monkeypatch.setattr("blackjack_unleashed.cli.fetch_deck", fake_fetch_deck)

    exit_code = main(
        ["https://example.test/deck", "--player-name", "Alice"],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == 0
    assert "Winner: Alice" in stdout.getvalue()
    assert "Alice | 21 | HA,C10" in stdout.getvalue()
    assert stderr.getvalue() == ""


def test_main_prints_clear_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_fetch_deck(url: str) -> list[Card]:
        raise DeckFetchError(f"Could not fetch deck from {url}")

    stdout = StringIO()
    stderr = StringIO()
    monkeypatch.setattr("blackjack_unleashed.cli.fetch_deck", fake_fetch_deck)

    exit_code = main(["https://example.test/deck"], stdout=stdout, stderr=stderr)

    assert exit_code == 1
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == (
        "Error: Could not fetch deck from https://example.test/deck\n"
    )
