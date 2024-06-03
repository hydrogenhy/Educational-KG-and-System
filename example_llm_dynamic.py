from llm_utils.query import QueryLLM
from graph_utils.knowledge_graph import KnowledgeGraph, Embedding


def llm_dynamic_add(msg, kg: KnowledgeGraph, query: QueryLLM):
    # dict_llm = query.query_llm(msg)
    dict_llm = msg
    triple = [[dict_llm['src_node_type'], dict_llm['src_node_value']], [dict_llm['tgt_node_type'], dict_llm['tgt_node_value']], [dict_llm['relation_type']]]
    print(kg)
    ans = kg.add_triple_fuzzy(triple)
    return ans


# emb = Embedding()
# print("Emb")
# kg = KnowledgeGraph("bolt://localhost:7687", ("neo4j", "12345678"), emb)
# print("kg")
# query_llm = None # QueryLLM(device='cuda:1')
# msg = "机器学习这门课程中有蒙特卡洛方法。"

# llm_dynamic_add(msg, kg, query_llm)
