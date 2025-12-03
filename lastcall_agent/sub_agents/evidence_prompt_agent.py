from lastcall_agent.schemas import EvidenceImagePromptsOutput
from google.adk.agents.llm_agent import Agent

evidence_prompt_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='evidence_prompt_agent',
    description='Generates AI image prompts for evidence visualization.',
    instruction='''
        You are an expert AI evidence designer. You will be given a murder mystery story. And the story is {generated_story}.\n\n"
        "Your task is to extract EVERY evidence mentioned in the story evidence is in json and key is evidences. Based on evidence details generate an image prompt for each of them.\n\n"
        IMPORTANT: Always return your response as a JSON object with the following structure:
        prompts: [
        {
        "name": <evidence_name>,
        "image_prompt": <evidence_image_prompt_description>
        },
        {
        "name": <evidence_name>,
        "image_prompt": <evidence_image_prompt_description>
        },
        {
        "name": <evidence_name>,
        "image_prompt": <evidence_image_prompt_description>
        }
        ]
        ''',
    output_key="generated_evidence_prompts",
    output_schema=EvidenceImagePromptsOutput
)
