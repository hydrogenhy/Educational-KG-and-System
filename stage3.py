from graph_utils.search import MidSearch
from graph_utils.knowledge_graph import KnowledgeGraph, Embedding
from graph_utils.utils import *
import pickle
from example_llm_dynamic import llm_dynamic_add

def task1(graph:KnowledgeGraph, question=None, type=3):
    types = [['course'], ['chapter'], ['knowledge'], ['course', 'chapter', 'knowledge']]
    ans = ""
    # input
    print('请输入欲查询的内容')
    name = question # input()
    # process
    print("搜索中......")
    name_all = []
    for type in types[type]:
        name_all = list(graph.embeddings[type].keys())
        if name in name_all:
            q1, q2 = built_s(name, type)
            res1 = graph.query(q1, 1)
            res2 = graph.query(q2, 2)
            ans = kg_return(res1, res2)
            break
    if ans == "":
        print("未匹配到内容，建议使用模糊搜索")
        ans += "未匹配到内容，建议使用模糊搜索"
    return ans

def task2(graph:KnowledgeGraph, graph_s:MidSearch, question=None, type=3):
    types = [['course'], ['chapter'], ['knowledge'], ['course', 'chapter', 'knowledge']]
    ans = ""
    # input
    print('请输入欲查询的内容')
    name = question # input()
    print('请输入欲查询范围(0-课程范围; 1-章节范围; 2-知识点范围; 3-全部范围):')
    type_c = type # int(input())
    # process
    print("搜索中......")
    score, text, cat = graph_s.search(name, types[type_c])
    q1, q2 = built_s(text, types[cat][0])
    res1 = graph.query(q1, 1)
    res2 = graph.query(q2, 2)
    print(f"您欲搜索的知识内容为：{name}, 在知识图谱给定范围中查到最相近的内容为：{types[cat][0]}-{text} (余弦相似度为{score.item():.2f})。")
    ans += f"您欲搜索的知识内容为：{name}, 在知识图谱给定范围中查到最相近的内容为：{types[cat][0]}-{text} (余弦相似度为{score.item():.2f})。\n"
    ans += kg_return(res1, res2)
    return ans

def task3(graph:KnowledgeGraph, msg=None,):
    ans = llm_dynamic_add(msg, graph, None)
    return ans

def task4(graph:KnowledgeGraph, graph_s:MidSearch, querys):
    ans = ""
    print("您可能需要的内容如下：")
    ans += "您可能需要的内容如下：\n"
    for i, q in enumerate(querys):
        print(f"{i+1}.{q}：")
        ans += f"{i+1}.{q}：\n"
        ans += task2(graph, graph_s, q)
    return ans






# if __name__=='__main__':
#     # init
#     emb = Embedding()
#     graph = KnowledgeGraph(
#         URI = "bolt://localhost:7687",
#         AUTH = ("neo4j", "12345678"),
#         embedding_model = emb
#     )
#     graph_s = MidSearch(graph)

#     # task3(graph, graph_s)
#     while 1:
#         mode = int(input("\n选用问答方式: 1-字符匹配, 2-模糊匹配: "))
#         if mode == 1:
#             task1(graph)
#         elif mode == 2:
#             task2(graph, graph_s)