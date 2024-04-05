import networkx as nx
import pickle
import matplotlib.pyplot as plt
from pyvis.network import Network
import json

def read_graph_from_gpickle(file_path):
    """
    Reads a graph from a gpickle file and returns the graph object.

    Parameters:
    - file_path (str): The path to the .gpickle file.

    Returns:
    - G (Graph): The graph object loaded from the .gpickle file.
    """
    try:
        # Load the graph from the .gpickle file
        with open(file_path,'rb') as inpf:
            G = pickle.load(inpf) 
        print("Graph loaded successfully.")
        return G
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Path to your .gpickle file
    graphs_fps = [
      "./expanded_knowledge_graph_with_questions.gpickle",
      "./expanded_knowledge_graph_with_more_questions.gpickle",
      "expanded_knowledge_graph_with_all_questions.gpickle",
    ]
    file_path = graphs_fps[-1] 
    
    # Read the graph
    catMap = {
        1: 'category',
        2: 'category',
        3: 'task',
        4: 'question'
    }
    colorMap = {
        'category',
        'task',
        'question'
    }
    with open(f'{graphs_fps[-1]}.json') as inpf:
        d = json.load(inpf) 
        d['nodes'] = [
            {**node_d,
             'category': catMap[len(node_d['id'].split('.'))],
             'group': len(node_d['id'].split('.')),
             } for node_d in d['nodes'] 
        ]
        print(d['nodes'])
        exit()
        try:
            G = nx.node_link_graph(d)
        except:
            G = read_graph_from_gpickle(file_path)
            exit()
    
    print(nx.node_link_data(G))
    exit()
    # Example usage: Print the nodes and edges of the graph
    if G is not None:
        print("Nodes in the graph:")
        for node in G.nodes(data=True):
            print(node)
        
        print("\nEdges in the graph:")
        for edge in G.edges(data=True):
            print(edge)

    '''
    pos = { 1: (20, 30), 2: (40, 30), 3: (30, 10),4: (0, 40)}

    nx.draw_networkx(G)
    plt.show()
    '''
    net = Network(
    directed = True,
    select_menu = True, # Show part 1 in the plot (optional)
    filter_menu = True, # Show part 2 in the plot (optional)
    )
    net.show_buttons() # Show part 3 in the plot (optional)
    net.from_nx(G) # Create directly from nx graph
    print(net.nodes)
    print(dir(net))
    net.write_html('test.html')
    dict_data  = nx.node_link_data(G)
    with open(f'{graphs_fps[-1]}-modified.json','w') as outf:
        outf.write(json.dumps(dict_data, indent=4))
