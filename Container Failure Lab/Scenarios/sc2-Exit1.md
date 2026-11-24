# Scenario 2: Simulating Exit Code 1 (`DB_URL` Startup Guard)

add a startup guard at the top of `app.py` that checks `os.environ.get("DB_URL")`, writes an error message to `sys.stderr`, and calls `sys.exit(1)` when `DB_URL` is missing or empty.

## 1. Update `app.py` with the `DB_URL` Guard

Add `sys` and check `DB_URL` right at the top before starting Flask:

The app.py code is already updated and commented. While running this scenario uncomment it.

## 2. Make Sure `Dockerfile` Runs `app.py` Normally

Keep `CMD ["python", "app.py"]` active (uncommented) in your `Dockerfile` so `app.py` is the main process whose exit code becomes the container's exit code(1).


## 3. Build, Trigger `Exited (1)`, and Verify Fix

1. **Remove any previous `hello_app` container (stop it before rmeoving as the prevoius scenario container is in restarting mode)and rebuild the image:**

   ```bash
   docker rm hello_app 2>/dev/null || true
   docker build -t hello_app .
   ```

2. **Run without `DB_URL` to trigger `Exited (1)`:**

   ```bash
   docker run -p 5000:5000 --name=hello_app hello_app:latest
   ```

   - **Expected result:** It immediately prints `ERROR: DB_URL environment variable is not set.` to `stderr` and exits.

3. **Inspect status and logs:**

   ```bash
   docker ps -a
   docker logs hello_app
   ```

   - **Expected result:** `docker ps -a` shows `hello_app` with `Exited (1)`, and `docker logs hello_app` shows the `DB_URL` error message.

4. **Test the healthy run by passing `DB_URL`:**

   ```bash
   docker rm hello_app
   docker run -p 5000:5000 -e DB_URL="sqlite:///lab.db" --name=hello_app hello_app:latest
   ```

   - **Expected result:** The check passes and Flask starts normally (`Running on all addresses (0.0.0.0)`).