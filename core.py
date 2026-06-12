from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from typing import List , Optional
from langchain_core.output_parsers import PydanticOutputParser

model = ChatMistralAI(model='mistral-small-2506')


# Create a schema
class Movie(BaseModel): # Pydantic schema
    title:str
    release_year:Optional[int]
    genre:List[str]
    director:Optional[str]
    cast:List[str]
    rating:Optional[float]
    summary:str

parser = PydanticOutputParser(pydantic_object=Movie)

prompt = ChatPromptTemplate.from_messages([
    ('system',"""
Extract movie information from the paragraph
     {format_instructions}
"""     
    ),
    ('human','{paragraph}')]
)
#     [(
#         "system",
#         """
# You are an expert information extraction system.

# Your task is to analyze the given text and extract the most useful information.

# Rules:
# 1. Extract only information explicitly present in the text.
# 2. Do not hallucinate or invent facts.
# 3. If information is missing, return null.
# 4. Generate a concise summary in 2-3 sentences.
# 5. Return output in valid JSON only.
# 6. Keep lists as arrays.
# 7. Preserve original names and spellings.

# Output Schema:

# Title:
# Type:
# Release Year:
# Genre:
# Director:
# Writer:
# Cast:
# Series:
# Setting:
# Location:
# Main Characters:
# Organizations:
# Important Entities:
# Plot:
# Themes:
# Keywords:
# """
#     ),
#     (
#         "human",
#         """
# Extract structured information from the following paragraph.

# TEXT:
# {paragraph}
# """
#     )
# ]


para = input('Give your Paragraph : ')

final_prompt = prompt.invoke(
    {
        'paragraph' : para,
        'format_instructions':parser.get_format_instructions()
    }
)

response = model.invoke(final_prompt)
# movie_data = parser.parse(response.content)
# print(movie_data)

print(response.content)