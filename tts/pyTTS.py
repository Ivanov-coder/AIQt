import pyttsx3
import wave
import pyaudio


class pyTTS:
    # 初始设定请做到settings.yaml文件中
    '''
    用于生成并播放音频
    '''

    def __init__(self,
                 *,
                 lang: str = "en",
                 rate: int = 150,
                 volume: float = 1.0,
                 output_path: str = "/audio.wav",
                 text=None) -> None:

        self.LANG = lang
        self.RATE = rate
        self.VOLUME = volume
        self.OUTPUT_PATH = output_path
        self.TEXT = text
        self.CHUNK = 1024

    def get(self) -> None:
        try:
            self._generate()
            # self._play()
        except Exception as e:
            raise e

    def _generate(self):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", self.RATE)
            engine.setProperty("volume", self.VOLUME)
            engine.say(self.TEXT)
            engine.save_to_file(self.TEXT, self.OUTPUT_PATH)
            engine.runAndWait()

        except Exception as e:
            raise e

    def _play(self) -> None:
        with wave.open(self.OUTPUT_PATH, "rb") as w:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(w.getsampwidth()),
                channels=w.getnchannels(),
                rate=w.getframerate(),
                output=True,
            )

            while (data := w.readframes(self.CHUNK)):
                stream.write(data)
                data = w.readframes(self.CHUNK)

            stream.stop_stream()
            stream.close()

            p.terminate()
