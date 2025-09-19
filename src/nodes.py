from typing import Dict, Any, List
from src.utils import sanitize_text, score_argument

class NodeResponse:
    def __init__(self, speaker: str, content: str, round_no: int):
        self.speaker = speaker
        self.content = sanitize_text(content)
        self.round_no = round_no

    def to_dict(self):
        return {'speaker': self.speaker, 'content': self.content, 'round': self.round_no}

class AgentNode:
    def __init__(self, name: str, persona: str, policy: str = 'templated'):
        self.name = name
        self.persona = persona
        self.policy = policy
        self.past_arguments: List[str] = []

    def generate(self, topic: str, memory_summary: str, turn_no: int) -> NodeResponse:
        base = f"Topic: {topic}."
        if self.persona.lower().startswith('scient'):
            content = (f"As a {self.persona}, I argue that {topic} poses measurable risks and needs regulation. "
                       f"Consider risk-based frameworks, safety testing, and clinical-style evaluation. "
                       f"Memory notes: {memory_summary}")
        else:
            content = (f"From a {self.persona} perspective, {topic} touches autonomy and freedom of thought. "
                       f"Overregulation can stifle progress and philosophical inquiry. "
                       f"Memory notes: {memory_summary}")
        if content in self.past_arguments:
            content += " (additional nuance added to avoid repetition.)"
        self.past_arguments.append(content)
        return NodeResponse(self.name, content, turn_no)

class MemoryNode:
    def __init__(self):
        self.transcript: List[Dict[str, Any]] = []
        self.summary: str = ''

    def update(self, response: NodeResponse):
        self.transcript.append(response.to_dict())
        last_texts = ' '.join([r['content'] for r in self.transcript[-4:]])
        self.summary = last_texts[:800]

    def get_agent_memory_for(self, agent_name: str) -> str:
        mem_items = []
        for r in self.transcript[-3:]:
            if r['speaker'] != agent_name:
                mem_items.append(r['content'])
        return ' | '.join(mem_items)

class JudgeNode:
    def __init__(self):
        pass

    def evaluate(self, transcript: List[Dict[str, Any]], memory_summary: str) -> Dict[str, Any]:
        totals = {'Scientist': 0, 'Philosopher': 0}
        details = []
        for r in transcript:
            sc = score_argument(r['content'])
            if r['speaker'].lower().startswith('scient'):
                totals['Scientist'] += sc['safety_score'] - sc['freedom_score']*0.2
            else:
                totals['Philosopher'] += sc['freedom_score'] - sc['safety_score']*0.2
            details.append({'round': r['round'], 'speaker': r['speaker'], 'score': sc})
        winner = max(totals, key=totals.get)
        justification = (f"Totals: {totals}. Judge notes memory summary length {len(memory_summary)}. "
                         f"Winner chosen based on keyword-aligned scores and coherence across rounds.")
        return {'winner': winner, 'totals': totals, 'details': details, 'justification': justification}
