# Karen - AI Assistant

Karen is an AI assistant that provides various system utilities and features including battery monitoring, speech-to-text, text-to-speech, and more.

## Project Structure

```
├── SystemUtility/     # System monitoring utilities
├── music/            # Music-related functionality
├── app/              # Core application components
├── website/          # Web interface components
├── speechtotext/     # Speech recognition features
├── texttosppech/     # Text-to-speech capabilities
├── venv/             # Python virtual environment
├── requirements.txt  # Project dependencies
├── karen.py         # Main application file
└── explain.drawio.svg # System architecture diagram
```

## Features

- Battery monitoring and notifications
- Speech recognition
- Text-to-speech conversion
- Music playback
- Web automation
- System utilities

## System Architecture

![System Architecture](explain.drawio.svg)

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd karen
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- SpeechRecognition: For speech recognition capabilities
- PyAudio: For audio input/output
- colorama: For colored terminal output
- edge-tts: For text-to-speech conversion
- playsound: For audio playback
- webbrowser: For web automation
- pyautogui: For GUI automation
- pywhatkit: For additional web features
- psutil: For system monitoring
- plyer: For system notifications

## Usage

Run the main application:
```bash
python karen.py
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 