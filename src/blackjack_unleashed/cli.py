"""Command-line interface for the Blackjack game."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from typing import TextIO

from blackjack_unleashed.deck_client import DEFAULT_DECK_URL, fetch_deck
from blackjack_unleashed.errors import BlackjackError
from blackjack_unleashed.game import play_round

DEFAULT_PLAYER_NAME = "David"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="blackjack",
        description="Play one round of Blackjack with a deck from a shuffle URL.",
    )
    parser.add_argument(
        "deck_url",
        nargs="?",
        default=DEFAULT_DECK_URL,
        help=f"URL returning a JSON list of cards. Defaults to {DEFAULT_DECK_URL}",
    )
    parser.add_argument(
        "--player-name",
        default=DEFAULT_PLAYER_NAME,
        help=f"Name to use for the player. Defaults to {DEFAULT_PLAYER_NAME}",
    )
    return parser


def main(
    argv: Sequence[str] | None = None,
    stdout: TextIO = sys.stdout,
    stderr: TextIO = sys.stderr,
) -> int:
    args = build_parser().parse_args(argv)

    try:
        deck = fetch_deck(args.deck_url)
        result = play_round(deck, player_name=args.player_name)
    except BlackjackError as exc:
        print(f"Error: {exc}", file=stderr)
        return 1

    print(result.format_output(), file=stdout)
    return 0


def run() -> None:
    raise SystemExit(main())
