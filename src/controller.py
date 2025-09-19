import json
import os
from src.nodes import AgentNode, MemoryNode, JudgeNode
from src.logger_setup import get_logger
from src.utils import sanitize_text

logger = get_logger()

class DebateController:
    def __init__(self, topic: str, agent_a_name='Scientist', agent_b_name='Philosopher'):
        self.topic = sanitize_text(topic)
        self.agent_a = AgentNode(agent_a_name, 'Scientist')
        self.agent_b = AgentNode(agent_b_name, 'Philosopher')
        self.memory = MemoryNode()
        self.judge = JudgeNode()
        self.rounds_total = 8
        self.history = []
        self.state_file = os.path.join(os.getcwd(), 'logs', 'debate_state.json')

    def validate_turn(self, expected_round, speaker):
        if expected_round != len(self.history) + 1:
            raise RuntimeError('Round mismatch')

    def run(self):
        logger.info(f"Starting debate on: {self.topic}")
        current_speaker = 'A'
        for r in range(1, self.rounds_total + 1):
            self.validate_turn(r, current_speaker)
            if current_speaker == 'A':
                memory_for = self.memory.get_agent_memory_for(self.agent_a.name)
                resp = self.agent_a.generate(self.topic, memory_for, r)
            else:
                memory_for = self.memory.get_agent_memory_for(self.agent_b.name)
                resp = self.agent_b.generate(self.topic, memory_for, r)
            if any(h['content'] == resp.content for h in self.history):
                logger.warning(f"Detected repeated argument on round {r} by {resp.speaker}")
                resp.content += ' (added nuance to avoid exact repetition)'
            self.history.append(resp.to_dict())
            self.memory.update(resp)
            logger.info(f"[Round {r}] {resp.speaker}: {resp.content}")
            current_speaker = 'B' if current_speaker == 'A' else 'A'
            self._save_state()
        judge_output = self.judge.evaluate(self.history, self.memory.summary)
        logger.info('[Judge] Summary of debate:')
        logger.info(judge_output['justification'])
        logger.info(f"[Judge] Winner: {judge_output['winner']}")
        self._save_state(final_judgment=judge_output)
        return judge_output

    def _save_state(self, final_judgment=None):
        data = {'topic': self.topic, 'history': self.history, 'memory_summary': self.memory.summary}
        if final_judgment:
            data['judgment'] = final_judgment
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
