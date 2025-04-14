from flask import Flask, request, jsonify, render_template, Response, stream_with_context
from flask_cors import CORS
import os
import json
import time
import traceback
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  
from LLMmodel import LLMConnector

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')

# Configure CORS more explicitly
CORS(app, resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}})

# Initialize LLM connector
try:
    llm_connector = LLMConnector()
    print("LLM connector initialized successfully")
except Exception as e:
    print(f"Error initializing LLM connector: {str(e)}")
    traceback.print_exc()

# Load character prompt
def load_character_prompt():
    try:
        with open("Character.txt", "r", encoding="utf-8") as file:
            # Modify the prompt to instruct the model to break responses
            prompt = file.read().strip()
            print(f"Character prompt loaded, length: {len(prompt)} characters")
            return prompt
    except FileNotFoundError:
        print("Character.txt not found, using default prompt")
        return "你是一個友善的 AI 助手，請用廣東話回答問題。"
    except Exception as e:
        print(f"Error loading character prompt: {str(e)}")
        traceback.print_exc()
        return "你是一個友善的 AI 助手，請用廣東話回答問題。"

# Get system prompt
system_prompt = load_character_prompt()

# 返回 index.html 頁面（如果前端有 UI，這裡可以渲染畫面）。
@app.route('/')
def index():
    """Serve the main HTML page"""
    return render_template('index.html')

# 提供 API 狀態信息，確保 API 服務正常運行。
@app.route('/api')
def api_info():
    """API information endpoint"""
    return jsonify({
        "status": "ok",
        "message": "AI Chatbot API is running",
        "endpoints": {
            "/chat": "POST - Get AI response to text",
            "/models": "GET - List available models"
        }
    })


# 處理用戶發送的訊息，並透過 LLM 生成 AI 回應。
@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        # 使用 get_json() 確保數據正確
        data = request.get_json()
        print(f"Received chat request: {data}")
        user_message = data.get("message", "").strip() 

        if not user_message:
            return Response("data: " + json.dumps({"error": "No message provided"}) + "\n\n", mimetype="text/event-stream")

        print(f"\n收到請求: {user_message}")  # ✅ 紀錄請求
        print("正在向 OpenAI 發送請求...\n")
        time.sleep(0.1)
        # 獲取 AI 模型
        model_name =  "gpt-4o-mini"
        print(f"Using model: {model_name}")
       
        stream = True
        
        if not user_message:
            return json.dumps({"status": "error", "message": "No message provided"}), 400
        
        def generate():
            try: # 這裡應該使用 OpenAI API 而唔係固定字串
                stream_response = llm_connector.query(
                    model_name="gpt-4o-mini",
                    question=user_message,
                    system_prompt= system_prompt,
                    max_output_tokens=2048,
                    temperature=0.5,
                    stream=True
                )
                print(" AI 正在回應...\n") 
            
                for chunk in stream_response:
                    time.sleep(0.1)
                    yield f"data: {json.dumps({'text': chunk})}\n\n"
            
            finally:
                print("\nAI 回應完成，發送 [DONE]")  # ✅ 確保 Streaming 結束時發送 [DONE]

        return Response(stream_with_context(generate()), content_type='text/event-stream')
        
    except Exception as e:
        print(f"Error in chat: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "Internal Server Error",
            "message": str(e)
        }), 500
            
            

        

if __name__ == '__main__':
    # Create directories if they don't exist
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("Starting AI Gamebot API server...")
    
    # Get port from environment variable or use 8080 as default (changed from 5000 to avoid conflict with AirPlay)
    port = int(os.environ.get('PORT', 2110))
    print(f"Server will run on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)