# Health Coach AI - Startup Script
# This script runs the Streamlit app with analytics disabled

$env:STREAMLIT_LOGGER_LEVEL = "error"
$env:STREAMLIT_CLIENT_TOOLBAR_MODE = "minimal"

# Disable telemetry and usage stats
$env:STREAMLIT_BROWSER_GATHERUSAGESTATS = "False"

Write-Host "Starting Health Coach AI..." -ForegroundColor Green
Write-Host "App will be available at: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

python -m streamlit run main.py
