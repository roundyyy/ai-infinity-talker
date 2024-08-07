# AI Infinity Talker

AI Infinity Talker is a desktop application that uses AI to generate endless text based on an initial input and user-defined style options. The generated text is then converted to audio, providing a continuous talking experience. It's like having a chatty friend who never runs out of things to say!

## Demo Video

Watch the demo video on YouTube:

[![AI Infinite Talker Demo YouTube](https://img.youtube.com/vi/EmUcYtgWkIY/hqdefault.jpg)](https://youtu.be/EmUcYtgWkIY)

## Features

- **Infinity Text Generation**: Generates continuous text based on initial input and predefined styles.
- **Text-to-Speech**: Converts the generated text to audio using the Coqui TTS engine.
- **Style Options**: Allows users to customize the style of the generated text with various options like sarcasm, humor, scientific, philosophical, etc.
- **Real-time Updates**: The application continuously updates the text and audio in real-time.

## Installation

### Steps

1. **Install Prerequisites**:
    - **NVIDIA GPU**: Required. A 8GB GPU should work, but a 12GB GPU is recommended for best results. Trust us, you don't want your AI buddy running out of breath!
    - **Ollama**: Must be installed manually. [Ollama Installation Guide](https://ollama.com/download/windows)
    - **FFmpeg**: Must be installed manually. [FFmpeg Installation Guide](https://phoenixnap.com/kb/ffmpeg-windows)

2. **Download the Project** (for beginners):
    - Click the green "Code" button and select "Download ZIP".

3. **Unpack the ZIP File**:
    - Locate the downloaded ZIP file on your computer (usually in your Downloads folder).
    - Right-click the file and select "Extract All..." or "Unzip Here".

4. **Run the Installation Script**:
    - Open the extracted folder.
    - Double-click `start.bat`. This will automatically install all required dependencies and start the application.

## Usage

1. **Start the Application**:
    - On Windows:
        Double-click `start.bat`. This will launch the application.

2. **Enter Text**:
    - Input your initial text in the "Enter Text" area.

3. **Select Style Options**:
    - Choose the desired style options from the right panel. Whether you want it to be sarcastic, humorous, or philosophically deep, we've got you covered!

4. **Start Generation**:
    - Click the "Start" button to begin generating and playing the text. Watch as your AI friend comes to life!

5. **Stop Generation**:
    - Click the "Stop" button to stop the generation and audio playback. Even AI needs a break sometimes.

## Credits

This project uses the following libraries, tools, and models:

- [ttkbootstrap](https://github.com/israel-dryer/ttkbootstrap)
- [httpx](https://www.python-httpx.org/)
- [nltk](https://www.nltk.org/)
- [sounddevice](https://python-sounddevice.readthedocs.io/)
- [RealtimeTTS](https://github.com/KoljaB/RealtimeTTS)
- [Coqui XTTS-v2](https://huggingface.co/coqui/XTTS-v2)
- [Meta-Llama-3.1-8B-Instruct-abliterated](https://huggingface.co/mlabonne/Meta-Llama-3.1-8B-Instruct-abliterated)

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
