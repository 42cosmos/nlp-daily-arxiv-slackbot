import os
import json
import argparse
import datetime

import logging
import logging.config
from dotenv import load_dotenv

import openai

logger = logging.getLogger("openai").setLevel(logging.INFO)


class OpenAIGpt:
    def __init__(self):
        load_dotenv()
        self._api_key = os.getenv("OPENAI_API_KEY")
        assert self._api_key is not None, "Please set OPENAI_API_KEY in .env file"
        openai.api_key = self._api_key

    def request(self, request_data: list, model):
        request_data = [{"role": role, "content": content} for role, content in request_data]
        completion = openai.ChatCompletion.create(
            model=model,
            messages=request_data,
        )
        try:
            return completion['choices'][0]['message']['content']

        except openai.error.APIError as e:
            logger.exception(f"API Error: {e}")
            return "API Error"

        except openai.error.RateLimitError as e:
            logger.exception(f"Rate Limit Error: {e}")
            return "Rate Limit Error"

        except Exception as e:
            logger.exception(f"Error: {e}")
            return False

    def translate(self, text, model="gpt-3.5-turbo"):
        request_data = [("system",
                         "You are a helpful assistant that translates English to Korean. Translate the following English text to Korean"),
                        ("user", text)]
        return self.request(request_data=request_data, model=model)

    def summarise(self, text, model="gpt-3.5-turbo"):
        prompt = f'Please summarize the following text into 3 sentences and extract only the essentials: {text}'
        request_data = [("system", "You are a helpful research paper assistant that makes awesome summarised text."),
                        ("user", prompt)]
        return self.request(request_data=request_data, model=model)
