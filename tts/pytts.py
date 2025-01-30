from .tts_registor import TTSHandler


class PyTTS(TTSHandler):
    r"""
    Generate wave and play it

    Just overrided method <_generate>

    See abstract base class <TTSRegistor> for details.
    """

    from pyttsx3 import init

    def _generate(self):
        try:
            engine = self.init()
            engine.setProperty("rate", self.RATE)
            engine.setProperty("volume", self.VOLUME)
            engine.say(self.TEXT)
            engine.save_to_file(self.TEXT, self.OUTPUT_PATH)
            engine.runAndWait()

        except Exception as e:
            raise e
