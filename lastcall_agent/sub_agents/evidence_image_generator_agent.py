from lastcall_agent.tools.generate_image import generate_image
from lastcall_agent.schemas import EvidenceImagesOutput
from google.adk.agents.llm_agent import Agent

evidence_image_generator_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='evidence_image_generator_agent',
    description='Generates actual images for each piece of evidence using image generation tools.',
    instruction='''
        You have to pass each image prompt from {generated_evidence_prompts} to the tool and generate an image.
        return a list of image urls
        IMPORTANT: Always return your response as a JSON object with the following structure:
        urls: [
            {
                "name": <evidence_name>,
                "url": <evidence_image_url>
            },
            {
                "name": <evidence_name>,
                "url": <evidence_image_url>
            },
            {
                "name": <evidence_name>,
                "url": <evidence_image_url>
            }
        ]
        ''',
    tools=[generate_image],
    output_schema=EvidenceImagesOutput
)
