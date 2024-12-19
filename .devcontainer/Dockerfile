# ベースイメージにUbuntuを使用
FROM ubuntu:22.04

# 必要なパッケージをインストール（非対話モードに設定）
ENV DEBIAN_FRONTEND=noninteractive

# 必要なパッケージをインストール（bashを含む）
RUN apt-get update && apt-get install -y \
    bash \
    software-properties-common \
    build-essential \
    git \
    curl \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    python3-gi \
    python3-gi-cairo \
    nano \
    vim \
    lsof \
    && add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update && apt-get install -y \
    python3.9 \
    python3.9-venv \
    python3.9-dev \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# OllamaのLinux用バイナリをダウンロード
RUN curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o /usr/bin/ollama.tgz
# アーカイブを展開
RUN tar -xzf /usr/bin/ollama.tgz -C /usr/bin/ && \
    rm /usr/bin/ollama.tgz

# デフォルトのPythonを3.9に設定
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# ローカルのrequirements.txtをコンテナ内にコピー
COPY requirements.txt ./

# Pythonのパッケージをインストール
RUN pip3 install --no-cache-dir -r requirements.txt

# コンテナ内のポートを開放
EXPOSE 5000
EXPOSE 11434

# パスを設定
ENV PATH="/usr/bin/bin:${PATH}"

# コンテナ起動時にOllamaを起動
CMD ["/usr/bin/bin/ollama", "serve"]