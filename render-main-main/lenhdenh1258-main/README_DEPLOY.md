Deploy guide — frontend on Netlify, backend on Render

Overview
- Frontend (static files) lives in `test-main 2` and can be deployed to Netlify.
- Backend (`test-main 2/server.py`) is a small Python HTTP server; deploy it to Render as a Web Service.

Frontend (Netlify)
1. Create a GitHub repo and push this project.
2. In Netlify, create a new site from Git -> GitHub.
3. Set the "Publish directory" to `test-main 2` and deploy (no build command required for static files).
4. In Site settings -> Environment, add `API_BASE` with the backend URL (e.g. `https://your-backend.onrender.com`).

Backend (Render)
1. Create a GitHub repo and push this project (or use the same repo).
2. In Render dashboard, create a new "Web Service" and connect your repo.
3. Set the start command to:
   ```bash
   python3 'test-main 2/server.py'
   ```
4. Set environment variables in Render:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID` (use numeric chat id for direct messages, or `@groupusername`/-100... for groups)
   - Optionally `PORT` (Render sets one automatically via `$PORT` — the server reads `PORT` env var).
5. If you need persistent storage for SQLite, use Render Volumes (paid) or migrate to PostgreSQL and set `DATABASE_URL`.

Notes
- The server uses only Python standard library; `requirements.txt` is left empty as a placeholder.
- If you want everything on Netlify, the backend must be rewritten as Netlify Functions and use a hosted DB (e.g., Supabase).

If you want, I can:
- Create the GitHub repo and push the code for you (you'll need to connect credentials), or
- Prepare a Dockerfile and instructions for Fly.io instead, or
- Walk you step-by-step through linking Netlify + Render webhooks and env vars.
