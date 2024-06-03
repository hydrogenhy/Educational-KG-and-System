import torch


def cos_cal(emb1, emb2):
    emb1 = torch.tensor(emb1, device='cuda:0')
    emb2 = torch.tensor(emb2, device='cuda:0')
    a = torch.dot(emb1, emb2)
    a1 = torch.norm(emb1)
    a2 = torch.norm(emb2)
    return a / (a1 * a2)

def kg_return(res1, res2):
    ans = ""
    if len(res1) != 0:
        print("你可能需要系统的了解：", end='')
        ans += "你可能需要系统的了解："
        for i in res1:
            print(i, end=', ')
            ans += i
            ans += ", "
        print("\b\b 等领域")
        ans = ans[:-2]
        ans += " 等领域\n"
    if len(res2) != 0:
        print("你可能需要深入了解：", end='')
        ans += "你可能需要深入了解："
        for i in res2:
            print(i, end=', ')
            ans += i
            ans += ", "
        print("\b\b 等知识")
        ans = ans[:-2]
        ans += " 等领域\n"
    return ans

def built_s(text, cat):
    q1 = f"MATCH (n)-[r]->(m:{cat}) WHERE m.title = '{text}' RETURN n,r,m"
    q2 = f"MATCH (n:{cat})-[r]->(m) WHERE n.title = '{text}' RETURN n,r,m"
    return q1, q2

def print_course_outline(course_outline, course_name):
    res1 = ""
    def print_tree(dictionary, prefix=''):
        res2 = ""
        # 获取字典中的所有键值对
        items = list(dictionary.items())
        # 获取字典中项目的数量
        count = len(items)
        for index, (chapter, knowledge_list) in enumerate(items):
            # 判断是否是最后一个元素
            if index == count - 1:
                # print(prefix + '└── ' + chapter)
                res2 += prefix + '└── ' + chapter + '\n'
                new_prefix = prefix + '    '
            else:
                # print(prefix + '├── ' + chapter)
                res2 += prefix + '├── ' + chapter + '\n'
                new_prefix = prefix + '│   '
            # 打印知识点列表
            if knowledge_list:
                for knowledge in knowledge_list:
                    if knowledge == knowledge_list[-1]:
                        # print(new_prefix + '└── ' + knowledge)
                        res2 += new_prefix + '└── ' + knowledge + '\n'
                    else:
                        # print(new_prefix + '├── ' + knowledge)
                        res2 += new_prefix + '├── ' + knowledge + '\n'
        return res2

    # 打印课程名称
    # print(course_name)
    res1 += course_name + '\n'
    # 打印课程大纲
    res1 += print_tree(course_outline)
    print(res1)
    return res1
