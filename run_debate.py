from src.controller import DebateController
from src.dag_generator import generate_dag

def main():
    topic = input('Enter topic for debate: ')
    dc = DebateController(topic)
    img = generate_dag()
    print('DAG generated at:', img)
    result = dc.run()
    print('\n[Judge] Winner:', result['winner'])
    print('Reason:', result['justification'])

if __name__ == '__main__':
    main()
