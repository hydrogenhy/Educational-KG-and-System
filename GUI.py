import tkinter as tk
from tkinter import ttk, Label
from tkinter import font
from PIL import Image, ImageTk
from stage3 import *

class KG_show:
    def __init__(self, root):
        self.emb = Embedding()
        self.graph = KnowledgeGraph(
            URI="bolt://localhost:7687",
            AUTH=("neo4j", "12345678"),
            embedding_model=self.emb
        )
        self.graph_s = MidSearch(self.graph)

        bg_c = '#99FFFF' 

        self.root = root
        self.root.title("教育知识图谱问答")
        self.root.geometry("500x650")
        self.root.configure(bg=bg_c)  # 设置背景颜色

        # 设置字体
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(size=11, family='Courier New')

        self.title_font = font.Font(size=14, family='Arial', weight='bold')

        # 设置标题
        self.title_label = tk.Label(root, text="教育知识图谱问答", font=self.title_font, bg=bg_c)
        self.title_label.pack(pady=10)

        # 创建一个Frame用于放置第一个模式选择框
        mode_frame1 = tk.Frame(root, bg=bg_c)
        mode_frame1.pack(pady=5, fill=tk.X, padx=20)

        # 第一个模式选择框
        self.mode_label1 = tk.Label(mode_frame1, text="选择模式:", bg=bg_c)
        self.mode_label1.pack(side=tk.TOP, padx=5)

        self.mode_var1 = tk.StringVar()
        self.mode_combobox1 = ttk.Combobox(mode_frame1, textvariable=self.mode_var1, font=self.default_font)
        self.mode_combobox1['values'] = ('文本匹配', '模糊搜索', '智能问答', '添加关系', '课程大纲')
        self.mode_combobox1.current(0)  # 设置默认值
        self.mode_combobox1.pack(side=tk.TOP, padx=5)

        # 创建一个Frame用于放置第二个模式选择框
        mode_frame2 = tk.Frame(root, bg=bg_c)
        mode_frame2.pack(pady=5, fill=tk.X, padx=20)

        # 第二个模式选择框
        self.mode_label2 = tk.Label(mode_frame2, text="搜索范围:", bg=bg_c)
        self.mode_label2.pack(side=tk.TOP, padx=5)

        self.mode_var2 = tk.StringVar()
        self.mode_combobox2 = ttk.Combobox(mode_frame2, textvariable=self.mode_var2, font=self.default_font)
        self.mode_combobox2['values'] = ('课程', '章节', '知识点', '全部')
        self.mode_combobox2.current(3)  # 设置默认值
        self.mode_combobox2.pack(side=tk.TOP, padx=5)

        self.input_label = tk.Label(root, text="请输入您的问题:", bg=bg_c)
        self.input_label.pack(pady=5)

        self.input_text = tk.Text(root, height=5, width=50, font=self.default_font)
        self.input_text.pack(pady=5)

        self.submit_button = tk.Button(root, text="提交", command=self.handle_submit, bg='#4CAF50', fg='white', font=self.default_font)
        self.submit_button.pack(pady=10)

        self.output_label = tk.Label(root, text="回答:", bg=bg_c)
        self.output_label.pack(pady=5)

        self.output_text = tk.Text(root, height=15, width=50, font=self.default_font)
        self.output_text.pack(pady=5)
        self.output_text.config(state=tk.DISABLED)  # 设为只读模式

    def handle_submit(self):
        question = self.input_text.get("1.0", tk.END).replace("\n", "").strip()
        mode = self.mode_var1.get()
        field = self.mode_var2.get()
        self.generate_answer(question, mode, field)

    def generate_answer(self, question, mode, field):
        dic = {'课程':0, '章节':1, '知识点':2, '全部':3}
        if field not in list(dic.keys()):
            self.text_show("未知课程范围")
            return
        if mode == '文本匹配':
            self.text_show("正在搜索......")
            self.root.update_idletasks()
            answer = task1(self.graph, question, dic[field])
            self.text_show(answer)
        elif mode == '模糊搜索':
            self.text_show("正在搜索......")
            self.root.update_idletasks()
            answer = task2(self.graph, self.graph_s, question, dic[field])
            self.text_show(answer)
        elif mode == '智能问答':
            question = question.strip().split() # 若无大模型则输入list
            self.text_show("正在搜索......")
            self.root.update_idletasks()
            answer = task4(self.graph, self.graph_s, question)
            self.text_show(answer)
        elif mode == '添加关系':
            self.text_show("正在处理......")
            self.root.update_idletasks()
            try:
                t = question.strip().split()
            except:
                ValueError("wrong template")
            question = {"src_node_type": t[0], "src_node_value": t[1], 
                        "tgt_node_type": t[2], "tgt_node_value": t[3], 
                        "relation_type": t[4]}
            answer = task3(self.graph, question)
            self.text_show({answer})
        elif mode == '课程大纲':
            self.text_show("正在搜索......")
            self.root.update_idletasks()
            course_all = list(self.graph.embeddings['course'].keys())
            if question in course_all:
                answer = self.graph.query_course(question)
            else:
                answer = "不存在当前课程"
            self.text_show(answer)
        else:
            self.text_show("未知模式")
    
    def text_show(self, text):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = KG_show(root)
    root.mainloop()
