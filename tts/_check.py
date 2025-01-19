from utils import typing


def check_if_need_tts(which: str = "coqui") -> typing.Optional[typing.Callable]:
    r"""
    :param: which: str -> select one of the TTS engine, default to be "coqui"
    """
    if which == "coqui":
        from ._coquiTTS import coquiTTS

        return coquiTTS

    elif which == "pytts":
        from ._pyTTS import pyTTS

        return pyTTS
    else:
        raise ValueError("The parameter `which` must be 'coqui' or 'pyTTS'")
