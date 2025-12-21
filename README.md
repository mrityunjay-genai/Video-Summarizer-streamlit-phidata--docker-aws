# Streamlit app Docker Image
## Used Tech
-  Streamlit
-  Phidata Framework
-  Docker
-  AWS EC2

## 1. Login with your AWS console and launch an EC2 instance
## 2. Run the following commands

Note: 
-   Do the port mapping to this port:- 8501
-   To execute gpt_app.py with docker or docker-compose change the app.y to gpt-app.py 

```bash
sudo apt-get update -y

sudo apt-get upgrade

#Install Docker

curl -fsSL https://get.docker.com -o get-docker.sh

sudo sh get-docker.sh

sudo usermod -aG docker ubuntu

newgrp docker
```

```bash
git clone "your-project"
```
```
nano .env
GOOGLE_API_KEY=<Google AI Studio api_key without double quotes>
```
```bash
docker compose up
docker compose down
docker compose stop
docker compose start 
```

```bash
docker build -t mrityunjaygenai/video_summarizer:latest . 
```

```bash
docker images -a  
```

```bash
docker run -d -p 8501:8501 mrityunjaygenai/video_summarizer 
```
```bash
docker run --rm --env-file .env -p 8501:8501 mrityunjaygenai/video_summarizer 
```

```bash
docker ps  
```

```bash
docker stop container_id
```

```bash
docker rm $(docker ps -a -q)
```

```bash
docker login 
```

```bash
docker push mrityunjaygenai/video_summarizer:latest 
```

```bash
docker rmi mrityunjaygenai/video_summarizer:latest
```

```bash
docker pull mrityunjaygenai/video_summarizer
```






