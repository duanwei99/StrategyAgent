@echo off
echo Starting Streamlit Frontend...
echo.
echo Make sure Backend is already running on http://localhost:8000
echo.

streamlit run frontend/app.py --server.port 8501 --server.address localhost

pause

