import logging
import numpy as np
from pydub import AudioSegment
import librosa

def simple_energy_based_diarization(audio_file, config):
    logging.info("Performing simple energy-based diarization...")
    
    audio = AudioSegment.from_wav(audio_file)
    samples = np.array(audio.get_array_of_samples())
    
    if audio.channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)
    
    frame_length = int(config['diarization']['frame_length'] * audio.frame_rate)
    hop_length = int(config['diarization']['hop_length'] * audio.frame_rate)
    energy = librosa.feature.rms(y=samples, frame_length=frame_length, hop_length=hop_length)[0]
    
    threshold = np.mean(energy) * config['diarization']['energy_threshold']
    speech_frames = energy > threshold
    
    times = librosa.frames_to_time(np.arange(len(speech_frames)), sr=audio.frame_rate, hop_length=hop_length)
    
    segments = []
    is_speech = False
    start_time = 0
    min_silence_duration = config['diarization']['min_silence_duration']
    
    for i, time in enumerate(times):
        if speech_frames[i] and not is_speech:
            if segments and time - segments[-1][1] >= min_silence_duration:
                segments.append((segments[-1][1], time, "PAUSE"))
            start_time = time
            is_speech = True
        elif not speech_frames[i] and is_speech:
            if time - start_time >= config['diarization']['min_speech_duration']:
                segments.append((start_time, time, "SPEAKER"))
            is_speech = False
    
    if is_speech:
        segments.append((start_time, times[-1], "SPEAKER"))
    
    return segments

def diarize_audio(audio_file, config):
    return simple_energy_based_diarization(audio_file, config)