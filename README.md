# president-bot_RAG-ollama

## はじめに
こちら、以前公開した[*presiden-bot_RAG*](https://github.com/SakutoHata/president-bot_RAG)のOllama対応版となります。

## システム構成
![ボット構成図](/images/ボット構成図.png)<br>
Dockerコンテナを用いて、Ubuntu環境にて実行可能な構成となっております。

## セットアップ
「初回のみ」と付くものは、初回で必須の対応となります。<br>
初回のセットアップが済んでいる場合は「[4. アプリの起動 初回以降の場合](#4-アプリの起動)」を参考にしてアプリを起動させてください。<br>
なお、DockerやUbuntu、VsCode等の準備ができてない方は、「」を参考にこちらを先に対応して下さい。

### 1. ローカルPCでの準備（初回のみ）
1. 当リポジトリをcloneし、VsCodeで開いてください。
2. 各ファイルを配置して下さい。
    ```
    president-bot_RAG-ollama/
        ├── db/
        │   └── 対象CSVデータ
        ├── prompts/
        │   └── character_prompts_gemma.txt （※1を参考に作成）
        ├── static/
        │   ├── images/
        │   │   ├── background.jpg      （モデル背景画像）
        │   │   ├── bot-icon.png        （チャット欄 ボット用アイコン）
        │   │   └── user-icon.png       （チャット欄 ユーザ用アイコン）
        │   ├── models/
        │   │   └── vrm/
        │   │       └── 対象VRモデル     （VRMファイル形式）
        │   └── motions/
        │       └── vrma/
        │           └── 対象VRモデル用アニメーション×4（VRMAファイル形式 4つ配置）
        └── .env (※2 については必ず記載し格納すること)
    ```
    ※1 [URL](https://www.promptingguide.ai/models/gemma)

    ※2 *FILE_PATH="/workspaces/president-bot_RAG-ollama"*

### 2. VsCodeにてDocker環境を構築
1. 導入済みのDocker Desktopを起動させて下さい。
2. 導入済みのdev containerを用いて、「reopen container」でDocker環境の構築を行って下さい。
### 3. Ollamaの準備
#### 3-1. Ollama Serverの立ち上げ
ターミナルにて、以下のコマンドを実行して下さい。
```
cd ../../usr/bin
ollama serve
```
#### 3-2. Ollama modelのインストール（初回のみ）
新しいターミナルを立ち上げ、以下のコマンドを実行して下さい。
```
cd ../../usr/bin
ollama pull mxbai-embed-large
ollama pull schroneko/gemma-2-2b-jpn-it
```
### 4. アプリの起動
各ケースに沿った対応をして下さい。

- 初回対応の場合<br>

    VsCodeのターミナルにて、以下のコマンドを実行して下さい。

    ```
    /usr/bin/python3 /workspaces/president-bot_RAG-ollama/main.py
    ```

- 初回以降の場合<br>
    1. Docker Desktopを立ち上げ、対象のコンテナを起動して下さい。

    2. 各方法からアプリを起動させて下さい。
    - VsCodeの場合<br>
        1. 該当コンテナに入って下さい。
        2. 以下のコマンドをターミナルで実行してください。
            ```
            cd ../../usr/bin && ./ollama serve &
            python3 main.py
            ```
    - Ubuntuの場合<br>
        以下のコマンドを実行してください。
        ```
        docker exec -d ＜コンテナ名＞ /bin/bash
        cd /usr/bin
        ollama serve &
        cd ../../workspaces/president-bot_RAG-ollama
        python3 main.py
        ```