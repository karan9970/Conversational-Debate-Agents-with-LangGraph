from graphviz import Digraph
import os

OUT_DIR = os.path.join(os.getcwd(), 'diagrams')
os.makedirs(OUT_DIR, exist_ok=True)

def generate_dag(output_path=None):
    dot = Digraph(comment='Debate DAG', format='png')
    dot.node('U', 'UserInputNode')
    dot.node('A', 'AgentA')
    dot.node('M', 'MemoryNode')
    dot.node('B', 'AgentB')
    dot.node('J', 'JudgeNode')
    dot.edges([('U','A'), ('A','M'), ('M','B'), ('B','M'), ('M','A'), ('A','M'), ('M','J')])
    p = output_path or os.path.join(OUT_DIR, 'debate_dag')
    dot.render(p, cleanup=True)
    return p + '.png'

if __name__ == '__main__':
    print('Generating DAG...')
    print(generate_dag())
