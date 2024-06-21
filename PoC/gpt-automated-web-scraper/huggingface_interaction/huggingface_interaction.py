"""gpt_interaction.py: A module to interact with GPT models using the OpenAI API."""
import os
from typing import Optional

import warnings
warnings.warn("Warning...........Message")
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
from dotenv import load_dotenv

load_dotenv()


class HuggingfaceCausalLMInteraction:
    """A class to interact with Huggingface Causal LLM models"""

    _supported_chat_models = [
        "meta-llama/Meta-Llama-3-8B",
        "meta-llama/Meta-Llama-3-8B-Instruct"
    ]

    def __init__(
        self,
        model: str,
        max_tokens: int
    ):
        """
        Initialize the Huggingface CausalLM Interaction class with the required parameters.

        :param api_token: OpenAI API key, defaults to None
        :param model: GPT model to use, defaults to "gpt-4"
        :param temperature: Sampling temperature for the model, defaults to 1
        :param max_tokens: Maximum number of tokens for the model to generate, defaults to 4096
        :param top_p: Nucleus sampling parameter, defaults to 1
        """

        if model not in self._supported_chat_models:
            raise ValueError("Unsupported model")
        
        if "HUGGINGFACE_TOKEN" not in os.environ:
            warnings.warn("Huggingface token not found in environment variables. Set it to \"HUGGINGFACE_TOKEN\" variable")
        else:
            login(token=os.environ["HUGGINGFACE_TOKEN"])
            print("Login successful")
        

        self.model = AutoModelForCausalLM.from_pretrained(model)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.max_tokens = max_tokens

    def call(self, prompt: str) -> str:
        """
        Call the Huggingface model with the given prompt and return the response.

        :param prompt: The input prompt to send to the model
        :return: The generated text from the GPT model
        """
        inputToken = self.tokenizer(prompt, return_tensors="pt")
        output = self.model.generate(inputToken, max_length=self.max_tokens)

        return output
