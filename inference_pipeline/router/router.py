from semantic_router.layer import RouteLayer
from semantic_router import Route
from langchain.encoders import OpenAIEncoder
import os
from config import settings
# we could use this as a guide for our chatbot to avoid political
# conversations

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

semanticRag = Route(
    name="SemanticRAG",
    utterances=[
        "What do you think about using AI and celebrities in education? Do you find it effective?",
        "Have you ever used a specific method like BAP to solve math problems? What works  best for you?",
        "What other creative uses for deep fake technology can you think of in education?",
        "How do you feel about kids learning math through AI? Is it a good idea?",
        "Would you want guides on using AI tools for learning? What subjects would you like to explore?"
    ],
)

# this could be used as an indicator to our chatbot to switch to a more
# conversational prompt
textSql = Route(
    name="TextToSql",
    utterances=[
        "What is the total number of views for all TikTok videos?",
        "Which video has the highest number of likes, and what is the link to it?",
        """How many comments did the video titled "ChatDev - Build an AI workforce" receive?""",
        "What are the hashtags used in the video with the most shares?",
        "Which video has the longest duration, and what is its date posted?",
        """How many likes did the video with the caption "Top Free AI Text-to-Image Generators" receive?""",
        "List all videos that have more than 500,000 views and their corresponding comments."
    ],
)

# we place both of our decisions together into single list
routes = [semanticRag, textSql]

encoder = OpenAIEncoder()
routeLayer = RouteLayer(encoder=encoder, routes=routes)