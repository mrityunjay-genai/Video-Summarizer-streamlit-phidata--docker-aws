FROM python:3.10.19-alpine
EXPOSE 8501
# Install Python3, pip, git, and build essentials for Alpine
RUN apk add --no-cache \
    python3 \
    py3-pip \
    git \
    build-base

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]