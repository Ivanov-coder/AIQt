from .tts_registor import TTSHandler


class CoquiTTS(TTSHandler):
    r"""
    Generate wave and play it

    Just overrided method <_generate>

    See abstract base class <TTSRegistor> for details.
    """

    from TTS.api import TTS
    from torch.cuda import is_available

    def __init__(
        self,
        device: str = "cuda" if is_available() else "cpu",
        speaker: str = "Daisy Studious",
        speaker_wav: str = None,  # See the doc of CoquiTTS
        spilt_sentences: bool = True,
    ) -> None:
        super().__init__()
        self.DEVICE = device
        self.SPLIT_SENTENCES = spilt_sentences
        self.SPEAKER_WAV = (
            speaker_wav  # XXX: If here can exist both? Speaker and Speaker_wav
        )
        self.SPEAKER = speaker

    def _generate(self):
        try:
            model = self.TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2"
            ).to(self.DEVICE)

            # TODO: 这里的speaker也只做了其中一个的接口，后面看下能否开放选择，甚至是克隆自己的声音。
            model.tts_to_file(
                text=self.TEXT,
                speaker=self.SPEAKER,  # HERE
                speaker_wav=self.SPEAKER_WAV,
                language=self.LANG,
                emotion=self.EMOTION,  # TODO: If the emotion is mutable? Various Emotions may be popular
                speed=self.SPEED,
                file_path=self.OUTPUT_PATH,
                split_sentences=self.SPLIT_SENTENCES,
            )

        except Exception as e:
            raise e
