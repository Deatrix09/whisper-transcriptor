# Improved Audio Transcription Application

This application transcribes audio files, optionally performs speaker diarization, optionally translates the transcript, and outputs the results in various formats.

## Installation

1. Ensure you have Python 3.7+ installed.
2. Install the required packages:

```
pip install -r requirements.txt
```

3. Obtain a Hugging Face authentication token for the pyannote.audio library and replace "YOUR_HF_AUTH_TOKEN" in `src/transcribe.py` with your token.

## Usage

1. Place your audio file in the same directory as the script.
2. Modify the `config.yaml` file to suit your needs:
   - `audio.input_file`: Name of your input audio file
   - `audio.output_file`: Base name of the output file (without extension)
   - `audio.output_format`: Output format (txt, json, csv, xml)
   - `whisper.model`: Whisper model to use (tiny, base, small, medium, large)
   - `whisper.language`: Language of the audio (use "auto" for automatic detection)
   - `diarization.enabled`: Enable or disable speaker diarization
   - `diarization.num_speakers`: Expected number of speakers in the audio
   - `translation.enabled`: Enable or disable translation
   - `translation.target_language`: Target language for translation

3. Run the script:

```
python src/main.py
```

You can also specify options directly from the command line:

```
python src/main.py --format json --diarization True --translation False
```

4. The script will generate an output file with the transcription, and optionally translation and diarization information in the specified format.

## Output Formats

- `txt`: Human-readable text format with original transcript, translated transcript (if enabled), and speaker diarization (if enabled).
- `json`: JSON format containing all information in a structured manner.
- `csv`: CSV format focusing on the speaker diarization segments (only if diarization is enabled).
- `xml`: XML format containing all information in a structured manner.

## Customization

You can further customize the application by modifying the `config.yaml` file or extending the modules in the `src` directory to add more functionality.

## Limitations

- The accuracy of transcription, diarization, and translation may vary depending on the quality of the audio and the complexity of the conversation.
- For optimal performance, ensure the audio file is clear and has minimal background noise.

## Troubleshooting

If you encounter any issues, please check the following:
- Ensure all dependencies are correctly installed
- Verify that the audio file is in a supported format (WAV is recommended)
- Check that the `config.yaml` file is correctly formatted and contains valid values
- Make sure you have provided a valid Hugging Face authentication token for pyannote.audio

For any other issues, please open an issue on the GitHub repository.