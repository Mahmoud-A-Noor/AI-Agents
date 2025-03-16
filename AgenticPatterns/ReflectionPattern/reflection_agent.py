from colorama import Fore
from dotenv import load_dotenv
from groq import Groq

from utils.completions import build_prompt_structure, completions_create, FixedFirstChatHistory, update_chat_history
from utils.logging import fancy_step_tracker

load_dotenv()


BASE_GENERATION_SYSTEM_PROMPT = """
Your task is to Generate the best content possible for the user's request.
If the user provides critique, respond with a revised version of your previous attempt.
You must always output the revised content.
"""

BASE_REFLECTION_SYSTEM_PROMPT = """
You are tasked with generating critique and recommendations to the user's generated content.
If the user content has something wrong or something to be improved, output a list of recommendations
and critiques. If the user content is ok and there's nothing to change, output this: <OK>
"""


class ReflectionAgent:

    def __init__(self, model: str = "llama-3.3-70b-versatile"):
        self.client = Groq()
        self.model = model

    def _request_completion(
        self,
        history: list,
        verbose: int = 0,
        log_title: str = "COMPLETION",
        log_color: str = "",
    ):
        output = completions_create(self.client, history, self.model)

        if verbose > 0:
            print(log_color, f"\n\n{log_title}\n\n", output)

        return output

    def generate(self, generation_history: list, verbose: int = 0) -> str:
        return self._request_completion(
            generation_history, verbose, log_title="GENERATION", log_color=Fore.BLUE
        )

    def reflect(self, reflection_history: list, verbose: int = 0) -> str:
        return self._request_completion(
            reflection_history, verbose, log_title="REFLECTION", log_color=Fore.GREEN
        )

    def run(
        self,
        user_msg: str,
        generation_system_prompt: str = "",
        reflection_system_prompt: str = "",
        n_steps: int = 10,
        verbose: int = 0,
    ) -> str:

        generation_system_prompt += BASE_GENERATION_SYSTEM_PROMPT
        reflection_system_prompt += BASE_REFLECTION_SYSTEM_PROMPT

        generation_history = FixedFirstChatHistory(
            [
                build_prompt_structure(prompt=generation_system_prompt, role="system"),
                build_prompt_structure(prompt=user_msg, role="user"),
            ],
            total_length=3,
        )

        reflection_history = FixedFirstChatHistory(
            [build_prompt_structure(prompt=reflection_system_prompt, role="system")],
            total_length=3,
        )

        for step in range(n_steps):
            if verbose > 0:
                fancy_step_tracker(step, n_steps)

            # Generate the response
            generation = self.generate(generation_history, verbose=verbose)
            update_chat_history(generation_history, generation, "assistant")
            update_chat_history(reflection_history, generation, "user")

            # Reflect and critique the generation
            critique = self.reflect(reflection_history, verbose=verbose)

            if "<OK>" in critique:
                # If no additional suggestions are made, stop the loop
                print(
                    Fore.RED,
                    "\n\nStop Sequence found. Stopping the reflection loop ... \n\n",
                )
                break

            update_chat_history(generation_history, critique, "user")
            update_chat_history(reflection_history, critique, "assistant")

        return generation