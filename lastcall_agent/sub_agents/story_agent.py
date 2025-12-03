from lastcall_agent.schemas import MurderMysteryStory
from google.adk.agents.llm_agent import Agent

story_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='story_agent',
    description='Generates a murder mystery plot with victim, killer, suspects, and evidence.',
    instruction='''
        You are a master mystery writer. Create a concise but detailed murder mystery plot. The plot must include a backstory involving a murder by a Killer.
        Include the motive, the method, the location, and 3 other characters and always one female and two males and all they are suspects. So there are total 4 characters including victim and killer. And also include their names
        Do not write a dialogue, just the narrative facts.
        You have to also include the names of 3 evidences. and carefully describe that and also make sure evidence should be relevant to the plot and can easily generate image of that evidence and details should have clue so user can find out who is killer.
        IMPORTANT: Always return your response as a JSON object with the following structure and always make sure there is only one female in suspect and two others are male:
        {
        "victim": <victim_name>,
        "killer": <killer_name>,
        "story": <story>,
        "location": <location>,
        "character_details": [
            {
                "name": <character_name>,
                "gender": <character_gender>,
                "description": <character_description>
            },
            {
                "name": <character_name>,
                "gender": <character_gender>,
                "description": <character_description>
            },
            {
                "name": <character_name>,
                "gender": <character_gender>,
                "description": <character_description>
            }        
        ],
        "evidences": [
            {
                "name": <evidence_name>,
                "description": <evidence_description>
            },
            {
                "name": <evidence_name>,
                "description": <evidence_description>
            },
            {
                "name": <evidence_name>,
                "description": <evidence_description>
            }
        ]
        }
    ''',
    output_key="generated_story",
    output_schema=MurderMysteryStory
)
