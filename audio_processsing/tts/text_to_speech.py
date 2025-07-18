import torch
from TTS.api import TTS
from TTS.tts.configs.xtts_config import XttsConfig, XttsAudioConfig
from TTS.config.shared_configs import BaseDatasetConfig
from TTS.tts.models.xtts import XttsArgs
import os

# It's recommended to add these to the safe globals for model loading
torch.serialization.add_safe_globals(
    [XttsConfig, XttsAudioConfig, BaseDatasetConfig, XttsArgs]
)


class TextToSpeechGenerator:
    """
    A class to handle Text-to-Speech generation using Coqui TTS.
    """

    def __init__(
        self,
        speaker_wav_path: str,
        model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    ):
        """
        Initializes the TTS model.

        Args:
            speaker_wav_path (str): Path to the reference audio file for the speaker's voice.
            model_name (str): The name of the TTS model to use.
        """
        self.speaker_wav_path = speaker_wav_path
        self.language = "pt"  # Default language

        if not os.path.exists(self.speaker_wav_path):
            raise FileNotFoundError(
                f"Speaker reference file not found at: {self.speaker_wav_path}"
            )

        # Determine the device to use
        self.use_gpu = torch.cuda.is_available()
        self.device = "cuda" if self.use_gpu else "cpu"
        print(f"Using device: {self.device}")

        try:
            print("Initializing TTS model...")
            self.tts = TTS(
                model_name=model_name,
                progress_bar=True,
                gpu=self.use_gpu,
            )
            print("TTS model initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize TTS model: {e}")
            raise

    def synthesize(self, text: str, output_path: str):
        """
        Synthesizes audio from the given text and saves it to a file.

        Args:
            text (str): The text to be converted to speech.
            output_path (str): The path to save the generated audio file.
        """
        try:
            print(f"\nGenerating speech for text: '{text[:30]}...'")
            self.tts.tts_to_file(
                text=text,
                speaker_wav=self.speaker_wav_path,
                language=self.language,
                file_path=output_path,
            )
            print(f"Audio successfully saved to '{output_path}'")
        except Exception as e:
            print(f"An error occurred during TTS synthesis: {e}")


# Example of how to use the class
if __name__ == "__main__":
    # --- Configuration ---
    SPEAKER_WAV = "/Users/theocoelho/Documents/academico/faculdade/TCC/tcc_project/audios/554199941200/20250714/e6b9aef5-81d9-40c7-99e8-d8c1604cf33a.ogg"
    TEXT_TO_SYNTHESIZE = "Olá! Este áudio soa bem natural, em português do Brasil."
    OUTPUT_FILENAME = "saida.wav"
    # ---------------------

    try:
        # 1. Initialize the generator (this loads the model)
        tts_generator = TextToSpeechGenerator(speaker_wav_path=SPEAKER_WAV)

        # 2. Synthesize audio from text
        tts_generator.synthesize(text=TEXT_TO_SYNTHESIZE, output_path=OUTPUT_FILENAME)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print(
            "Please update the 'SPEAKER_WAV' variable with the correct path to your audio file."
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
