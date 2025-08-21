from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from typing import Any
import logging
from telugu_nlp_processor import TeluguNLPProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Telugu NLP processor
nlp_processor = TeluguNLPProcessor()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/api/generate-qa', methods=['POST'])
def generate_qa():
    """Generate questions and answers from Telugu paragraph"""
    try:
        data: Any = request.get_json()
        paragraph = data.get('paragraph', '')
        num_questions = data.get('num_questions', 5)
        difficulty = data.get('difficulty', 'mixed')
        
        if not paragraph:
            return jsonify({'error': 'Paragraph is required'}), 400
        
        # Generate Q&A pairs
        qa_pairs = nlp_processor.generate_qa_pairs(paragraph, num_questions, difficulty)
        
        # Get question statistics
        statistics = nlp_processor.get_question_statistics(qa_pairs)
        
        return jsonify({
            'success': True,
            'qa_pairs': qa_pairs,
            'total_questions': len(qa_pairs),
            'statistics': statistics
        })
        
    except Exception as e:
        logger.error(f"Error generating Q&A: {str(e)}")
        return jsonify({'error': 'Failed to generate Q&A'}), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'telugu-qa-generator'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
