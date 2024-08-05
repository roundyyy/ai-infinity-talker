@echo off

:: Check if Python is installed

echo Checking if Python is installed...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. 
	echo Please install Python https://www.microsoft.com/store/productId/9NCVDN91XZQP?ocid=pdpshare
	echo CTRL+Click to follow link
	pause >nul
	exit /b
    
    
)
echo Python is already installed.

:: Check if Ollama is installed
echo Checking if Ollama is installed...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo Ollama is not installed. Proceeding with installation...

    :: Download Ollama installer using PowerShell
    echo Downloading Ollama installer...
    powershell -Command "Invoke-WebRequest -Uri 'https://ollama.com/download/OllamaSetup.exe' -OutFile 'OllamaSetup.exe'"

    :: Run the installer
    echo Running Ollama installer...
    start /wait OllamaSetup.exe

    :: Wait for user confirmation
    echo Installation is complete. Please press any key to continue...
    pause >nul

    echo Ollama installation complete.
) else (
    echo Ollama is already installed.
)

:: Check if the Ollama model is already installed
echo Checking if the Ollama model is installed...
ollama list | find "mannix/llama3.1-8b-abliterated:latest" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing the Ollama model...
    ollama pull mannix/llama3.1-8b-abliterated:latest
) else (
    echo Ollama model is already installed.
)

:: Create and activate a virtual environment if not already created
if not exist "venv\Scripts\activate" (
    echo Setting up virtual environment...
    python -m venv venv
)
call venv\Scripts\activate

:: Check if CUDA PyTorch is installed
echo Checking if CUDA PyTorch is installed...
pip show torch >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing CUDA PyTorch...
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
) else (
    echo CUDA PyTorch is already installed.
)

:: Check if real-time TTS is installed
echo Checking if real-time TTS is installed...
pip show realtimetts >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing real-time TTS...
    pip install realtimetts[coqui]
) else (
    echo Real-time TTS is already installed.
)

:: Install additional requirements if not already installed
echo Checking additional requirements...
pip install -r requirements.txt

:: Run the Python script
echo Running the script...
python infinitytalker.py

if %errorlevel% neq 0 (
    echo There was an error running the script.
    echo Please check the error messages above and try again.
    pause
    exit /b
)

echo Script finished successfully.
pause
