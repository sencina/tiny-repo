from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from env import OPENAI_API_KEY

model = ChatOpenAI(model="gpt-4o", temperature=0.7,api_key=OPENAI_API_KEY)

def call_json_output_parser():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate many questions related to the phrase passed, there must be 1 numeric question.\nFormatting Instructions: {format_instructions}"),
        ("human", "{phrase}")
    ])

    class Question(BaseModel):
        type: str = Field(description="the type of the question, it can be only 'NUMERIC' or 'STRING'")
        # content: list = Field(description="the content of the question")
        content: str = Field(description="the content of the question")        

    class Response(BaseModel):
        questions: list[Question] = Field(description="the generated questions (must be question type as passed)")
    
    parser = JsonOutputParser(pydantic_object=Response)

    chain = prompt | model | parser
    
    return chain.invoke({
        "phrase": "The ingredients for a Margherita pizza are tomatoes, onions, cheese, basil.",
        "format_instructions": parser.get_format_instructions()
    })


if __name__ == "__main__":
    print(call_json_output_parser())