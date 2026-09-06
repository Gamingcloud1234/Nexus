# NEXUS MC — Streamlit

White/light NEXUS MC community access portal.

## Files
- app.py
- database.py
- requirements.txt

## Local
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Streamlit Community Cloud
Deploy `app.py` from GitHub. In Advanced settings → Secrets, add:

```toml
ADMIN_PASSWORD = "YOUR_ADMIN_PASSWORD"
```

The app uses a local SQLite file for basic demo persistence. For a production shared database, replace SQLite with a hosted database such as PostgreSQL/Supabase.

## Important
The YouTube return flow does NOT verify a YouTube subscription. It only redirects the visitor to the channel and issues a portal code when they return. The app never asks for Minecraft/Microsoft credentials.
