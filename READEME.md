



# Step up K8s Web App Setup Guide

This guide assumes the following:
- You've already gone through the <a href="https://github.com/khutchi2/simple_k8s_webapp?tab=readme-ov-file"> Simple K8s Webapp </a>
- Running K8s cluster using Rancher Desktop
- You already have K8s, kubectl, etc. installed

## I. dockerhub Repo
1. Because you've already walked through the simpler version of the app, just setup a new repository for this step-up web app.

## II. Project Structure
Same drill as before, either you can clone this repo, or set it all up yourself.  Because I don't want this README to be a novel, I'm going to skip including all of the file contents here and instead just include a brief description of what each file/component is for.
```
stepup-k8s-webapp/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   ├── schema.sql
│   ├── requirements.txt
│   └── templates/
│       └── index.html
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
│
├── Dockerfile
│
└── k8s/
    └── k8s-manifests.yaml

```

### 1. Dockerfile
The Dockerfile is the same as before.  Just a basic Python image to run our Flask app in.


### 2. app
#### main.py
This is a basic Flask app with a REST API and a SQLite database.  There are endpoints for retrieving and adding items.  The database initializes when the app starts.

#### requirements.txt
A file for grabbing the needed dependencies for the app to run.  ```flask``` is obviously needed for the Flask app and ```gunicorn``` is for <insert_explanation>.

### 3. k8s
```k8s-manifests.yaml```


## III. Deployment Steps
This will all be much the same as before.

1. Build the docker images in the ```/app``` and ```/nginx``` directories.
```bash
docker build -t <username>/<repo-name>:<tag> .
```

2. Push the docker images to DockerHub, run:
```bash
docker push <username>/<repo-name>:<tag>
```

2. Apply the Kubernetes manifests and kick off spinning up the app by running:
```bash
kubectl apply -f k8s/k8s-manifests.yaml/
```
3. Find the pod name (and check that there haven't been any errors) by running:
```bash
kubectl get pods
```

4. To view the web app you'll first need to forward the port:
```bash
kubectl port-forward service/nginx-service 8080:80
```
5. Open a web browser and enter the following into the URL bar:
```
localhost:8080/
```
hopefully you'll see a page with a couple of text boxes.  Type something in and it should post it on the page.