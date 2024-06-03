from graph_utils.search import MidSearch
from graph_utils.knowledge_graph import KnowledgeGraph, Embedding


emb = Embedding()
kg = KnowledgeGraph("neo4j://localhost", ("neo4j", "sjz20030616"), emb)
a = MidSearch(kg)

score, text, cat = a.search('模糊搜索', types=['all'])
print(score, text, cat, kg.node_type[cat])
