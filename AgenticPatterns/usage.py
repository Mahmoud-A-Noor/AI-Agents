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

import json
import requests
from ToolPattern.tool import tool
from ToolPattern.tool_agent import ToolAgent

@tool
def fetch_top_hacker_news_stories(top_n: int):
    """
    Fetch the top stories from Hacker News.

    This function retrieves the top `top_n` stories from Hacker News using the Hacker News API. 
    Each story contains the title, URL, score, author, and time of submission. The data is fetched 
    from the official Firebase Hacker News API, which returns story details in JSON format.

    Args:
        top_n (int): The number of top stories to retrieve.
    """

    top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    
    try:
        response = requests.get(top_stories_url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Get the top story IDs
        top_story_ids = response.json()[:top_n]
        
        top_stories = []
        
        # For each story ID, fetch the story details
        for story_id in top_story_ids:
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            story_response = requests.get(story_url)
            story_response.raise_for_status()  # Check for HTTP errors
            story_data = story_response.json()
            
            # Append the story title and URL (or other relevant info) to the list
            top_stories.append({
                'title': story_data.get('title', 'No title'),
                'url': story_data.get('url', 'No URL available'),
            })
        
        return json.dumps(top_stories)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []

tool_agent = ToolAgent(tools=[fetch_top_hacker_news_stories])
output = tool_agent.run(user_msg="Tell me your name")
print(output)
output = tool_agent.run(user_msg="Tell me the top 5 Hacker News stories right now")
print(output)
