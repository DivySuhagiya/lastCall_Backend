from lastcall_agent.schemas import CharacterScenariosOutput
from google.adk.agents.llm_agent import Agent

scenario_builder_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='scenario_builder_agent',
    description='Creates role-play instructions for each suspect character.',
    instruction='''
        "You are an expert AI persona designer. You will be given a murder mystery story. And the story is {generated_story}."
        "Your task is to extract EVERY character mentioned in the story and generate a 'Scenario Block' for them. And never generate scenario of character who is victim or who is killed."
        "For each character, the scenario must follow this EXACT format:"
        "[ROLE: <Summary of their role (e.g. You secretly killed... or You are an innocent witness...)]"
        "[KEY FACTS YOU MUST REMEMBER]"
        "- <Fact 1>"
        "- <Fact 2>"
        "[HOW TO TALK ABOUT IT]"
        "- <Guideline 1>"
        "- Example tone: <Example quote>"
        "Output strictly valid JSON where keys are character names and values are the scenario strings:"
        "Example_OUTPUT = { "name":"Amelia", "scenario": "...scenario string...",
                            "name": "Lucian", "scenario": "...scenario string...",
                            "name": "Sebastian", "scenario": "...scenario string..."
                        }"
        In scenario string i want only string no other special characters and /n and all.
    ''',
    output_key="generated_scenarios",
    output_schema=CharacterScenariosOutput,
)
