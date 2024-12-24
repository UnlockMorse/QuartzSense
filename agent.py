import openai
import json
from tasks import greet_user, tell_joke, tell_story, perform_calculation
from logs import log_interaction
from settings import load_user_settings

class AIAgent:
    def __init__(self, name, personality, task_list, settings):
        self.name = name
        self.personality = personality
        self.task_list = task_list
        self.settings = settings
        self.api_key = settings["openai_api_key"]
        openai.api_key = self.api_key
        self.interaction_history = []

    def interact(self, user_input):
        log_interaction("User", user_input)  # Log user input

        prompt = f"Agent {self.name} with the personality of {self.personality}, respond to: {user_input}"
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            agent_response = response.choices[0].text.strip()
            log_interaction("Agent", agent_response)  # Log agent response
            return agent_response
        except Exception as e:
            log_interaction("Error", str(e))
            return f"Sorry, I encountered an error: {str(e)}"

    def execute_task(self, task_name):
        if task_name in self.task_list:
            task_function = self.task_list[task_name]
            result = task_function()
            log_interaction("Task", f"Executed task {task_name}: {result}")  # Log task execution
            return result
        else:
            return f"Sorry, I don't know how to perform the task: {task_name}"

    def show_settings(self):
        return f"Current settings: {json.dumps(self.settings, indent=4)}"

    def update_settings(self, new_settings):
        self.settings.update(new_settings)
        return "Settings updated successfully! 🔧"

def create_agent(config_path, settings_path):
    with open(config_path, "r") as f:
        config = json.load(f)
    
    settings = load_user_settings(settings_path)
    
    agent = AIAgent(
        name=config["name"],
        personality=config["personality"],
        task_list=config["tasks"],
        settings=settings
    )
    
    return agent
