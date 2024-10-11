import librosa
import soundfile as sf
import logging

def preprocess_audio(config):
    logging.info("Preprocessing audio...")
    # Load audio file
    y, sr = librosa.load(config['audio']['input_file'], sr=None)
    
    # Apply preprocessing steps
    if config['preprocess']['noise_reduction']:
        logging.info("Applying noise reduction...")
        y = librosa.effects.preemphasis(y)
    
    if config['preprocess']['normalize']:
        logging.info("Normalizing audio...")
        y = librosa.util.normalize(y)
    
    # Save preprocessed audio
    logging.info(f"Saving preprocessed audio to {config['preprocess']['output_file']}")
    sf.write(config['preprocess']['output_file'], y, sr)