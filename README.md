# Telugu Q&A Generator - తెలుగు ప్రశ్నోత్తర జనరేటర్

A professional web application that generates questions and answers in Telugu from given Telugu paragraphs using Natural Language Processing (NLP) techniques.

## 🌟 Features

- **Telugu Language Support**: Full support for Telugu text input and output
- **NLP-Powered**: Uses advanced NLP techniques for intelligent Q&A generation
- **Professional UI**: Clean, responsive design with modern aesthetics
- **Real-time Processing**: Instant Q&A generation from paragraphs
- **Export Options**: Download generated Q&A in multiple formats
- **Mobile Responsive**: Works seamlessly on all devices

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Node.js (for frontend dependencies)
- Telugu NLP libraries

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/telugu-qa-generator.git
cd telugu-qa-generator
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **Transformers**: Hugging Face transformers for Telugu NLP
- **IndicNLP**: Indian language processing toolkit
- **spaCy**: Advanced NLP processing

### Frontend
- **HTML5/CSS3**: Modern web standards
- **JavaScript**: Interactive functionality
- **Bootstrap 5**: Responsive design framework
- **Font Awesome**: Icons and visual elements

## 📖 Usage

1. **Input Telugu Paragraph**: Paste or type your Telugu paragraph in the input area
2. **Generate Q&A**: Click the "Generate Questions" button
3. **Review Results**: View generated questions and answers in Telugu
4. **Export**: Download results as PDF, JSON, or plain text

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
MODEL_PATH=./models/telugu-qa
```

### Model Configuration
The application uses pre-trained Telugu language models. Ensure you have:
- Telugu BERT model
- Telugu tokenizer
- Telugu POS tagger

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/generate-qa` | POST | Generate Q&A from Telugu paragraph |
| `/api/health` | GET | Health check endpoint |
| `/api/export` | POST | Export generated Q&A |

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Hugging Face for transformer models
- IndicNLP team for Telugu language support
- Telugu Wikipedia for training data

## 📞 Support

For support, email support@telugu-qa-generator.com or join our Discord server.
