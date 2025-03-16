from ReflectionPattern.reflection_agent import ReflectionAgent

agent = ReflectionAgent()

final_response = agent.run(
    n_steps=7,
    user_msg="generate a python implementation of the best sort algorithm that works for any data type",
    verbose=1
)

print(final_response)