import gradio as gr
import requests
import json
import re

# Base URL of your Flask API
BASE_URL = "http://127.0.0.1:5000"  # Adjust port if needed

def ask_question(question, context):
    payload = json.dumps({"question": question, "context": context})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/qa", data=payload, headers=headers)
    if response.ok:
        return response.json().get("answer", "Error: No answer received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def summarize_text(text):
    payload = json.dumps({"text": text})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/summarize", data=payload, headers=headers)
    if response.ok:
        return response.json().get("summary", "Error: No summary received.")
    else:
        return f"Error: {response.status_code} - {response.text}"

def extract_keywords(text):
    payload = json.dumps({"text": text})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/keywords", data=payload, headers=headers)
    if response.ok:
        keywords_data = response.json().get("keywords", [])
        print(f"Frontend - Received keywords_data: {keywords_data}")
        if isinstance(keywords_data, list) and all(isinstance(item, str) for item in keywords_data):
            return ", ".join(keywords_data) or "Error: No keywords received."
        else:
            return f"Error: Unexpected keyword format received: {keywords_data}"
    else:
        return f"Error: {response.status_code} - {response.text}"

def generate_question(topic):
    payload = json.dumps({"topic": topic})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(f"{BASE_URL}/generate_question", data=payload, headers=headers)
    if response.ok:
        return response.json().get("generated_question", "Error: No question generated.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# def generate_text_t5(input_text):
#     payload = json.dumps({"input": input_text})
#     headers = {'Content-Type': 'application/json'}
#     response = requests.post(f"{BASE_URL}/generate_t5", data=payload, headers=headers)
#     if response.ok:
#         return response.json().get("output", "Error: No output received.")
#     else:
#         return f"Error: {response.status_code} - {response.text}"

# with gr.Blocks() as demo:
#     gr.Markdown("# EDUASSIST")

    with gr.Tab("Question Answering"):
        question_input = gr.Textbox(label="Question")
        context_input = gr.Textbox(label="Context")
        qa_button = gr.Button("Ask")
        answer_output = gr.Textbox(label="Answer")
        qa_button.click(ask_question, inputs=[question_input, context_input], outputs=answer_output)

    with gr.Tab("Summarize Text"):
        summary_input = gr.Textbox(label="Text to Summarize")
        summary_button = gr.Button("Summarize")
        summary_output = gr.Textbox(label="Summary")
        summary_button.click(summarize_text, inputs=summary_input, outputs=summary_output)

    with gr.Tab("Extract Keywords"):
        keywords_input = gr.Textbox(label="Text for Keywords")
        keywords_button = gr.Button("Extract")
        keywords_output = gr.Textbox(label="Keywords")
        keywords_button.click(extract_keywords, inputs=keywords_input, outputs=keywords_output)

    with gr.Tab("Generate Question"):
        topic_input = gr.Textbox(label="Topic")
        generate_button = gr.Button("Generate")
        question_output = gr.Textbox(label="Generated Question")
        generate_button.click(generate_question, inputs=topic_input, outputs=question_output)

    # with gr.Tab("Cloud Computing Model"):
    #     t5_input = gr.Textbox(label="Enter Text to Generate")
    #     t5_generate_button = gr.Button("Generate Text (T5)")
    #     t5_output = gr.Textbox(label="Generated Text (T5)")
    #     t5_generate_button.click(generate_text_t5, inputs=t5_input, outputs=t5_output)
    

if __name__ == "__main__":
    demo.launch()
