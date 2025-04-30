import os
import openai
from dotenv import load_dotenv
import logging
import re

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class KeywordExtractor:
    def __init__(self):
        pass

    def extract_keywords(self, text):
        if not openai.api_key:
            logging.error("OPENAI_API_KEY not found in environment.")
            return None, "OpenAI API key not configured"
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts key keywords or phrases from the given text. Return each keyword on a new line."},
                    {"role": "user", "content": f"Extract keywords from the following text: {text}"}
                ]
            )
            keywords_str = response.choices[0].message.content
            # Split the response by newline to get individual keyword lines
            keyword_lines = keywords_str.split('\n')
            cleaned_keywords = []
            for line in keyword_lines:
                keyword = line.strip()
                if keyword and keyword.lower() != 'keywords':  # Ignore empty lines and "Keywords" title
                    cleaned_keywords.append(keyword.strip())
            return cleaned_keywords, None
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return None, f"OpenAI API error: {e}"