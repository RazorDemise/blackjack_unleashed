import pytest

from blackjack_unleashed.cards import Card
from blackjack_unleashed.errors import DeckExhaustedError
from blackjack_unleashed.game import play_round


def card(value: str, suit: str = "SPADES") -> Card:
    return Card(suit=suit, value=value)


def test_dealer_wins_when_both_players_have_initial_blackjack() -> None:
    result = play_round(
        [
            card("A", "HEARTS"),
            card("10", "SPADES"),
            card("A", "DIAMONDS"),
            card("K", "CLUBS"),
        ],
        player_name="David",
    )

    assert result.winner == "Dealer"
    assert result.player.is_blackjack
    assert result.dealer.is_blackjack


def test_player_wins_with_initial_blackjack_when_dealer_does_not() -> None:
    result = play_round(
        [
            card("A", "HEARTS"),
            card("10", "SPADES"),
            card("9", "DIAMONDS"),
            card("8", "CLUBS"),
        ],
        player_name="David",
    )

    assert result.winner == "David"


def test_dealer_wins_with_initial_blackjack_when_player_does_not() -> None:
    result = play_round(
        [
            card("9", "HEARTS"),
            card("8", "SPADES"),
            card("A", "DIAMONDS"),
            card("Q", "CLUBS"),
        ],
        player_name="David",
    )

    assert result.winner == "Dealer"


def test_player_draws_until_seventeen_or_higher_and_dealer_can_bust() -> None:
    result = play_round(
        [
            card("2", "DIAMONDS"),
            card("2", "HEARTS"),
            card("7", "SPADES"),
            card("10", "SPADES"),
            card("6", "CLUBS"),
            card("9", "HEARTS"),
            card("J", "CLUBS"),
        ],
        player_name="David",
    )

    assert result.winner == "David"
    assert result.player.score == 19
    assert result.player.display_cards == "D2,H2,C6,H9"
    assert result.dealer.score == 27
    assert result.dealer.display_cards == "S7,S10,CJ"
    assert result.format_output() == (
        "Winner: David\nDealer | 27 | S7,S10,CJ\nDavid | 19 | D2,H2,C6,H9"
    )


def test_player_busts_and_loses_before_dealer_draws() -> None:
    result = play_round(
        [
            card("10", "HEARTS"),
            card("6", "CLUBS"),
            card("5", "DIAMONDS"),
            card("8", "SPADES"),
            card("10", "CLUBS"),
        ],
        player_name="David",
    )

    assert result.winner == "Dealer"
    assert result.player.score == 26
    assert result.dealer.score == 13


def test_dealer_draws_until_higher_than_player() -> None:
    result = play_round(
        [
            card("10", "HEARTS"),
            card("7", "CLUBS"),
            card("9", "DIAMONDS"),
            card("7", "SPADES"),
            card("2", "CLUBS"),
        ],
        player_name="David",
    )

    assert result.winner == "Dealer"
    assert result.player.score == 17
    assert result.dealer.score == 18


def test_deck_exhaustion_is_reported() -> None:
    with pytest.raises(DeckExhaustedError, match="ran out"):
        play_round(
            [
                card("2", "HEARTS"),
                card("2", "CLUBS"),
                card("7", "DIAMONDS"),
                card("7", "SPADES"),
            ],
            player_name="David",
        )
