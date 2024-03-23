import torch

from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.utils import logging

logging.get_logger("transformers").setLevel(logging.ERROR)
# attention from ninja
# flashattention2
# quantize

# models
# model_name = "microsoft/DialoGPT-large"
# model_name = "microsoft/DialoGPT-medium"
# model_name = "microsoft/DialoGPT-small"
# model_name = "HuggingFaceH4/zephyr-7b-beta" # Needs more RAM
# model_name = 'meta-llama/Llama-2-70b-chat-hf' # Requires authorization token
# model_name = "deepset/roberta-base-squad2" # For QA only

token = None

# Implmentation can be done via pipeline(an interface for applying standard configurations rapidly) 
# or 
# through the Auto Classes
chat_template = [
    {
        'role' : 'system',
        'content' : 'You provide specific answers with some occasional humour.'
    },
    {
        'role' : 'user',
        'content' : 'I am interested in rapidly learning about programming languages.'
    },
]


# The section below is the default code from hugging face. Not in use as there is a greater latency than the other method.
# pipe = pipeline("conversational", model="HuggingFaceH4/zephyr-7b-beta", torch_dtype=torch.bfloat16, device="cpu", max_new_tokens=20)
# prompt = pipe.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
# outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
# print(outputs[0]["generated_text"])

# This is a piece of self developed code that is low perfomring than the logic implemented.
# Conversation type can only be utilized when pipeline type is "conversational"
# while True:
#     conversation = Conversation(input("User : "))
#     resp = pipe(conversation)
#     print(resp)

# model_config = AutoConfig.from_pretrained(model_name, use_auth_token=token) # This is required for custom configuration for non-standardized models

class ConversationalAgent:
    def __init__(self, model_name : str, token: str | None = None, use_history : bool = False, use_beam : bool = False):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, padding_side='left', use_auth_token=token)# Usage of fast may reduce accuracy
        self.model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=token)
        self.tokenizer.apply_chat_template(chat_template, tokenize=False)
        self.history_enabled = use_history
        self.beam_selector = use_beam
        
        # Chat history elements
        self.chat_history = None
        self.chat_flag = False

    def eval_resp(self, message : str) -> str:
        # encode the input and add end of string token
        input_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors="pt", max_length=100, truncation=True)

        bot_input_ids = None
        if self.chat_history :
            bot_input_ids = torch.cat([chat_history_ids, input_ids], dim=-1) if self.chat_flag > 0 else input_ids
            self.chat_flag = 1
        else :
            bot_input_ids = input_ids
        
        chat_history_ids : list = []
        if self.beam_selector :
            chat_history_ids = self.model.generate(
                bot_input_ids,
                do_sample=True,
                temperature=0.75,
                top_k = 25,
                epsilon_cutoff=0.5,
                length_penalty=0.2,
                num_beams=4,
                remove_invalid_values = True,
                early_stopping= True,
                # num_return_sequences=1,
                # no_repeat_ngram_size=1,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id
            )
        else :
            chat_history_ids = self.model.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        return self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

def serve_chat(**kwargs):
    '''Enable conversation over CLI. Useful for testing'''
    print("Loading...", end='')
    agent = ConversationalAgent("microsoft/DialoGPT-large", use_history=True, use_beam=True)
    print('\r          ', end='')
    while True:
        print(f"Agent : {agent.eval_resp(input("\rUser : "))}")

if __name__ == "__main__":
    serve_chat()