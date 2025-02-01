import os
import wave
import pyaudio
from dataclasses import dataclass


@dataclass
class TTSHandler:
	r"""
	The base class for select TTS

	text (str): The text to be converted to audio

	output_path (str): The path to save the audio file

					The OUTPUT_PATH should be the formation like:

	`f"./audio/{folder_name}/{file_name}.wav"`

	lang (str): The language of the text, now supports TODO: later figure out what is supported

	rate (int): The rate of the text

	volume (float): The volume of the text, defaults to 1.0

	emotion (str): The emotion of the text	 XXX: Actually CoquiTTS doesn't support this

	speed (float): The speed of the text	 XXX: Actually CoquiTTS doesn't support this

	chunk (int): The chunk size of the audio file
	"""

	text: str
	output_path: str
	lang: str = "en"
	rate: int = 150
	volume: float = 1.0
	emotion: str = "Neutral"  # XXX: Probably useless
	speed: float = 1.0  # XXX: Probably useless
	chunk: int = 1024

	def __post_init__(self):
		if not self.text:
			# Avoiding llm error condition, without any answers generated
			self.text = "Sorry, Failed to get the answer from LLM."

	def get(self) -> None:
		r"""
		API for generating and playing the audio.
		"""
		try:
			self._create_folders()  # Used to create folder for wave files
			self._generate()  # Generate the wave files
			self._play()  # Play the wave files
		except Exception as e:
			raise e

	def _play(self) -> None:
		r"""
		Play the audio file.
		"""
		with wave.open(self.output_path, "rb") as w:
			p = pyaudio.PyAudio()
			stream = p.open(
				format=p.get_format_from_width(w.getsampwidth()),
				channels=w.getnchannels(),
				rate=w.getframerate(),
				output=True,
			)
			while len(data := w.readframes(self.chunk)):
				stream.write(data)
			stream.close()
			p.terminate()

	def _create_folders(self):
		r"""
		Create folders for wave files.

		The folder will be created in ./audio

		Just ensure that the wave files will be correctly put in their folder.

		The OUTPUT_PATH should be the formation like:

		`f"./audio/{folder_name}/{file_name}.wav"`
		"""
		# folder_path will be the formation like: `f"./audio/{folder_name}"` if correctly given arg.
		folder_path = os.path.dirname(self.output_path)

		# So here when we split by "/", it'll be a list with 3 elements
		assert len(folder_path.split("/")) == 3, ValueError(
			'The OUTPUT_PATH should be the formation like: `f"./audio/{folder_name}/{file_name}.wav"`'
		)
		# BUG: Hope it works...

		if not os.path.exists(folder_path):
			# create folders
			os.makedirs(folder_path)

	def _generate(self):
		r"""
		Generate waves and save to files.
		"""
		raise NotImplementedError(
			f"Subclass <{self.__class__.__name__}> must override the method <_generate>"
		)
