from collections import deque

from colorama import Fore
from graphviz import Digraph

from utils.logging import fancy_print


class Crew:
    current_crew = None

    def __init__(self):
        self.agents = []

    def __enter__(self):
        Crew.current_crew = self
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Crew.current_crew = None

    def add_agent(self, agent):
        self.agents.append(agent)

    @staticmethod
    def register_agent(agent):
        if Crew.current_crew is not None:
            Crew.current_crew.add_agent(agent)

    def topological_sort(self):
        in_degree = {agent: len(agent.dependencies) for agent in self.agents}
        queue = deque([agent for agent in self.agents if in_degree[agent] == 0])

        sorted_agents = []

        while queue:
            current_agent = queue.popleft()
            sorted_agents.append(current_agent)

            for dependent in current_agent.dependents:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)

        if len(sorted_agents) != len(self.agents):
            raise ValueError(
                "Circular dependencies detected among agents, preventing a valid topological sort"
            )

        return sorted_agents

    def plot(self):
        dot = Digraph(format="png")

        # Add nodes and edges for each agent in the crew
        for agent in self.agents:
            dot.node(agent.name)
            for dependency in agent.dependencies:
                dot.edge(dependency.name, agent.name)
        return dot

    def run(self):
        sorted_agents = self.topological_sort()
        for agent in sorted_agents:
            fancy_print(f"RUNNING AGENT: {agent}")
            print(Fore.RED + f"{agent.run()}")