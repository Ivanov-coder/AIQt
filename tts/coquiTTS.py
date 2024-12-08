import os
import wave
import pyaudio
from TTS.api import TTS
from torch.cuda import is_available


class coquiTTS:
    # 初始设定请做到settings.yaml文件中
    """
    用于生成并播放音频
    """

    def __init__(
        self,
        *,
        lang: str = "en",   # TODO: 查下官网看下支持什么
        device: str = "cuda" if is_available() else "cpu",
        output_path: str = "./audio.wav",
        text=None,
    ) -> None:

        self.LANG = lang
        self.DEVICE = device
        self.OUTPUT_PATH = output_path
        self.TEXT = text
        self.CHUNK = 1024

    def _generate(self):
        try:
            # TODO: 这里只做了一个模型的接口，后面看下其他模型是否可用
            model = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2").to(self.DEVICE)
            # TODO: 这里的speaker也只做了其中一个的接口，后面看下能否开放选择，甚至是克隆自己的声音。
            model.tts_to_file(
                text=self.TEXT,
                language=self.LANG,
                speaker="Daisy Studious", # TODO 开放API
                file_path=self.OUTPUT_PATH,
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

            while data := w.readframes(self.CHUNK):
                stream.write(data)
                data = w.readframes(self.CHUNK)

            stream.stop_stream()
            stream.close()

            p.terminate()

    def get(self) -> None:
        try:
            self._generate()
            self._play()
        except Exception as e:
            raise e


# available voices:
# [
#     "Claribel Dervla",
#     "Daisy Studious",
#     "Gracie Wise",
#     "Tammie Ema",
#     "Alison Dietlinde",
#     "Ana Florence",
#     "Annmarie Nele",
#     "Asya Anara",
#     "Brenda Stern",
#     "Gitta Nikolina",
#     "Henriette Usha",
#     "Sofia Hellen",
#     "Tammy Grit",
#     "Tanja Adelina",
#     "Vjollca Johnnie",
#     "Andrew Chipper",
#     "Badr Odhiambo",
#     "Dionisio Schuyler",
#     "Royston Min",
#     "Viktor Eka",
#     "Abrahan Mack",
#     "Adde Michal",
#     "Baldur Sanjin",
#     "Craig Gutsy",
#     "Damien Black",
#     "Gilberto Mathias",
#     "Ilkin Urbano",
#     "Kazuhiko Atallah",
#     "Ludvig Milivoj",
#     "Suad Qasim",
#     "Torcull Diarmuid",
#     "Viktor Menelaos",
#     "Zacharie Aimilios",
#     "Nova Hogarth",
#     "Maja Ruoho",
#     "Uta Obando",
#     "Lidiya Szekeres",
#     "Chandra MacFarland",
#     "Szofi Granger",
#     "Camilla Holmström",
#     "Lilya Stainthorpe",
#     "Zofija Kendrick",
#     "Narelle Moon",
#     "Barbora MacLean",
#     "Alexandra Hisakawa",
#     "Alma María",
#     "Rosemary Okafor",
#     "Ige Behringer",
#     "Filip Traverse",
#     "Damjan Chapman",
#     "Wulf Carlevaro",
#     "Aaron Dreschner",
#     "Kumar Dahl",
#     "Eugenio Mataracı",
#     "Ferran Simen",
#     "Xavier Hayasaka",
#     "Luis Moray",
#     "Marcos Rudaski",
# ]
