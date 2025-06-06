from flask import Flask, request, jsonify, render_template_string
import requests
import os
import json
from datetime import datetime

app = Flask(__name__)

# Together AI API 설정
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
MODEL_NAME = "lgai/exaone-3-5-32b-instruct"

# 간단한 HTML 템플릿 (인라인으로 포함)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 EXA Chat - EXAONE 3.5 32B</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; min-height: 100vh; display: flex; flex-direction: column; }
        .header { text-align: center; color: white; margin-bottom: 30px; }
        .chat-container { flex: 1; background: white; border-radius: 15px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); display: flex; flex-direction: column; }
        .messages { flex: 1; overflow-y: auto; margin-bottom: 20px; max-height: 400px; }
        .message { margin-bottom: 15px; padding: 12px; border-radius: 10px; max-width: 80%; }
        .user-message { background: #007bff; color: white; margin-left: auto; }
        .bot-message { background: #f1f3f4; color: #333; }
        .input-container { display: flex; gap: 10px; }
        .message-input { flex: 1; padding: 12px; border: 2px solid #ddd; border-radius: 25px; outline: none; }
        .send-btn { padding: 12px 20px; background: #007bff; color: white; border: none; border-radius: 25px; cursor: pointer; }
        .send-btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 EXA Chat</h1>
            <p>EXAONE 3.5 32B Instruct와 대화하세요</p>
        </div>
        <div class="chat-container">
            <div class="messages" id="messages">
                <div class="message bot-message">
                    안녕하세요! 👋 EXAONE 3.5 32B AI 어시스턴트입니다.<br>
                    무엇이든 궁금한 것이 있으시면 편하게 물어보세요!
                </div>
            </div>
            <div class="input-container">
                <input type="text" class="message-input" id="messageInput" placeholder="메시지를 입력하세요..." maxlength="1000">
                <button class="send-btn" onclick="sendMessage()">전송</button>
            </div>
        </div>
    </div>

    <script>
        const messagesDiv = document.getElementById('messages');
        const messageInput = document.getElementById('messageInput');

        function addMessage(content, isUser = false) {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
            messageDiv.innerHTML = content;
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            if (!message) return;

            addMessage(message, true);
            messageInput.value = '';

            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });

                const data = await response.json();
                if (data.error) {
                    addMessage(`❌ 오류: ${data.error}`);
                } else {
                    addMessage(data.response);
                }
            } catch (error) {
                addMessage(`❌ 연결 오류: ${error.message}`);
            }
        }

        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
"""

def chat_with_together(message):
    """Together AI API를 통해 EXAONE 3.5 32B 모델과 대화"""
    try:
        if not TOGETHER_API_KEY:
            return "Together AI API 키가 설정되지 않았습니다."
        
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 친근하고 정확하게 답변해주세요."},
                {"role": "user", "content": message}
            ],
            "temperature": 0.7,
            "max_tokens": 1000
        }
        
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
        
        return f"API 오류 (상태 코드: {response.status_code})"
            
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

@app.route('/')
def index():
    """메인 페이지"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat():
    """채팅 API 엔드포인트"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': '메시지를 입력해주세요.'})
        
        bot_response = chat_with_together(user_message)
        
        return jsonify({
            'response': bot_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'})

# Vercel에서 인식할 수 있도록 app을 export 