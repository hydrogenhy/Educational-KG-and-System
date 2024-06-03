from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import json


class QueryLLM:
    def __init__(self, device, model_name='Qwen/Qwen-7B-Chat'):
        # Note: The default behavior now has injection attack prevention off.
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True).eval()
        self.model.to(device)
    
    def query_llm(self, prompt, history=None):
        response, new_history = self.model.chat(self.tokenizer, prompt, history=history)
        try:
            dictionary = json.loads(response)
        except:
            print(f"LLM provided a wrong answer. Try again.\n Wrong Answer: {response}")
            dictionary = None
        return dictionary, new_history
