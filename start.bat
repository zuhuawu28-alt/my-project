@echo off
cd /d "%~dp0"
echo ================================
echo  Cii.中国 服务器启动中...
echo ================================
echo.
echo 前台: http://localhost:5099
echo 后台: http://localhost:5099/admin
echo.
echo 关闭此窗口即可停止服务器
echo ================================
python server.py
pause
