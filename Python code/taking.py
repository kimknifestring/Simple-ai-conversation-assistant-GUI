import pyaudio
import wave
import threading
import os
import json
import openai

def record_audio(output_filename, record_seconds=5):
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 1
    fs = 44100  # Record at 44100 samples per second
    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print("녹음 중...")

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # 지정된 시간동안 데이터를 저장
    for _ in range(0, int(fs / chunk * record_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # 스트림 종료 및 닫기
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("녹음 완료")

    # WAV 파일로 저장
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

def transcribe_audio(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    api_path = os.path.join(script_dir, '../apiKey.json')

    with open(api_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    openai.api_key = data['gptapi']
    
    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file, language="ko")
    
    return transcript["text"]