from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

app = Flask(__name__)

# Together AI API 설정
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')
MODEL_NAME = "lgai/exaone-3-5-32b-instruct"

# 대화 기록을 저장할 리스트
conversation_history = []

def chat_with_together(message, context=""):
    """Together AI API를 통해 EXAONE 3.5 32B 모델과 대화"""
    try:
        if not TOGETHER_API_KEY:
            return "Together AI API 키가 설정되지 않았습니다. .env 파일에 TOGETHER_API_KEY를 설정해주세요."
        
        # 메시지 형식을 Chat Completions API 형식으로 변환
        messages = []
        
        # 시스템 메시지 추가
        messages.append({
            "role": "system",
            "content": "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 친근하고 정확하게 답변해주세요."
        })
        
        # 이전 대화 맥락 추가
        if context:
            context_lines = context.split('\n')
            for line in context_lines:
                if line.startswith('사용자: '):
                    messages.append({"role": "user", "content": line[4:]})
                elif line.startswith('어시스턴트: '):
                    messages.append({"role": "assistant", "content": line[6:]})
        
        # 현재 사용자 메시지 추가
        messages.append({"role": "user", "content": message})
        
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODEL_NAME,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
            "top_p": 0.9
        }
        
        response = requests.post(TOGETHER_API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return "죄송합니다. 응답을 생성할 수 없습니다."
        else:
            error_msg = f"API 오류 (상태 코드: {response.status_code})"
            try:
                error_detail = response.json()
                if 'error' in error_detail:
                    error_msg += f": {error_detail['error'].get('message', '알 수 없는 오류')}"
            except:
                pass
            return error_msg
            
    except requests.exceptions.RequestException as e:
        return f"연결 오류: {str(e)}"
    except Exception as e:
        return f"오류가 발생했습니다: {str(e)}"

@app.route('/')
def index():
    """메인 페이지"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """채팅 API 엔드포인트"""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': '메시지를 입력해주세요.'})
        
        # 최근 5개의 대화만 맥락으로 사용
        context = ""
        if len(conversation_history) > 0:
            recent_history = conversation_history[-5:]
            context_parts = []
            for item in recent_history:
                context_parts.append(f"사용자: {item['user']}")
                context_parts.append(f"어시스턴트: {item['bot']}")
            context = "\n".join(context_parts)
        
        # AI 응답 생성
        bot_response = chat_with_together(user_message, context)
        
        # 대화 기록에 추가
        conversation_item = {
            'user': user_message,
            'bot': bot_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        conversation_history.append(conversation_item)
        
        # 대화 기록이 50개를 초과하면 오래된 것부터 제거
        if len(conversation_history) > 50:
            conversation_history.pop(0)
        
        return jsonify({
            'response': bot_response,
            'timestamp': conversation_item['timestamp']
        })
        
    except Exception as e:
        return jsonify({'error': f'서버 오류: {str(e)}'})

@app.route('/clear', methods=['POST'])
def clear_history():
    """대화 기록 초기화"""
    global conversation_history
    conversation_history = []
    return jsonify({'message': '대화 기록이 초기화되었습니다.'})

@app.route('/history')
def get_history():
    """대화 기록 조회"""
    return jsonify({'history': conversation_history})

if __name__ == '__main__':
    print(f"🤖 Together AI + EXAONE 3.5 32B 챗봇이 시작되었습니다!")
    print(f"📱 사용 모델: {MODEL_NAME}")
    if TOGETHER_API_KEY:
        print(f"🔑 API 키: {'*' * (len(TOGETHER_API_KEY)-8) + TOGETHER_API_KEY[-4:]}")
    else:
        print(f"⚠️  API 키가 설정되지 않았습니다! .env 파일에 TOGETHER_API_KEY를 설정해주세요.")
    print(f"🌐 웹 브라우저에서 http://localhost:5000 으로 접속하세요")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000) 