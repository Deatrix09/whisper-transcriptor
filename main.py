import yaml
import click
from src.transcribe import process_audio
from src.output_formatters import formatters
import os

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

@click.command()
@click.option('--config', default='config.yaml', help='Path to the configuration file')
@click.option('--format', default=None, help='Output format (txt, json, csv, xml)')
@click.option('--diarization', default=None, type=bool, help='Enable or disable diarization')
@click.option('--translation', default=None, type=bool, help='Enable or disable translation')
@click.option('--audio', default=None, help='Path to the input audio file')
def main(config, format, diarization, translation, audio):
    config = load_config(config)
    if format:
        config['audio']['output_format'] = format
    if diarization is not None:
        config['diarization']['enabled'] = diarization
    if translation is not None:
        config['translation']['enabled'] = translation
    if audio:
        config['audio']['input_file'] = audio
    
    print("Processing audio...")
    result = process_audio(config)
    
    output_format = config['audio']['output_format']
    if output_format not in formatters:
        print(f"Unsupported output format: {output_format}")
        return
    
    formatter = formatters[output_format]
    output = formatter(result)
    
    output_file = f"{config['audio']['output_file']}.{output_format}"
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"Output written to {output_file}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    main()