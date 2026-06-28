"""Blackjack round rules."""

from __future__ import annotations

from dataclasses import dataclass

from blackjack_unleashed.cards import Card
from blackjack_unleashed.errors import DeckExhaustedError

DEALER_NAME = "Dealer"


@dataclass(frozen=True, slots=True)
class Hand:
    name: str
    cards: tuple[Card, ...]

    @property
    def score(self) -> int:
        return sum(card.score_value for card in self.cards)

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.score == 21

    @property
    def is_bust(self) -> bool:
        return self.score > 21

    @property
    def display_cards(self) -> str:
        return ",".join(card.display for card in self.cards)

    def with_card(self, card: Card) -> Hand:
        return Hand(name=self.name, cards=(*self.cards, card))


@dataclass(frozen=True, slots=True)
class GameResult:
    winner: str
    dealer: Hand
    player: Hand

    def format_output(self) -> str:
        return "\n".join(
            (
                f"Winner: {self.winner}",
                format_hand(self.dealer),
                format_hand(self.player),
            )
        )


class Deck:
    def __init__(self, cards: list[Card]) -> None:
        self._cards = cards
        self._position = 0

    def draw(self) -> Card:
        if self._position >= len(self._cards):
            raise DeckExhaustedError("Deck ran out of cards during the game.")

        card = self._cards[self._position]
        self._position += 1
        return card


def play_round(cards: list[Card], player_name: str) -> GameResult:
    deck = Deck(cards)
    player = Hand(name=player_name, cards=(deck.draw(), deck.draw()))
    dealer = Hand(name=DEALER_NAME, cards=(deck.draw(), deck.draw()))

    if dealer.is_blackjack:
        return GameResult(winner=dealer.name, dealer=dealer, player=player)
    if player.is_blackjack:
        return GameResult(winner=player.name, dealer=dealer, player=player)

    while player.score < 17:
        player = player.with_card(deck.draw())

    if player.is_bust:
        return GameResult(winner=dealer.name, dealer=dealer, player=player)

    while dealer.score <= player.score:
        dealer = dealer.with_card(deck.draw())

    winner = player.name if dealer.is_bust else dealer.name
    return GameResult(winner=winner, dealer=dealer, player=player)


def format_hand(hand: Hand) -> str:
    return f"{hand.name} | {hand.score} | {hand.display_cards}"
