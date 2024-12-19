from flask import Flask, Response, request, stream_with_context
from langchain_community.llms import Ollama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate, MessagesPlaceholder
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import os
import re
import time
from dotenv import load_dotenv

load_dotenv()
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
# 埋め込みモデルとLLMの設定
## Ollamaのモデルを使う場合
# embeddings = OllamaEmbeddings(model="mxbai-embed-large") # "mxbai-embed-large" "snowflake-arctic-embed2:latest"
## Huggingfaceのモデルを使う場合
embeddings = HuggingFaceEmbeddings(model_name="pkshatech/GLuCoSE-base-ja")

"""
model_name

・schroneko/gemma-2-2b-jpn-it:latest
・hf.co/dahara1/gemma-2-2b-jpn-it-gguf-japanese-imatrix:Q8_0_L  ← 個人的にはこちらがオススメ
・hf.co/dahara1/gemma-2-2b-jpn-it-gguf-japanese-imatrix:Q3_K_L
・hf.co/dahara1/gemma-2-2b-jpn-it-gguf-japanese-imatrix:Q4_K_L
"""
llm = Ollama(model="hf.co/dahara1/gemma-2-2b-jpn-it-gguf-japanese-imatrix:Q4_K_L", callbacks=callback_manager) # model変数はmodel_nameを例に指定してください。
FILE_PATH = os.environ["FILE_PATH"]

# FAISSインデックスの読み込みまたは作成
if os.path.exists(f'{FILE_PATH}/db/index.faiss'):
    index = FAISS.load_local(f"{FILE_PATH}/db", embeddings=embeddings, allow_dangerous_deserialization=True)
else:
    print("none index")
    loader = CSVLoader(file_path=f'{FILE_PATH}/db/merge_president_blog.csv', encoding='utf-8')
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    documents = text_splitter.split_documents(docs)
    index = FAISS.from_documents(documents, embeddings)
    index.save_local(f'{FILE_PATH}/db')

retriever = index.as_retriever(search_type="similarity", search_kwargs={"k": 5})


def rag(user_query):
    # 検索して関連ドキュメントを取得
    docs = retriever.invoke(user_query)
    contents = [re.search(r"Contents:\s*(.*)", doc.page_content).group(1) for doc in docs if re.search(r"Contents:\s*(.*)", doc.page_content)]
    contents = [item.replace("\u3000", "") for item in contents]
    context = [item.replace("〽", "") for item in contents]
    print(f"context： \n{context}")

    # 参照するPromptのテンプレートを指定
    """
    ・character_prompts.txt：モデル指定なし
    ・character_prompts_gemma.txt：gemma系モデル
    ・character_prompts_Tanuki.txt：Tanuki系 / Alpaca系モデル
    """
    TARGET_PROMPT = f'{FILE_PATH}/prompts/character_prompts_gemma.txt'

    with open(TARGET_PROMPT, 'r', encoding='utf-8') as f:
            system_prompt = f.read()

    if "gemma" or "Tanuki" in TARGET_PROMPT:
        # Promptに各情報を入力
        formatted_prompt = system_prompt.replace("{context}", "\n".join(context)).replace("{question}", user_query)
        # 処理開始時間
        start_time = time.time()
        response = llm.invoke(formatted_prompt)
        # 処理終了時間
        end_time = time.time()
        #print(response)
        print(f"処理時間：{format(end_time-start_time, '.3f')}s")
    else:   
        user_prompt = "context: {context}\nQuestion: {question}\nAnswer:"
        # ChatPromptTemplateを作成
        prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(system_prompt),
            HumanMessagePromptTemplate.from_template(user_prompt)
        ])
        # 処理開始時間
        start_time = time.time()
        # プロンプトを文字列にフォーマット
        formatted_prompt = prompt.format(context="\n".join(context), question=user_query)
        response = llm.invoke(formatted_prompt)
        # 処理終了時間
        end_time = time.time()
        #print(response)
        print(f"処理時間：{format(end_time-start_time, '.3f')}s")
    
    yield response