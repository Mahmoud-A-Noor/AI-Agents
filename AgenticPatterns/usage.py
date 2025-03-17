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

from PlanningPattern.planning_agent import PlanningAgent
from tools import sum_two_elements, multiply_two_elements, compute_log

agent = PlanningAgent(tools=[sum_two_elements, multiply_two_elements, compute_log])
output = agent.run(user_msg="I want to calculate the sum of 1234 and 5678 and multiply the result by 5. Then, I want to take the logarithm of this result")
print(output)
