##### Refect Agent Pattern Example #####

# from ReflectionPattern.reflection_agent import ReflectionAgent
# agent = ReflectionAgent()
# final_response = agent.run(
#     n_steps=7,
#     user_msg="generate a python implementation of the best sort algorithm that works for any data type",
#     verbose=1
# )
# print(final_response)


##### Tool Agent Pattern Example #####

# from ToolPattern.tool_agent import ToolAgent
# from tools import fetch_top_hacker_news_stories

# tool_agent = ToolAgent(tools=[fetch_top_hacker_news_stories])
# output = tool_agent.run(user_msg="Tell me your name")
# print(output)
# output = tool_agent.run(user_msg="Tell me the top 5 Hacker News stories right now")
# print(output)


##### Planning Agent Pattern Example #####

# from PlanningPattern.planning_agent import PlanningAgent
# from tools import sum_two_elements, multiply_two_elements, compute_log

# agent = PlanningAgent(tools=[sum_two_elements, multiply_two_elements, compute_log])
# output = agent.run(user_msg="I want to calculate the sum of 1234 and 5678 and multiply the result by 5. Then, I want to take the logarithm of this result")
# print(output)



##### Multi Agent Pattern Example #####

from MultiAgentPattern.crew import Crew
from MultiAgentPattern.agent import Agent
from tools import write_str_to_txt

with Crew() as crew:
    agent_1 = Agent(
        name="Poet Agent",
        backstory="You are a well-known poet, who enjoys creating high quality poetry.",
        task_description="Write a poem about the meaning of life",
        task_expected_output="Just output the poem, without any title or introductory sentences",
    )

    agent_2 = Agent(
        name="Poem Translator Agent",
        backstory="You are an expert translator especially skilled in Spanish",
        task_description="Translate a poem into Spanish", 
        task_expected_output="Just output the translated poem and nothing else"
    )

    agent_3 = Agent(
        name="Writer Agent",
        backstory="You are an expert transcriber, that loves writing poems into txt files",
        task_description="You'll receive a Spanish poem in your context. You need to write the poem into './poem.txt' file",
        task_expected_output="A txt file containing the greek poem received from the context",
        tools=write_str_to_txt,
    )

    agent_1 >> agent_2 >> agent_3

crew.plot()
crew.run()