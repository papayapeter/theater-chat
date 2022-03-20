import os


def clear() -> None:
    """
    clear the terminal.
    """

    os.system('cls' if os.name == 'nt' else 'clear')