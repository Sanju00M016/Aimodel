import time
import json
import logging
from flask import Flask, request, jsonify
from qa_module import QAModule
from summarize_module import Summarizer
from keywords_module import KeywordExtractor
from text_generation_module import TextGenerator
from t5_fine_tuning_module import T5TextGenerator

app = Flask(__name__)
qa_model = QAModule()
summarizer = Summarizer()
keyword_extractor = KeywordExtractor()
text_generator = TextGenerator()
t5_generator = T5TextGenerator()
t5_text_generator = T5TextGenerator()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/qa', methods=['POST'])
def answer_question_route():
    start_time = time.time()
    data = request.get_json()
    question = data.get('question')
    context = data.get('context')
    logging.info(f"Received QA request: Question='{question}', Context='{context[:50]}...'")
    if question and context:
        answer, error = qa_model.answer_question(question, context)
        latency = time.time() - start_time
        if answer:
            logging.info(f"QA response: Answer='{answer}', Latency={latency:.4f}s")
            return jsonify({'answer': answer, 'latency': latency})
        else:
            logging.error(f"QA error: {error}")
            return jsonify({'error': error}), 500
    else:
        logging.error("QA request missing question or context")
        return jsonify({'error': 'Missing question or context'}), 400

@app.route('/summarize', methods=['POST'])
def summarize_text_route():
    start_time = time.time()
    data = request.get_json()
    text = data.get('text')


    logging.info(f"Received summarize request: Text='{text[:50]}...'")
    if text:
        summary, error = summarizer.summarize_text(text)
        latency = time.time() - start_time
        if summary:
            logging.info(f"Summarize response: Summary='{summary}', Latency={latency:.4f}s")
            return jsonify({'summary': summary, 'latency': latency})
        else:
            logging.error(f"Summarize error: {error}")
            return jsonify({'error': error}), 500
    else:
        logging.error("Summarize request missing text")
        return jsonify({'error': 'Missing text'}), 400

@app.route('/keywords', methods=['POST'])
def extract_keywords_route():
    start_time = time.time()
    data = request.get_json()
    text = data.get('text')
    
    logging.info(f"Received keywords request: Text='{text[:50]}...'")
    if text:
        keywords, error = keyword_extractor.extract_keywords(text)  # Capture both return values
        latency = time.time() - start_time
        logging.info(f"Keywords response: Keywords='{keywords}', Latency={latency:.4f}s")
        return jsonify({'keywords': keywords, 'latency': latency})  # Only jsonify keywords
    else:
        logging.error("Keywords request missing text")
        return jsonify({'error': 'Missing text'}), 400

@app.route('/generate_question', methods=['POST'])
def generate_question_route():
    start_time = time.time()
    data = request.get_json()
    topic = data.get('topic')
    logging.info(f"Received generate question request: Topic='{topic}'")
    if topic:
        question, error = text_generator.generate_question(topic)
        latency = time.time() - start_time
        if question:
            logging.info(f"Generate question response: Question='{question}', Latency={latency:.4f}s")
            return jsonify({'generated_question': question, 'latency': latency})
        else:
            logging.error(f"Generate question error: {error}")
            return jsonify({'error': error}), 500
    else:
        logging.error("Generate question request missing topic")
        return jsonify({'error': 'Missing topic'}), 400
    
@app.route('/generate_t5', methods=['POST'])  # New route for T5
def generate_t5_route():
    start_time = time.time()
    data = request.get_json()
    input_text = data.get('input')
    logging.info(f"Received generate_t5 request: Input='{input_text[:50]}...'")

    if input_text:
        try:
            generated_text = t5_text_generator.generate_text(input_text)
            latency = time.time() - start_time
            logging.info(f"Generate_t5 response: Output='{generated_text}', Latency={latency:.4f}s")
            return jsonify({'output': generated_text, 'latency': latency})
        except Exception as e:
            logging.error(f"Error during T5 generation: {e}")
            return jsonify({'error': f'T5 Generation error: {e}'}), 500
    else:
        logging.error("Generate_t5 request missing input")
        return jsonify({'error': 'Missing input'}), 400

if __name__ == '__main__':
    app.run(debug=True)