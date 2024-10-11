# Improved Audio Transcription Application

This application transcribes audio files, optionally performs speaker diarization, optionally translates the transcript, and outputs the results in various formats.

## Features

- Audio transcription using OpenAI's Whisper model
- Optional speaker diarization using pyannote.audio
- Optional translation of transcripts
- Multiple output formats: TXT, JSON, CSV, XML
- Audio preprocessing options
- Configurable via YAML file and command-line arguments

## Installation

1. Ensure you have Python 3.7+ installed.
2. Clone this repository:
   ```
   git clone https://github.com/yourusername/audio-transcription-app.git
   cd audio-transcription-app
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Obtain a Hugging Face authentication token for the pyannote.audio library and update the `config.yaml` file with your token.

## Configuration

The application uses a `config.yaml` file for its settings. You can modify this file to change various aspects of the transcription process. Here are some key settings:

- `model.name`: Whisper model to use (tiny, base, small, medium, large)
- `model.language`: Language of the audio (use "auto" for automatic detection)
- `audio.chunk_size`: Size of audio chunks for processing (in seconds)
- `diarization.enabled`: Enable or disable speaker diarization
- `translation.enabled`: Enable or disable translation
- `preprocess.enabled`: Enable or disable audio preprocessing

## Usage

1. Place your audio file in the project directory.
2. Run the script:
   ```
   python main.py --audio your_audio_file.wav --formats txt json
   ```

### Command-line Options

- `--audio`: Path to the audio file for transcription
- `--model`: Model to use for transcription (tiny, base, small, medium, large)
- `--diarization`: Enable speaker diarization
- `--formats`: Output formats (txt, json, csv, xml)
- `--config`: Path to the configuration file (default: config.yaml)

## Output Formats

- `txt`: Human-readable text format with timestamps, transcripts, and speaker information
- `json`: Structured JSON format containing all information
- `csv`: CSV format focusing on speaker diarization segments
- `xml`: XML format containing all information in a structured manner

## Project Structure

- `main.py`: Entry point of the application
- `config.yaml`: Configuration file
- `src/`:
  - `transcribe.py`: Main transcription logic
  - `diarize.py`: Speaker diarization functionality
  - `translate.py`: Translation functionality
  - `preprocess.py`: Audio preprocessing
  - `output_formatters.py`: Output formatting functions

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.