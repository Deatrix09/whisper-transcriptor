import whisper
import torch
import logging
from .diarize import diarize_audio
from .translate import translate_text
from .preprocess import preprocess_audio

def detect_language(audio_file, model):
    try:
        audio = whisper.load_audio(audio_file)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)
        logging.info(f"Detected language: {detected_lang}")
        return detected_lang
    except Exception as e:
        logging.error(f"Language detection failed: {str(e)}")
        return 'en'  # Default to English

def transcribe_audio(audio_file, config):
    model = whisper.load_model(config['model']['name'])
    language = config['model']['language']
    
    if language == 'auto':
        language = detect_language(audio_file, model)
    
    logging.info(f"Transcribing with language: {language}")

    try:
        result = model.transcribe(
            audio_file,
            language=language,
            temperature=config['whisper']['temperature'],
            compression_ratio_threshold=config['whisper']['compression_ratio_threshold'],
            logprob_threshold=config['whisper']['logprob_threshold'],
            no_speech_threshold=config['whisper']['no_speech_threshold'],
            fp16=config['whisper']['fp16'] if torch.cuda.is_available() else False
        )
        return result
    except Exception as e:
        logging.error(f"Error during transcription: {str(e)}")
        return None

def process_audio(config):
    if config['preprocess']['enabled']:
        logging.info("Preprocessing audio...")
        preprocess_audio(config)
        audio_file = config['preprocess']['output_file']
    else:
        audio_file = config['audio']['input_file']

    logging.info(f"Processing audio file: {audio_file}")

    transcription_result = transcribe_audio(audio_file, config)
    
    if not transcription_result:
        return None

    diarization = None
    if config['diarization']['enabled']:
        try:
            diarization = diarize_audio(audio_file, config)
        except Exception as e:
            logging.error(f"Diarization failed: {str(e)}")

    combined_result = []
    diarization_index = 0
    current_speaker = None

    for segment in transcription_result['segments']:
        segment_start = segment['start']
        segment_end = segment['end']

        while diarization_index < len(diarization) and diarization[diarization_index][1] <= segment_start:
            if diarization[diarization_index][2] == "SPEAKER":
                current_speaker = f"SPEAKER_{diarization_index % 2 + 1}"
            elif diarization[diarization_index][2] == "PAUSE":
                combined_result.append({
                    'type': 'pause',
                    'start': diarization[diarization_index][0],
                    'end': diarization[diarization_index][1]
                })
            diarization_index += 1

        combined_result.append({
            'type': 'speech',
            'speaker': current_speaker if current_speaker else "UNKNOWN",
            'start': segment_start,
            'end': segment_end,
            'text': segment['text']
        })

    translation = None
    if config['translation']['enabled']:
        translation = translate_text(transcription_result['text'], config)

    return {
        'language': transcription_result['language'],
        'segments': combined_result,
        'translation': translation
    }