import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
import pickle


def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # 取最后一个隐层的第一个token ([CLS] token) 的向量作为句子的embedding
    embeddings = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return embeddings



# 加载BERT模型和tokenizer
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
model.eval()  # 设置模型为评估模式

# 假设你的数据存储在一个CSV文件中
data = pd.read_csv('relation3.csv')

# 假设数据在A列和C列中
chapters = list(set(data['course1'].tolist()))
knowledges = list(set(data['course2'].tolist()))
chapters.extend(knowledges)
all = list(set(chapters))
all.remove(' ')
all.remove(np.nan)

all_embedding = {}

for text in all[1: ]:
    all_embedding[text] = get_embedding(text)

with open('course_embedding.pkl', 'wb') as f:
    pickle.dump(all_embedding, f)


