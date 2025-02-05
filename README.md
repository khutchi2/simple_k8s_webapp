# Kubernetes Basic Web App Setup Guide

This guide assumes the following:
- Running K8s cluster using Rancher Desktop
- You already have K8s, kubectl, etc. installed

## I. dockerhub Repo
1. Create dockerhub account (you can login with Google).
2. Create a repo in dockerhub.  As an example, you can look at the <a href="https://hub.docker.com/repository/docker/khutchi2/howdy-earth/general"> howdy-earth repo</a>.  Anywhere in the commands and configs below that you see \<username\> you should put in your own username for dockerhub, and replace \<repo-name\> with your repo's name.
3. To authenticate with dockerhub, in local terminal run:
```bash
docker login
```
and follow the prompts to authenticate with dockerhub via the web.  (If you haven't authenticated, it should give you a key in the terminal along with a URL.  You'll copy and paste the key into the prompt the URL gives you.)

## II. Project Structure
Either you can clone this repo, or if you'd rather, you can go through the exercise of setting up the project yourself.  All of the contents of each file is contained in this README.
```
my-web-app/
├── Dockerfile
├── app/
│   ├── main.py
│   └── requirements.txt
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

### 1. Dockerfile
The dockerfile has no file extension.  Just make a file called "Dockerfile" and you're good.
```dockerfile
# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ .

# Make port 5000 available
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]
```


### 2. app
#### main.py
Super basic Flask app.
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from Docker!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### requirements.txt
```
flask==3.0.0
```




### 3. k8s
#### deployment.yaml (k8s deployment)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: <repo-name>
        image: <username>/<repo-name>:webapp
        ports:
        - containerPort: 5000
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
```

#### service.yaml (k8s service)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
  selector:
    app: webapp
```

## III. Deployment Steps

1. To build Docker image, from the same directory as the Dockerfile, run:
```bash
docker build -t <username>/<repo-name>:webapp .
```

2. Apply the Kubernetes manifests and kick off spinning up the app by running:
```bash
kubectl apply -f k8s/
```
3. Find the pod name (and check that there haven't been any errors) by running:
```bash
kubectl get pods
```

4. To view the web app you'll first need to forward the port.  This is basically how you open up your cluster to your web browser.  You'll need to run the command below.  From the previous command, you can copy and paste the pod with name prefixed "webapp".  (It will probably look something like: *webapp-6b6c6c5498-h4xcf*.)
```bash
kubectl port-forward pod/<pod-name> 5000:5000
```
5. Open a web browser and enter the following into the URL bar:
```
localhost:5000
```
hopefully you'll see a mostly blank page that says, "Hello from Docker!"