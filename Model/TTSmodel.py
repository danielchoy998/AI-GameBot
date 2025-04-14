import requests
import json
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play
import time 
import os
import io
import logging

# Set up the logger
logger = logging.getLogger(__name__)

load_dotenv() 
SECRET_KEY = os.getenv("CANTONESEAI_API_KEY")
url = "https://cantonese.ai/api/tts"

# 🔹 設定預設測試文本
DEFAULT_PROMPT = "你食咗飯未呀？"

def text_to_speech (text):
    """
    調用 TTS API，將文字轉語音
    :param text: 要轉換的文字
    :param api_key: API 金鑰
    :param url: TTS API 地址（預設為 Cantonese.ai）
    """
    logger.info("正在發送 TTS API 請求...")
    payload = json.dumps({
    "api_key": SECRET_KEY,
    "text": text,  
    "frame_rate": "24000", # 8000 or 16000 or 24000
    "speed": 1,
    "pitch": 0,
    "lang": "cantonese", # english or mandarin or cantonese
    "output_extension": "wav",
    "voice_id": "21c29c82-85e8-4f50-8d4b-aa84717b4115",
    "should_enhance": False
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST",url, headers=headers, data=payload)
    return response

def play_audio(response):
    audio = AudioSegment.from_file(io.BytesIO(response.content), format="wav")
    play(audio)
        

def main():
    while True:
        # 讓用戶輸入測試文本，直接按 Enter 使用預設值
        text = input("請輸入測試 TTS 嘅內容（輸入 'exit' 離開）：")

        # 如果輸入 'exit'，結束程式
        if text.lower() == "exit":
            print("已退出 TTS 測試！")
            break

        # 如果無輸入，則使用預設文本
        elif not text:
            text = DEFAULT_PROMPT
            print(f"使用預設文本: {text}")

        # 調用 TTS 生成語音
        response = text_to_speech(text)
        play_audio(response)


# 測試 TTSmodel 時用
if __name__ == "__main__":
    print("TTS 測試開始，等待用戶輸入...")
    main()
