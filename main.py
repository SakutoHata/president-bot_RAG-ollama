import os
import json
import re
import logging
import secrets  # secretsモジュールをインポート
from flask import Flask, Response, request, render_template, stream_with_context, abort, jsonify, redirect, url_for, flash, session
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores.faiss import FAISS
from dotenv import load_dotenv
from src.rag import rag as generate

load_dotenv()

def check_file_exists(file_path):
    return os.path.isfile(file_path)


app = Flask(__name__)

# セッション情報
app.secret_key = secrets.token_hex(16)  # 16バイト（32文字）のランダムなシークレットキーを生成

# ログの設定
logging.basicConfig(level=logging.INFO)  # ログレベルをINFOに設定

response_data = []

@app.before_request
def before_request():
    if request.headers.get('X-Forwarded-Proto') == 'https':
        request.environ['wsgi.url_scheme'] = 'https'

@app.route('/health', methods=['GET'])
def health():
    return 'Healthy', 200

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']    
    return Response(stream_with_context(generate(user_message)), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)