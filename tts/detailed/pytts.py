from ..tts_handler import TTSHandler


class PyTTS(TTSHandler):
    r"""
    Generate wave and play it

    Just overrided method <`_generate`>

    See abstract base class <`TTSRegistor`> for details.
    """

    import pyttsx3

    def _generate(self):
        try:
            engine = self.pyttsx3.init()
            engine.setProperty("rate", self.rate)
            engine.setProperty("volume", self.volume)
            engine.save_to_file(
                self.text, self.output_path
            )  # BUG: self.OUTPUT_PATH may need to be changed
            engine.runAndWait()

        except Exception as e:
            raise e
