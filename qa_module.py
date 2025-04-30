import os
import openai
from dotenv import load_dotenv
import logging

load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QAModule:
    def __init__(self):
        pass

    def answer_question(self, question, context):
        if not openai.api_key:
            logging.error("OPENAI_API_KEY not found in environment.")
            return None, "OpenAI API key not configured"
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
                ]
            )
            answer = response.choices[0].message.content
            return answer, None
        except openai.error.OpenAIError as e:
            logging.error(f"OpenAI API error: {e}")
            return None, f"OpenAI API error: {e}"
    

# from transformers import pipeline
# from datasets import load_dataset

# class QuestionAnsweringModel:
#     def __init__(self, model_name="bert-large-uncased", dataset_name="openbookqa"):
#         # OpenBookQA is a multiple-choice QA dataset. We might need a different
#         # model architecture or adapt the task. For now, let's stick with a
#         # general-purpose model and see how we can use the data.
#         self.pipeline = pipeline("text-classification", model=model_name)
#         self.openbookqa_dataset = load_dataset(dataset_name) # Loads train, validation, and test splits

#     def answer_question(self, question, choices):
#         """
#         This function will take a question and a list of choices and use the
#         text-classification pipeline to predict the most likely correct answer.
#         We will need to format the input appropriately for the model.
#         """
#         candidate_answers = [f"{question} {choice}" for choice in choices]
#         results = self.pipeline(candidate_answers)
#         # Assuming the model outputs probabilities for each class (choice)
#         # We need to find the choice with the highest probability.
#         best_choice_index = results.index(max(results, key=lambda x: x['score']))
#         return choices[best_choice_index]

#     def get_example_from_dataset(self, split="train", index=0):
#         if split in self.openbookqa_dataset and index < len(self.openbookqa_dataset[split]):
#             return self.openbookqa_dataset[split][index]
#         else:
#             return None

# if __name__ == '__main__':
#     qa_model = QuestionAnsweringModel()
#     example = qa_model.get_example_from_dataset(split="train", index=0)
#     if example:
#         print("Example from OpenBookQA dataset:")
#         print(f"Question: {example['question']}")
#         print(f"Choices: {example['choices']['text']}")
#         print(f"Correct Answer Index: {example['answerKey']}")

#         # Let's try to answer this question (note: this is a simplified approach)
#         question = example['question']
#         choices = example['choices']['text']
#         predicted_answer = qa_model.answer_question(question, choices)
#         print(f"\nPredicted Answer (using text-classification on choices): {predicted_answer}")