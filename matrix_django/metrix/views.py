import json
import shutil
import subprocess
import sys
sys.path.append('E:\course\知识图谱\大作业')
from stage3 import *
# from example_llm_dynamic import llm_dynamic_add

from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.conf import settings
import os

emb = Embedding()
graph = KnowledgeGraph(
    URI="bolt://localhost:7687",
    AUTH=("neo4j", "12345678"),
    embedding_model=emb
)
graph_s = MidSearch(graph)

def llm_dynamic_add(msg, kg: KnowledgeGraph, query):
    # dict_llm = query.query_llm(msg)
    dict_llm = msg
    triple = [[dict_llm['src_node_type'], dict_llm['src_node_value']], [dict_llm['tgt_node_type'], dict_llm['tgt_node_value']], [dict_llm['relation_type']]]
    print(kg)
    ans = kg.add_triple_fuzzy(triple)
    return ans

def get_llm(graph:KnowledgeGraph, msg=None,):
    ans = llm_dynamic_add(msg, graph, None)
    return ans

def test(mode, field, question):
    dic = {'课程':0, '章节':1, '知识点':2, '全部':3}
    if mode == '文本匹配':
        answer = task1(graph, question, dic[field])
    elif mode == '模糊搜索':
        answer = task2(graph, graph_s, question, dic[field])
    elif mode == '智能问答':
        question = question.strip().split()
        answer = task4(graph, graph_s, question)
    elif mode == '关系添加':
        # t = question.strip().split()
        # print(t)
        try:
            # question = {"src_node_type": t[0], "src_node_value": t[1], 
            #         "tgt_node_type": t[2], "tgt_node_value": t[3], 
            #         "relation_type": t[4]}
            answer = get_llm(graph, question)
        except:
            answer = "wrong template"
    elif mode == '课程大纲':
        course_all = list(graph.embeddings['course'].keys())
        if question in course_all:
            answer = graph.query_course(question)
        else:
            answer = "不存在当前课程"
    return answer


def answer(request):
    if request.method != "POST":
        return JsonResponse({'errno': 1001, 'errmsg': '请求方法错误'})
    body = json.loads(request.body)
    mode = body.get('mode')  # 选择模式
    range = body.get('range')  # 选择范围
    question = body.get('question')  # 输入问题
    print(mode, range, question) # 输入的参数
    answer = test(mode, range, question)
    return JsonResponse({'errno': 0, 'errmsg': '回答成功', 'data': answer})
