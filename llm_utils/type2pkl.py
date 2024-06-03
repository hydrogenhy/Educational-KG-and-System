import pickle


with open('node_type.pkl', 'wb') as f:
    pickle.dump(['course', 'chapter', 'knowledge'], f)

with open('edge_type.pkl', 'wb') as f:
    pickle.dump(['contain'], f)
