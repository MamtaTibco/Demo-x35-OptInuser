@echo off
uvicorn src.app:create_app --factory --reload
pause