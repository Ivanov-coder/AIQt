from .detailed.pytts import PyTTS
from .detailed.coqui import CoquiTTS

__all__ = ["get_tts_socket"]


def get_tts_socket(choice: str):
    r"""
    Get the socket of TTS

    :param:
        choice: "pytts" or "coqui" # XXX: till now, later we will add more.
    """
    # If possible, optimize the code, without using if...else...
    if choice == "pytts":
        return PyTTS
    elif choice == "coqui":
        return CoquiTTS
    else:
        raise ValueError("Invalid TTS choice")
