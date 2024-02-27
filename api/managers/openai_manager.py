import logging
import os

from openai import APIError, OpenAI, RateLimitError, Timeout
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential


class OpenAIManager:
    """Interact with OpenAI"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), organization=os.getenv("OPENAI_ORG_ID"))

    @retry(wait=wait_random_exponential(multiplier=1, max=40),
           stop=stop_after_attempt(3),
           retry=(retry_if_exception_type(RateLimitError) |
                  retry_if_exception_type(APIError)
                  )
           )
    def call_completion_with_retry(self, model, messages, tools=None, tool_choice=None):
        """
        Call the openai api with the given messages
        If the call fails, retry with exponential backoff.
        :param model: the model to use
        :param messages: messages to send to completion
        :param tools: optional param for functions to call
        :param tool_choice: optional param for forcing a function to be called
        """
        try:
            completion = self.client.chat.completions.create(model=model,
                                                             messages=messages,
                                                             tools=tools,
                                                             tool_choice=tool_choice)
        except (RateLimitError, APIError, Timeout) as e:
            logging.info(f"retrying completion with {messages}, retryable error {e}")
            raise e
        except Exception as e:
            logging.error(f"something went wrong with messages {messages}, error: {e}")
            return None
        return completion
