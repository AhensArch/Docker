## Scenario 01: Exit 0

### Change to the Base App

Update the `Dockerfile` instruction to:

```dockerfile
CMD ["sh", "-c", "python app.py &"]
```

Build and run the container again:

```bash
docker build -t hello_app .
docker run -d --name=hello_app -p 5000:5000 hello_app:latest
```

Using `CMD ["sh", "-c", "python app.py &"]` detaches `python app.py` into a background subshell and lets `sh` exit immediately (`Exited (0)`), which terminates the container because PID 1 (`sh`) finished.

---

### What to Observe & Test Next in This Failure Mode

1. **Verify the container is not running in `docker ps` (1 min):**
   ```bash
   docker ps
   docker ps -a
   ```
   *Verification:* `docker ps` shows no `hello_app` row, while `docker ps -a` shows `hello_app` with `Exited (0)`.

2. **Inspect container logs to see why nothing stayed up (1 min):**
   ```bash
   docker logs hello_app
   ```
   *Verification:* The command returns with little or no Flask startup output because `python app.py` was backgrounded and orphaned when `sh` exited.

3. **Confirm port 5000 is not bound by the exited container (1 min):**
   Open `http://127.0.0.1:5000/` in your browser or run:
   ```bash
   curl -i [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
   ```
   *Verification:* The connection is refused because no active listener is running inside a live container.

---

### Why This Happened

A container stays alive **only as long as its main process (PID 1) stays running**. In your `Dockerfile`, `CMD ["sh", "-c", "python app.py &"]` told the shell (`sh`) to start `python app.py` in the background (`&`) and immediately move on—so `sh` finished right away, and Docker shut down the container.

1. **The `&` sends `python app.py` to the background:** Instead of waiting for Flask to keep running, `sh -c` launches `python app.py &` as a background job and reaches the end of its command right away.
2. **PID 1 finishing ends the container:** In Docker, the command in `CMD` runs as the main container process (PID 1). The moment `sh` exits with code `0`, Docker considers the container's job done and stops it—even if `python app.py` was started in the background.
3. **Why `CMD ["python", "app.py"]` works differently:** Without `&`, `python app.py` runs in the foreground as the main process and stays running to serve requests, so the container stays `Up`.

---

### See the Difference Yourself

1. **Run a quick foreground vs. background check (1 min):**
   ```bash
   docker run --rm alpine sh -c "sleep 2 & echo done"
   ```
   *Verification:* The container prints `done` and exits right away without waiting for the backgrounded process to keep the container alive.

2. **Compare with a foreground process (1 min):**
   ```bash
   docker run --rm alpine sh -c "echo starting && sleep 5"
   ```
   *(Press `Ctrl + C` while it is waiting if you want to stop early.)*
   *Verification:* The container stays active for the full 5 seconds (or until interrupted) because the foreground `sh` process has not exited yet.

---

### Other Ways to Trigger `Exited (0)` in a Container

* **A command that finishes immediately:** Using `CMD ["echo", "done"]` or `CMD ["true"]` prints output or does nothing, then exits cleanly with code `0`.
* **A short-lived script:** Running a script or command that completes its work and returns without staying open (such as a one-off setup or print command) exits with `0` as soon as the last line finishes.
* **A server that exits early instead of blocking:** If a program or wrapper starts something else and returns `0` immediately—or hits an early return path coded to exit `0`—the container stops with `Exited (0)`.
* **Stopping the container normally (`docker stop`):** Sending a normal stop signal lets a well-behaved process shut down cleanly, resulting in a `0` (or `143` if killed by `SIGTERM`) exit code.

---

## Scenario: Short-Lived Script (`Exited (0)`)

### Change to the Base App

Update the `Dockerfile` instruction to run a short-lived Python snippet:

```dockerfile
CMD ["sh", "-c", "python - <<'EOF'\nprint('Starting short-lived script...')\ntotal = sum(range(5))\nprint(f'Completed with total={total}')\nEOF"]
```

Build and run the container:

```bash
docker build -t hello_app .
docker run -d -p 5000:5000 --name=hello_app hello_app:latest
```

---

### What Your Output Shows

```text
docker run -d -p 5000:5000 --name=hello_app hello_app:latest
f81289f83f671e37e717d2f1590fb8cff053474a446b52e9f7d7ed4ee3db38b6

docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

docker ps -a
CONTAINER ID   IMAGE              COMMAND                  CREATED         STATUS                     PORTS     NAMES
f81289f83f67   hello_app:latest   "sh -c 'python - <<'…"   6 seconds ago   Exited (0) 5 seconds ago             hello_app

docker logs f81289f83f67
Starting short-lived script...
Completed with total=10
```

1. **Completed successfully, not crashed:** `Exited (0)` means the command finished with zero errors. In Docker, `Exited (0)` is normal for batch jobs or one-off scripts, whereas a long-running service like a Flask web server is expected to stay up.
2. **Logs show full execution:** Unlike `python app.py &` (where `sh` exited immediately and orphaned the background process), here `python` ran in the foreground until `sum(range(5))` finished (`0 + 1 + 2 + 3 + 4 = 10`) and printed `Completed with total=10`.
3. **Why `docker ps` is empty:** Once the script finishes and `sh` exits, PID 1 is done, so the container stops and moves to `docker ps -a`.

---

