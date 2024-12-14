from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

model_dir = "./iic/SenseVoiceSmall"

model = AutoModel(
    model = model_dir,
    vad_model = "fsmn-vad",
    vad_kwargs = {"max_single_segment_time": 30000},
    device = "cuda"
)

res = model.generate(
    input = f"./a0405.wav",
    cache = {},
    language = "auto",
    use_itn = True,
    batch_size_s =  60,
    merge_vad = True,
    merge_length_s = 15,
)

text = rich_transcription_postprocess(res[0]["text"])

print(text)