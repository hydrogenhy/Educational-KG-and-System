import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
import pickle

from .knowledge_graph import KnowledgeGraph
from .utils import cos_cal


class MidSearch():
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.knowledge_graph = knowledge_graph
        self.node_type = knowledge_graph.node_type
        self.embeddings = knowledge_graph.embeddings

    def search(self, input_text, types=['all']):
        input_embedding = self.knowledge_graph.get_embedding(input_text)

        max_similarity = -1  # 初始化最大相似度
        most_similar_text = None
        category = 0
        
        for i, t in enumerate(self.knowledge_graph.node_type):
            if t in types or 'all' in types:
                for text, embedding in self.knowledge_graph.embeddings[t].items():
                    similarity = cos_cal(input_embedding, embedding)
                    if similarity > max_similarity:
                        max_similarity = similarity
                        most_similar_text = text
                        category = i
            
        return max_similarity, most_similar_text, category
