from utils import os
import wave
import pyaudio
from TTS.api import TTS
from torch.cuda import is_available

# FIXME: 对于单个模型的多个wav文件 需要开个文件夹 不然太乱了


class coquiTTS:
    r"""
    Generate wave and play it
    """

    def __init__(
        self,
        *,
        lang: str,  # WARN: Supported languages are ['en', 'es', 'fr', 'de', 'it', 'pt', 'pl', 'tr', 'ru', 'nl', 'cs', 'ar', 'zh-cn', 'hu', 'ko', 'ja', 'hi']
        device: str = (
            "cuda" if is_available() else "cpu"
        ),  # FIXME: 草 这里也有大问题 如果只下载torch，包是"cpu"的，但是cpu太慢了 需要想想怎么样在requirements.txt里面插入cuda版本
        output_path: str = "./audio/audio.wav",
        text: str = None,
        emotion: str = "Neutral",
        speed: float = 1,
    ) -> None:

        self.LANG = lang
        self.DEVICE = device
        self.OUTPUT_PATH = output_path
        self.TEXT = text
        self.EMOTION = emotion
        self.SPEED = speed
        self.CHUNK = 1024
        # TODO: Open the API of it when doing Qt:
        self.AVAILABLE_VOICES = (
            "Claribel Dervla",
            "Daisy Studious",
            "Gracie Wise",
            "Tammie Ema",
            "Alison Dietlinde",
            "Ana Florence",
            "Annmarie Nele",
            "Asya Anara",
            "Brenda Stern",
            "Gitta Nikolina",
            "Henriette Usha",
            "Sofia Hellen",
            "Tammy Grit",
            "Tanja Adelina",
            "Vjollca Johnnie",
            "Andrew Chipper",
            "Badr Odhiambo",
            "Dionisio Schuyler",
            "Royston Min",
            "Viktor Eka",
            "Abrahan Mack",
            "Adde Michal",
            "Baldur Sanjin",
            "Craig Gutsy",
            "Damien Black",
            "Gilberto Mathias",
            "Ilkin Urbano",
            "Kazuhiko Atallah",
            "Ludvig Milivoj",
            "Suad Qasim",
            "Torcull Diarmuid",
            "Viktor Menelaos",
            "Zacharie Aimilios",
            "Nova Hogarth",
            "Maja Ruoho",
            "Uta Obando",
            "Lidiya Szekeres",
            "Chandra MacFarland",
            "Szofi Granger",
            "Camilla Holmström",
            "Lilya Stainthorpe",
            "Zofija Kendrick",
            "Narelle Moon",
            "Barbora MacLean",
            "Alexandra Hisakawa",
            "Alma María",
            "Rosemary Okafor",
            "Ige Behringer",
            "Filip Traverse",
            "Damjan Chapman",
            "Wulf Carlevaro",
            "Aaron Dreschner",
            "Kumar Dahl",
            "Eugenio Mataracı",
            "Ferran Simen",
            "Xavier Hayasaka",
            "Luis Moray",
            "Marcos Rudaski",
        )

    def _generate(self):
        try:
            model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(
                self.DEVICE
            )
            # TODO: 这里的speaker也只做了其中一个的接口，后面看下能否开放选择，甚至是克隆自己的声音。
            model.tts_to_file(
                text=self.TEXT,
                language=self.LANG,
                speaker="Daisy Studious",  # TODO 开放API
                file_path=self.OUTPUT_PATH,
                emotion=self.EMOTION,
                speed=self.SPEED,
            )
        except Exception as e:
            raise e

    def _play(self) -> None:
        while True:
            if os.path.exists(self.OUTPUT_PATH):
                break

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

    def get(self) -> None:
        try:
            self._generate()
            self._play()
        except Exception as e:
            raise e
