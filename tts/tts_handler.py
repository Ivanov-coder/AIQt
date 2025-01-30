import wave
import pyaudio


class TTSHandler:
    r"""
    The base class for select TTS
    """

    def __init__(
        self,
        text: str,
        *,
        output_path: str,
        lang: str = "en",
        rate: int = 150,
        volume: float = 1.0,
        emotion: str = "Neural",
        speed: float = 1.0,
        chunk: int = 1024,
    ) -> None:
        # XXX: Those Parameters may won't all used in the Subclasses
        self.TEXT = text
        self.LANG = lang
        self.OUTPUT_PATH = output_path
        self.RATE = rate
        self.VOLUME = volume
        self.EMOTION = emotion
        self.SPEED = speed
        self.CHUCK = chunk

    def get(self) -> None:
        try:
            self._generate()
            self._play()
        except Exception as e:
            raise e

    def _generate(self):
        raise NotImplementedError(
            f"Subclass <{self.__class__.__name__}> must override the method <_generate>"
        )

    def _play(self) -> None:
        with wave.open(self.OUTPUT_PATH, "rb") as w:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(w.getsampwidth()),
                channels=w.getnchannels(),
                rate=w.getframerate(),
                output=True,
            )
            while len(data := w.readframes(self.CHUNK)):
                stream.write(data)
            stream.close()
            p.terminate()
