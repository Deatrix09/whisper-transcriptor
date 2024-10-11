import whisper
import torch
import logging
from pydub import AudioSegment
import os
from .diarize import diarize_audio
from .translate import translate_text
from .preprocess import preprocess_audio

def transcribe_audio(audio_file, config):
    model = whisper.load_model(config['model']['name'])
    result = model.transcribe(
        audio_file,
        language=config['model']['language'],
        temperature=config['whisper']['temperature'],
        compression_ratio_threshold=config['whisper']['compression_ratio_threshold'],
        logprob_threshold=config['whisper']['logprob_threshold'],
        no_speech_threshold=config['whisper']['no_speech_threshold'],
        fp16=config['whisper']['fp16'] if torch.cuda.is_available() else False
    )
    return result['text']

def process_audio_in_segments(config):
    if config['preprocess']['enabled']:
        logging.info("Preprocessing audio...")
        preprocess_audio(config)
        audio_file = config['preprocess']['output_file']
    else:
        audio_file = config['audio']['input_file']

    logging.info(f"Loading audio file: {audio_file}")
    audio = AudioSegment.from_wav(audio_file)
    segment_length = config['audio']['chunk_size'] * 1000  # Convert to milliseconds

    segments = []
    for start in range(0, len(audio), segment_length):
        end = start + segment_length
        segment = audio[start:end]
        segment_file = f"temp_segment_{start}.wav"
        segment.export(segment_file, format="wav")

        logging.info(f"Processing segment: {start/1000}s to {end/1000}s")
        transcript = transcribe_audio(segment_file, config)
        diarization = diarize_audio(segment_file, config) if config['diarization']['enabled'] else None
        translation = translate_text(transcript, config) if config['translation']['enabled'] else None

        segments.append({
            'start': start / 1000,  # Convert to seconds
            'end': end / 1000,
            'transcript': transcript,
            'translation': translation,
            'diarization': diarization
        })

        os.remove(segment_file)

    return segments