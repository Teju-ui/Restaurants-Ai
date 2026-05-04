@echo off
echo Starting DineScout Application Suite...

echo Starting Python Analytics API Server (Port 7000)...
start cmd /k "cd zomato_analyis && python api_server.py"

echo Starting Streamlit Business Dashboard (Port 8501)...
start cmd /k "cd zomato_analyis && python -m streamlit run app.py"

echo Starting Node.js Backend & Frontend Server (Port 5000)...
start cmd /k "cd DineScout\backend && node server.js"

echo =========================================================
echo All services have been launched in separate windows!
echo =========================================================
echo 1. Main Website: http://localhost:5000
echo 2. Business Dashboard: http://localhost:8501
echo =========================================================
pause
