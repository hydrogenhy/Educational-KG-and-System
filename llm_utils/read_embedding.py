import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
import pickle


with open('chapters_embedding.pkl', 'rb') as f:
    chapters_embedding = pickle.load(f)

print(chapters_embedding)
