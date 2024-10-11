import argparse
import yaml
import logging
from pathlib import Path
from src.transcribe import process_audio_in_segments
from src.output_formatters import formatters

CONFIG_PATH = Path(__file__).parent / "config.yaml"

def setup_logging(config):
    logging.basicConfig(
        level=getattr(logging, config['logging']['level']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=config['logging']['file'],
        filemode='a'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def main():
    parser = argparse.ArgumentParser(description="Whisper AI Audio Transcription")
    parser.add_argument("--audio", help="Path to the audio file for transcription")
    parser.add_argument("--model", choices=["tiny", "base", "small", "medium", "large"],
                        help="Model to use for transcription")
    parser.add_argument("--diarization", action="store_true", help="Enable speaker diarization")
    parser.add_argument("--formats", nargs="+", choices=["txt", "json", "csv", "xml", "srt"],
                        help="Output formats")
    parser.add_argument("--config", default=CONFIG_PATH, help="Path to the configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    setup_logging(config)

    if args.audio:
        config['audio']['input_file'] = args.audio
    if args.model:
        config['model']['name'] = args.model
    if args.diarization is not None:
        config['diarization']['enabled'] = args.diarization
    if args.formats:
        config['audio']['output_format'] = args.formats

    logging.info("Processing audio...")
    segments = process_audio_in_segments(config)
    
    for output_format in config['audio']['output_format']:
        if output_format not in formatters:
            logging.error(f"Unsupported output format: {output_format}")
            continue
        
        formatter = formatters[output_format]
        output = formatter(segments)
        
        output_file = f"{config['audio']['output_file']}.{output_format}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        
        logging.info(f"Output written to {output_file}")

if __name__ == "__main__":
    main()