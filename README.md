# Blackjack Unleashed

A command-line Blackjack game built for the Unleash technical assessment.

It fetches a shuffled deck, plays one round against the dealer, and prints the
winner plus both hands.

## Requirements

- Python 3.11 or newer
- [Poetry](https://python-poetry.org/docs/#installation)

## Quick Start

Install dependencies and run the checks:

```bash
poetry install
poetry run pytest
poetry run ruff check .
```

Run the app with the default shuffle URL and player name `David`:

```bash
poetry run blackjack
```

Run with a custom deck URL:

```bash
poetry run blackjack https://example.com/deck.json
```

Run with a custom player name:

```bash
poetry run blackjack https://example.com/deck.json --player-name Alice
```

Expected output format:

```text
Winner: David
Dealer | 27 | S7,S10,CJ
David | 19 | D2,H2,C6,H9
```

## Formatting

```bash
poetry run ruff format .
```

## Licence

This repository is proprietary. See [LICENSE](LICENSE).
