from llm_utils.query import QueryLLM
from llm_utils.prompt_manager import extract_prompt


"""
All prompts are saved in `prompt_manager.py` for better arrangment.
You may use `str.format` method to replace the obtain items.
"""

msg = "机器学习这门课程中讲了蒙特卡洛方法。"
prompt = extract_prompt.format(msg=msg)

query_llm = QueryLLM(device='cuda:1')
dictionary, history = query_llm.query_llm(prompt)
print(dictionary)
