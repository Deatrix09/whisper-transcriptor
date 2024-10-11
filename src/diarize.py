from pyannote.audio import Pipeline
import logging

def diarize_audio(audio_file, config):
    logging.info("Performing speaker diarization...")
    pipeline = Pipeline.from_pretrained(config['diarization']['model'],
                                        use_auth_token=config['diarization']['auth_token'])
    diarization = pipeline(audio_file, 
                           num_speakers=config['diarization']['num_speakers'],
                           min_speakers=1,
                           max_speakers=config['diarization']['num_speakers'])
    return [(turn.start, turn.end, speaker) for turn, _, speaker in diarization.itertracks(yield_label=True)]