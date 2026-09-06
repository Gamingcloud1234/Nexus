# NEXUS MC — Fixed White UI

## Fix
The GET ACCESS CODE button now performs normal top-level browser navigation to YouTube rather than attempting to embed YouTube inside Streamlit.

## Deploy
Upload `app.py`, `database.py`, `requirements.txt`, and `.streamlit/secrets.toml.example` to GitHub.
Deploy `app.py` on Streamlit Community Cloud.

In Advanced settings → Secrets:
```toml
ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"
```

The YouTube visit is not subscription verification. The portal does not request Minecraft/Microsoft credentials.
