import os
import json
from typing import Dict, Any, List, Union
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class LLMConnector:
    
    def __init__(self):
        # 載入環境變量
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.openai_client = None
        
        # 初始化 OpenAI 客戶端（如果有 API Key）
        if self.openai_api_key:
            self.openai_client = OpenAI(api_key=self.openai_api_key)
        else:
            raise ValueError("OpenAI API 密鑰未設置，請確認 .env 文件中有 OPENAI_API_KEY")
        
        # 可用模型列表
        self.available_models = {
            "openai": ["gpt-4o-mini"]
        }

    def get_available_models(self) -> Dict[str, List[str]]:
        """獲取所有可用的模型列表"""
        return self.available_models
        
    def query(self, 
             model_name: str, 
             question: str, 
             system_prompt: str,
             max_output_tokens: int = 512,
             temperature: float = 0.7,
             stream: bool = True
             ) -> Union[Dict[str, Any], Any]:

        try:
            print(f"正在調用 OpenAI API：模型={model_name}, 問題='{question}'")
            if stream:
                # 使用 Responses API 創建流式回應
                response = self.openai_client.responses.create(
                    model=model_name,
                    input=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    max_output_tokens=max_output_tokens,
                    temperature=temperature,
                    stream=True
                )
                print("開始 Streaming 回應\n")  # ✅ 紀錄 Streaming 開始
                for event in response:
                    if hasattr(event, "type") and "text.delta" in event.type:
                        print(event.delta, end="", flush=True)  # Debug 記錄 API 回應
                        yield event.delta  # Streaming 回應
            else:
                response = self.openai_client.responses.create(
                    model=model_name,
                    input=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    max_output_tokens=max_output_tokens,
                    temperature=temperature,
                    stream=True
                    )
                full_response = "".join(event.text for event in response if hasattr(event, "text"))
                print(f" 非 Streaming 完整回應: {repr(full_response)}") 
                return {"response": full_response}
                
        except Exception as e:
            print(f"OpenAI API 錯誤: {str(e)}")
            raise ValueError(f"查詢 OpenAI 時發生錯誤: {str(e)}")

# 創建簡單的使用示例
def main():
    """測試 LLM Connector 的功能"""
    connector = LLMConnector()
    
    # 顯示可用模型
    available_models = connector.get_available_models()
    print("可用模型:")
    for provider, models in available_models.items():
        print(f"- {provider}: {', '.join(models)}")
    
    # 選擇模型和問題
    model_name = input("請選擇模型 (例如 'gpt-4o-mini'): ")
    question = input("請輸入問題: ")
    
    # 載入系統提示詞
    try:
        with open("Character.txt", "r", encoding="utf-8") as file:
            system_prompt = file.read().strip()
    except FileNotFoundError:
        system_prompt = "你是一個友善的 AI 助手，請用廣東話回答問題。"
    
    # 調用 LLM
    try:
        response = connector.query(model_name, question, system_prompt)
        print("\n回應:")
        for chunk in response:
            print(chunk, end="", flush=True)
        print("\nStreaming end\n")
        
    except Exception as e:
        print(f"發生錯誤: {str(e)}")

if __name__ == "__main__":
    main() 