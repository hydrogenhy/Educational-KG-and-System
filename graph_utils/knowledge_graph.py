import pandas as pd
import numpy as np
from transformers import BertTokenizer, BertModel
import torch
import pickle
from neo4j import GraphDatabase

from .utils import *


class Embedding:
    def __init__(self, model_name='bert-base-chinese'):
        self.model_name = model_name
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()
    
    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
        return embeddings


class KnowledgeGraph:
    def __init__(
            self,
            URI,
            AUTH,
            embedding_model: Embedding,
            data_path='./data'
            ):
        self.data_path = data_path
        with open(f"{data_path}/type/node_type.pkl", 'rb') as f:
            self.node_type: list = pickle.load(f)
        with open(f"{data_path}/type/edge_type.pkl", 'rb') as f:
            self.edge_type: list = pickle.load(f)
        self.URI = URI
        self.AUTH = AUTH
        self.embeddings = {}
        for t in self.node_type:
            with open(f"{data_path}/embedding/embedding_{t}.pkl", 'rb') as f:
                self.embeddings[t] = pickle.load(f)
        self.embedding_model = embedding_model

    def add_triple(self, triple):
        """
        Add triple not strictly.
        """
        if triple[0][0] not in self.node_type:
            self.add_node_type(triple[0][0])
        if triple[1][0] not in self.node_type:
            self.add_node_type(triple[1][0])
        if triple[2][0] not in self.edge_type:
            self.add_edge_type(triple[2][0])
        self.add_triple_strict(triple)
    
    def add_triple_fuzzy(self, triple):
        ans = ""
        triple[0][1] = self.process_node_fuzzy(triple[0])
        triple[1][1] = self.process_node_fuzzy(triple[1])
        if triple[2][0] not in self.edge_type:
            self.add_edge_type(triple[2][0])
        print(f"Will add {triple}. Please check whether this triple is what you expect.")
        ans += f"已添加三元组 {triple}."
        self.add_triple_strict(triple)
        return ans

    def add_triple_strict(self, triple):
        """
        ONLY add if it is in the graph.
        triple:
            [0]: start node
            [1]: end node
            [2]: relation
        """
        assert triple[0][0] in self.node_type, f"You should add type: {triple[0][0]} in self.node_type first!"
        assert triple[1][0] in self.node_type, f"You should add type: {triple[1][0]} in self.node_type first!"
        assert triple[2][0] in self.edge_type, f"You should add type: {triple[2][0]} in self.edge_type first!"
        self.execute_query(
            f"MERGE (a:{triple[0][0]} {{title:'{triple[0][1]}'}}) \
            MERGE (b:{triple[1][0]} {{title:'{triple[1][1]}'}}) \
            MERGE (a)-[:{triple[2][0]}]->(b)"
        )
        self.add_node_embedding(triple[0])
        self.add_node_embedding(triple[1])

    def fuzzy_in(self, node, threshold=0.95):
        # has the original node
        if node[1] in self.embeddings[node[0]]:
            return True, node[1]
        
        emb = self.embedding_model.get_embedding(node[1])
        node_similar_name = None
        max_score = -1

        for exist_node_name, exist_emb in self.embeddings[node[0]].items():
            score = cos_cal(emb, exist_emb)
            if score > max_score:
                max_score = score
                node_similar_name = exist_node_name
        
        if max_score > threshold:
            return True, node_similar_name
        return False, None
    
    def process_node_fuzzy(self, node):
        """
        Process input node in a fuzzy way.
        Inputs:
        - node: [type, name]
        Outputs:
        - process node name (similar node or itself)
        """
        # add node type if not exist
        if node[0] not in self.node_type:
            self.add_node_type(node[0])             # it will return `False` in `fuzzy_in`
        inside, similar_node_name = self.fuzzy_in(node)
        if inside:
            return similar_node_name
        # if not inside, return original input node name (add later)
        return node[1]

    def add_node(self, node):
        if node[0] not in self.node_type:
            self.add_node_type(node[0])
        self.execute_query(
            f"MERGE (a:{node[0]}) {{title:'{node[1]}'}}"
        )
        self.add_node_embedding(node)
    
    def add_node_embedding(self, node):
        if node[1] not in self.embeddings[node[0]]:
            emb = self.get_embedding(node[1])
            self.embeddings[node[0]][node[1]] = emb 

    def execute_query(self, msg):
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()
            try:
                records, summarys, keys = driver.execute_query(msg)
                print("Execute successful!")
            except:
                raise ValueError("Unsucessful execution.")

    def query(self, msg, mod):
        res = []
        with GraphDatabase.driver(self.URI, auth=self.AUTH) as driver:
            driver.verify_connectivity()
            try:
                records, summarys, keys = driver.execute_query(msg)
                # print("Execute successful!")
                for record in records:
                    n, r, m = record['n'], record['r'], record['m']
                    # print(f"{n['title']} -> {r.type} -> {m['title']}")
                    if mod == 1:
                        res.append(n['title'])
                    elif mod == 2:
                        res.append(m['title'])
            except:
                raise ValueError("Unsucessful execution.")
        return res
    
    def query_course(self, course):
        template1 = f"MATCH (n:course)-[r]->(m) WHERE n.title = '{course}' RETURN n,r,m"
        queue = self.query(template1, 2)
        dic = {}
        ans = ""
        if len(queue) > 5:
            ans += "当前课程子章节过多，仅显示前五个章节。\n"
        for q in queue[:5]:
            template2 = f"MATCH (n:chapter)-[r]->(m) WHERE n.title = '{q}' RETURN n,r,m"
            res = self.query(template2, 2)
            dic[q] = res
        ans += print_course_outline(dic, course)
        return ans
            

    def add_node_type(self, node_type):
        if node_type in self.node_type:
            raise ValueError(f"type {node_type} already exists. Pass it.")
        else:
            self.node_type.append(node_type)
            self.embeddings[node_type] = {}
    
    def remove_node_type(self, node_type):
        if node_type not in self.node_type:
            raise ValueError(f"type {node_type} not exists. Pass it.")
        else:
            self.node_type.remove(node_type)
            self.embeddings.pop(node_type)
            self.execute_query(f"MATCH (n:{node_type}) DETACH DELETE n")
        
    def add_edge_type(self, edge_type):
        if edge_type in self.edge_type:
            raise ValueError(f"type {edge_type} already exists. Pass it.")
        else:
            self.edge_type.append(edge_type)

    def remove_edge_type(self, edge_type):
            if edge_type not in self.edge_type:
                raise ValueError(f"type {edge_type} not exists. Pass it.")
            else:
                self.edge_type.remove(edge_type)
                self.execute_query(f"MATCH (n)-[r:{edge_type}]-(m) DETACH DELETE r")
    
    def get_embedding(self, text):
        return self.embedding_model.get_embedding(text)
    
    def save(self):
        with open(f"{self.data_path}/type/node_type.pkl", 'wb') as f:
            pickle.dump(self.node_type, f)
        with open(f"{self.data_path}/type/edge_type.pkl", 'wb') as f:
            pickle.dump(self.edge_type, f)
        
        for t in self.node_type:
            with open(f"{self.data_path}/embedding/embedding_{t}.pkl", 'wb') as f:
                pickle.dump(self.embeddings[t], f)
        