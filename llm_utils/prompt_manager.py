extract_prompt = """从以下句子中提取符合node types和edge types的三元组:
Node types: ["course", "chapter", "knowledge"]
Edge types: ["contain"]

句子: {msg}

输出JSON格式: {{"src_node_type": type, "src_node_value": name, "tgt_node_type": type, "tgt_node_value": name, "relation_type": type}}

你只会以输出格式回复结果，而不是其他任何内容。请注意，您的回答应该是简明扼要的，不需要附带任何额外的解释。"""
