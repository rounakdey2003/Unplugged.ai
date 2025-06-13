# **UNplugged**.ai

**Elevate Your Workflow with Standalone AI.**

A powerful, offline AI application built with Streamlit that provides comprehensive AI capabilities without requiring internet connectivity for core functionality. Interact with local AI models through multiple interfaces including chat, document analysis, image processing, and voice commands.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.0+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### 🤖 **Multi-Modal AI Interaction**
- **Chat Interface**: Direct conversation with AI models
- **Document Analysis**: PDF and DOCX file processing and Q&A
- **Text Processing**: Upload text files or input manual text for analysis
- **Image Analysis**: Vision capabilities for image description and analysis
- **Voice Commands**: Speech-to-text and text-to-speech functionality

### 🎯 **Sentiment Analysis**
- Real-time emotion detection from user inputs
- Confidence scoring with visual probability distributions
- Emoji-based emotion representation
- Support for multiple emotions: anger, disgust, fear, happy, joy, neutral, sad, shame, surprise

### 🔧 **Model Management**
- Support for 17+ popular AI models including:
  - **DeepSeek-R1**: 1.5b, 7b, 8b, 14b, 32b, 70b, 671b
  - **Llama 3.3**: 70b
  - **Phi4**: 14b
  - **Llama 3.2**: 1b, 3b (with vision variants: 11b, 90b)
  - **Llama 3.1**: 8b, 70b, 405b
  - **Qwen 2.5**: 0.5b to 72b (including coder variants)
  - **Gemma**: 2b, 7b
  - **Mistral**: 7b
  - And many more...

### 🎙️ **Advanced Voice Features**
- Real-time speech recognition
- Customizable voice speed (100-300 WPM)
- Continuous conversation mode
- Hands-free interaction

### 📁 **Document Processing**
- **PDF Support**: Full text extraction and inline preview
- **DOCX Support**: Microsoft Word document processing
- **Text Files**: Plain text file upload and manual text input
- Context-aware questioning based on document content

### 🖼️ **Image Analysis**
- Support for PNG, JPG, JPEG formats
- Base64 encoding for model compatibility
- Image description and object detection
- Mood and caption generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com) installed on your system

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rounakdey2003/unplugged-ai.git
   cd unplugged-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install and setup Ollama**
   - Visit [Ollama.com](https://ollama.com)
   - Download and install Ollama for your operating system
   - Pull your first model:
     ```bash
     ollama pull llama3.2:3b
     ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   - Open your browser and navigate to `http://localhost:8501`

## 📖 Usage Guide

### 🔧 Model Configuration

1. **Select Model Tab**: Choose from pre-configured models or enter a custom model name
2. **Model Variations**: Select the appropriate size variant for your hardware
3. **System Detect**: View currently available models on your system

### 🛠️ Model Management

Use the **Manage Model** tab to:
- **Pull**: Download new models
- **List**: View installed models
- **Remove**: Delete unused models
- **Start/Stop**: Control Ollama service
- **Show**: Display model information

### 💬 Chat Interface

- Use predefined example questions or type custom queries
- Real-time sentiment analysis on user inputs
- Animated response generation
- Response time tracking

### 📄 Document Analysis

#### PDF Processing
- Upload PDF files with inline preview
- Extract and analyze text content
- Ask questions about document content
- Example operations: summarize, explain, conclude

#### DOCX Processing
- Upload Microsoft Word documents
- Full text extraction and preview
- Context-aware Q&A
- Document analysis and summarization

#### Text Processing
- Upload .txt files or input text manually
- Combined text analysis from multiple sources
- Text summarization and explanation

### 🖼️ Image Analysis

- Upload images in PNG, JPG, or JPEG format
- Ask questions about image content
- Generate descriptions and captions
- Analyze mood and detect objects

### 🎙️ Voice Interaction

- **Start Listening**: Begin speech recognition
- **Continuous Mode**: Auto-restart listening after AI responses
- **Voice Speed Control**: Adjust TTS speed (100-300 WPM)
- **Real-time Status**: Visual feedback for listening/speaking states

## 🏗️ Architecture

### Project Structure
```
unplugged-ai/
├── app.py                 # Main application entry point
├── requirements.txt       # Python dependencies
├── image/
│   └── omenLogo.png      # Application logo
├── sentiment/
│   ├── emotion.py        # Sentiment analysis module
│   └── text_emotion.pkl  # Pre-trained emotion model
└── tabs/
    ├── chat_tab.py       # Chat interface
    ├── document_tab.py   # DOCX processing
    ├── image_tab.py      # Image analysis
    ├── pdf_tab.py        # PDF processing
    ├── text_tab.py       # Text processing
    └── voice_tab.py      # Voice commands
```

### Core Components

#### **Main Application (app.py)**
- Streamlit configuration and layout
- Session state management
- Model selection and validation
- Sentiment analysis integration
- Response generation and animation

#### **Tab Modules**
Each tab module handles specific functionality:
- File upload and processing
- Context preparation
- Example prompts
- User input handling

#### **Sentiment Analysis (sentiment/)**
- Pre-trained emotion classification model
- Real-time emotion detection
- Probability distribution visualization
- Emoji-based emotion representation

## 🔒 Privacy & Security

- **Offline Operation**: Core AI functionality works without internet
- **Local Processing**: All data processing happens on your machine
- **No Data Collection**: No user data is transmitted or stored externally
- **Model Privacy**: Use local models for sensitive content

## ⚡ Performance Tips

### Model Selection
- **Small Models (1b-3b)**: Fast responses, lower accuracy
- **Medium Models (7b-14b)**: Balanced performance
- **Large Models (70b+)**: High accuracy, requires more resources

### Hardware Recommendations
- **Minimum**: 8GB RAM, 4GB free disk space
- **Recommended**: 16GB+ RAM, SSD storage
- **Optimal**: 32GB+ RAM, GPU acceleration (if supported)

### Optimization
- Close unused applications to free memory
- Use smaller models for faster responses
- Monitor system resources during usage

## 🛠️ Dependencies

### Core Requirements
```
streamlit          # Web application framework
Pillow            # Image processing
ollama            # AI model integration
python-docx       # DOCX document processing
PyPDF2            # PDF document processing
pyttsx3           # Text-to-speech
SpeechRecognition # Speech-to-text
pandas            # Data manipulation
numpy             # Numerical computing
altair            # Data visualization
joblib            # Model serialization
scikit-learn      # Machine learning utilities
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.com) for providing the local AI model infrastructure
- [Streamlit](https://streamlit.io) for the excellent web application framework
- The open-source AI community for model development and distribution

## 📧 Contact

**Rounak Dey** - [@rounakdey2003](https://github.com/rounakdey2003)

Project Link: [https://github.com/rounakdey2003/unplugged-ai](https://github.com/rounakdey2003/unplugged-ai)

---

**UNplugged**🌈**.ai** - *Bringing AI capabilities to your local machine, no internet required.*
