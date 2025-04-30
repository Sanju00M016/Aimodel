
import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TextGenerator:
    def __init__(self):
        pass

    def generate_question(self, topic, max_length=50):
        if not openai.api_key:
            logging.error("OPENAI_API_KEY not found in environment.")
            return None, "OpenAI API key not configured"
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that generates relevant questions based on a given topic."},
                    {"role": "user", "content": f"Generate a question about the topic: {topic}"}
                ]
            )
            question = response.choices[0].message.content
            return question, None
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return None, f"OpenAI API error: {e}"

# from transformers import pipeline
# from datasets import load_dataset

# class TextGenerator:
#     def __init__(self, model_name="allenai/t5-small-squad2-question-generation", dataset_name=None):
#         self.pipeline = pipeline("text2text-generation", model=model_name)
#         self.generation_dataset = None # We might not need to load a dataset in the constructor for just inference

#     def generate_question(self, topic, max_length=50):
#         prompt = f"generate question: {topic}"
#         generated_text = self.pipeline(prompt, max_length=max_length, num_return_sequences=1)[0]['generated_text']
#         return generated_text.strip()

#     def get_example_from_dataset(self, index=0):
#         # We might not be directly using the dataset in this version
#         return None

# if __name__ == '__main__':
#     text_generator = TextGenerator()
#     topic = "Photosynthesis"
#     question = text_generator.generate_question(topic)
#     print(f"Topic: {topic}")
#     print(f"Generated Question: {question}")