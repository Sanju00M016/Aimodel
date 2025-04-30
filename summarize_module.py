
import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Summarizer:
    def __init__(self):
        pass

    def summarize_text(self, text):
        if not openai.api_key:
            logging.error("OPENAI_API_KEY not found in environment.")
            return None, "OpenAI API key not configured"
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides concise summaries of text."},
                    {"role": "user", "content": f"Summarize the following text: {text}"}
                ]
            )
            summary = response.choices[0].message.content
            return summary, None
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return None, f"OpenAI API error: {e}"

# from transformers import pipeline
# from datasets import load_dataset

# class SummarizationModel:
#     def __init__(self, model_name="facebook/bart-large-cnn", dataset_name="cnn_dailymail"):
#         self.pipeline = pipeline("summarization", model=model_name)
#         self.summarization_dataset = load_dataset(dataset_name, '3.0.0', split="train[:1000]") # Load a small subset for now

#     def summarize_text(self, text):
#         summary = self.pipeline(text, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
#         return summary

#     def get_example_from_dataset(self, index=0):
#         if index < len(self.summarization_dataset):
#             return self.summarization_dataset[index]
#         else:
#             return None

# if __name__ == '__main__':
#     summarizer = SummarizationModel()
#     example = summarizer.get_example_from_dataset(index=0)
#     if example:
#         print("Example from CNN/DailyMail Dataset:")
#         print(f"Article: {example['article'][:200]}...")
#         print(f"Summary: {example['highlights']}")
#         text_to_summarize = example['article']
#         summary = summarizer.summarize_text(text_to_summarize)
#         print(f"\nGenerated Summary: {summary}")