"""Application-specific exceptions."""


class BlackjackError(Exception):
    """Base exception for expected Blackjack application failures."""


class DeckFetchError(BlackjackError):
    """Raised when the deck URL cannot be fetched or decoded."""


class InvalidCardError(BlackjackError):
    """Raised when card data does not match the expected schema."""


class InvalidDeckError(BlackjackError):
    """Raised when the deck payload is not a list of valid cards."""


class DeckExhaustedError(BlackjackError):
    """Raised when the game needs to draw from an empty deck."""
