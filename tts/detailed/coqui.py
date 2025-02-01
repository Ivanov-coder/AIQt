from dataclasses import dataclass
from ..tts_handler import TTSHandler


@dataclass
class CoquiTTS(TTSHandler):
    r"""
    Generate wave and play it

    Just overrided method <`_generate`>

    See abstract base class <`TTSRegistor`> for details.

    Please read the docstring of TTSHandler for detailed.

    :param:
        device: "cuda" or "cpu"
        speaker: Speaker name, supports: TODO: figure out
        speaker_wav: If you want to use your own voice, you can use this parameter to specify the path of the wav file.
        split_sentences: Whether to split sentences, defaults to True, if False, the whole text will be read out without stopping.
    """

    from TTS.api import TTS
    from torch.cuda import is_available

    device: str = "cuda" if is_available() else "cpu"
    speaker: str = "Daisy Studious"
    speaker_wav: str = None  # See the doc of CoquiTTS
    spilt_sentences: bool = True

    def _generate(self):
        try:
            # self.device = "cuda" if self.is_available() else "cpu"
            model = self.TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2"
            ).to(self.device)

            # TODO: 这里的speaker也只做了其中一个的接口，后面看下能否开放选择，甚至是克隆自己的声音。
            model.tts_to_file(
                text=self.text,
                speaker=self.speaker,  # HERE
                speaker_wav=self.speaker_wav,
                language=self.lang,
                emotion=self.emotion,  # XXX: Actually the CoquiTTS don't support emotion now
                speed=self.speed,  # Don't Support too.
                file_path=self.output_path,
                split_sentences=self.spilt_sentences,
            )

        except Exception as e:
            raise e
