import tempfile
from pydub import AudioSegment


class AudioConverter:
    @staticmethod
    def to_wav(input_path: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
            sound = AudioSegment.from_ogg(input_path)
            sound.export(tmp_wav.name, format="wav")
            return tmp_wav.name
