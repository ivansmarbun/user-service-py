# User Service Python Project

This project is a simple Python application designed to help you learn about Docker and set up a basic CI/CD pipeline using Jenkins.

## Features
- Simple Python app
- Dockerized for easy deployment
- Jenkins pipeline for automated build, test, and deploy

---

## Prerequisites
- Docker installed on your host machine
- [Optional] Docker Compose
- Git
- Jenkins (run as a Docker container)

---

## Step-by-Step Installation Guide

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd user-service-py
```

### 2. Build the Jenkins Docker Image (with Docker CLI)
Create a `Dockerfile` in a separate folder (e.g., `dockerfile/`) with the following content:
```dockerfile
FROM jenkins/jenkins:lts
USER root
ARG DOCKER_GID=1001 # Use your host's docker group GID
RUN groupdel docker || true \
    && groupadd -g ${DOCKER_GID} docker \
    && usermod -aG docker jenkins \
    && apt-get update && apt-get install -y docker.io
USER jenkins
```
Build the image:
```bash
docker build --build-arg DOCKER_GID=$(getent group docker | cut -d: -f3) -t myjenkins-docker ./dockerfile
```

### 3. Run Jenkins Container
```bash
docker run -d \
  -p 8080:8080 \
  -v /var/jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --name jenkins_server \
  myjenkins-docker
```

### 4. Access Jenkins
Open your browser and go to `http://localhost:8080`.

### 5. Set Up Jenkins Pipeline
- Use the provided `Jenkinsfile` in this repo for your pipeline configuration.
- Create a new pipeline job in Jenkins and point it to this repository.

### 6. Build and Test
- Trigger the pipeline in Jenkins.
- The pipeline will build the Docker image, run tests, and deploy the app.

---

## Troubleshooting
- Make sure the Docker group GID in your Jenkins image matches your host's Docker group GID.
- Ensure the Jenkins user is in the Docker group inside the container.
- Mount the Docker socket when running Jenkins.

---

## License
MIT

---

## Author
ivansmarbun
