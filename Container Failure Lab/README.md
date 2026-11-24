# Container Failure Lab

## Setup

Clone the repository and enter the project directory:

```bash
git clone <repository-url>
cd Container\ Failure\ Lab
```

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip3 install flask
```

Run the Flask application:

```bash
python app.py
```

---

## Troubleshooting: `Address already in use`

Port `5000` is in use by another program. Either identify and stop that program, or start the server with a different port:

1. **Check which process is using port `5000`:**
   ```bash
   lsof -i:5000
   ```
   Stop or kill the process after checking which process is using it.

2. **Change the port in `app.py`**, or **use port forwarding** when running the container (see below).

---

## Build and Run with Docker

1. **Build the Docker image:**
   ```bash
   docker build -t hello_app .
   ```
   See `hello_app` images using:
   ```bash
   docker images
   ```

2. **Run the container:**
   ```bash
   docker run -d --name=hello_app -p 5000:5000 hello_app:latest
   ```
   Or use port forwarding (for example, host port `5001` to container port `5000`):
   ```bash
   docker run -d -p 5001:5000 --name=hello_app hello_app:latest
   ```
   See the running container using:
   ```bash
   docker ps
   ```

3. **Test in your browser:**
   Run `http://127.0.0.1:5000` in your browser. It should show `"Hello from the Container Failure Lab"` on the web page. It also works on `http://0.0.0.0:5000/`.

---

## Let's Break the Lab

Delete all containers and images built so far so you can try the scenarios:

```bash
docker rm -f hello_app
docker rmi hello_app:latest
```

See the `scenario` folder for further lab exercises.