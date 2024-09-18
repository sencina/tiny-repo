from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from translator import parse_relation, translate

from env import OPENAI_API_KEY

model = ChatOpenAI(model="gpt-4o", temperature=0.7,api_key=OPENAI_API_KEY)

system_prompt = system_prompt = """
AI is responsible for parsing a dialogue containing questions and answers and generating a list of questions based on the content. The questions should be engaging, interactive, and relevant to the conversation's context. The whole chat has to be conversational and engaging, with the AI acting as a teacher conducting an interactive training session. The AI should provide theoretical knowledge, definitions, and motivational questions to encourage student participation.

The max amount of sequential ACTIONS is 3. After that a question engaging the user must be asked. That question must be sequential, making the flow interactive and not take different paths.

There are three types of question_type: MULTIPLECHOICE, SINGLECHOICE, and ACTION. There are two types of `type`: QUESTION and ACTION.

- Type ACTION is used to provide context, and Type QUESTION is used to display question options. 
- ACTION must always be followed by a QUESTION or another ACTION, but ultimately, the sequence must end with a QUESTION.
- ACTIONS cannot include options. 
- The maximum amount of characters per ACTION is 150 characters.

Remember, each question should consist of an ACTION with the question content and a QUESTION with the possible answers. For example: 
- ACTION: "What is the capital of France?" 
- QUESTION: "a) Paris b) London c) Berlin d) Madrid" (The question name should be an empty string.)

This is mandatory to fulfill the requirements of the task above, becuase it is used after in a computer program and that the QUESTION name is always empty as the name of the question is passed in the ACTION before.

If an ACTION's content is lengthy, it should be split into multiple ACTION entries. Make the flow interactive, avoiding long sequences of ACTIONs without questions.

Ensure each question is directly related to the previous content to maintain logical, sequential flow. Include at least one MULTIPLECHOICE question to enhance engagement and assess comprehension. For example, when the dialogue says "Are you ready?!", it should be followed by a SINGLECHOICE question with only positive options like "Yes!" or "Absolutely!"

At the end of the conversation, the AI should provide a summary of key points and encourage further exploration of the topic, ending with a goodbye message.

Interactive questions must not open new paths but instead focus on continuing the current explanation or segment. For example, if the limit is reached, provide options like "Continue with the current topic" or "Learn about the next concept" to ensure a smooth flow without diverging into alternative topics.

Formatting Instructions: {format_instructions}
"""

def call_json_output_parser(phrase):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{phrase}")
    ])

    class Question(BaseModel):
        id: str = Field(description="the id of the question (numeric incremental)")
        type: str = Field(description="the type of the question, it can be 'QUESTION' or 'ACTION'")
        name: str = Field(description="the content of the question")
        question_type: str = Field(description="the type of the question, it can be 'SINGLECHOICE','MULTIPLECHOICE' or 'ACTION'")
        options: list[str] = Field(description="the options of the question, it must be a list of strings. If the question is not a multiple choice question, it must be an empty list")
        answer: list[str] = Field(description="List of the options that are correct")

    class Relation(BaseModel):
        parent: str = Field(description="the id of the parent question")
        child: str = Field(description="the id of the child question")

    class Response(BaseModel):
        id: str = Field(description="the id of the response, should be an emty string")
        type: str = Field(description="the type of the response, should be DYNAMIC")
        initial: str = Field(description="the id of the initial question/action")
        elements: list[Question] = Field(description="the generated questions (must be question type as passed)")
        relations: list[Relation] = Field(description="the relations between the questions, (order of the questions)")
    
    parser = JsonOutputParser(pydantic_object=Response)

    chain = prompt | model | parser
    
    return chain.invoke({
        "phrase":phrase,
        "format_instructions": parser.get_format_instructions()
    })

if __name__ == "__main__":
    phrase =  """
        Profesor: Hello there!
Profesor: Today, we're going to dive into a fascinating topic in software design: Creational Patterns, with a particular focus on the Builder and Factory Method patterns.
Profesor: Are you ready to explore these concepts?
Alumno: Absolutely, let's go!
Profesor: Great! To start, it's important to understand that creational patterns deal with object creation mechanisms, trying to create objects in a manner suitable to the situation. By abstracting the process of object creation, these patterns provide different ways to associate an interface with its implementation transparently at instantiation.
Profesor: Creational patterns ensure that your system is written in terms of interfaces, not implementations. This makes your system more flexible and reusable.
Alumno: That sounds useful. Can you explain more about how this works?
Profesor: Sure! Let's start with an overview of some common creational patterns: Abstract Factory, Builder, Factory Method, Prototype, and Singleton. Each of these patterns offers a unique way to create objects, providing various degrees of flexibility and complexity.
Profesor: For instance, the Factory Method pattern makes a design more customizable and only a little more complicated. It requires a new operation rather than new classes, making it a popular choice for object creation.
Alumno: So, when would you use Factory Method over other patterns?
Profesor: Good question! You'd use Factory Method when the class that gets instantiated can change or when instantiation takes place in an operation that subclasses can easily override, such as an initialization operation.
Profesor: On the other hand, designs using Abstract Factory, Prototype, or Builder are even more flexible but also more complex. Often, designs start with Factory Method and evolve towards these other patterns as more flexibility is needed.
Alumno: Got it. Can we focus on the Builder pattern now?
Profesor: Absolutely! The Builder pattern is particularly useful when you need to construct a complex object step by step. It separates the construction of a complex object from its representation, allowing the same construction process to create different representations.
Profesor: Think of it like building a house. You have different phases: laying the foundation, constructing the walls, and adding the roof. The Builder pattern allows you to use the same process to build different types of houses.
Alumno: That makes sense. What are some real-world applications of the Builder pattern?
Profesor: The Builder pattern is often used in scenarios where an object requires numerous steps to be created. For example, it's commonly used in constructing objects that require multiple configurations, like assembling a car with different features or creating a complex document with various components.
Profesor: Now, let's switch gears and talk about the Factory Method pattern.
Alumno: Sure, I'm ready!
Profesor: The Factory Method pattern defines an interface for creating an object but lets subclasses alter the type of objects that will be created. This pattern promotes loose coupling by eliminating the need to bind application-specific classes into your code.
Profesor: For example, consider a logistics application that can handle different types of transportation: trucks, ships, and planes. The Factory Method allows you to define a method for creating these transport objects, and each subclass can implement the method to instantiate the appropriate transport type.
Alumno: Interesting. How does the Factory Method pattern compare to the Builder pattern?
Profesor: Great question! While both patterns deal with object creation, they serve different purposes. The Builder pattern is best suited for constructing complex objects step by step, whereas the Factory Method pattern is ideal for creating objects without specifying the exact class of the object that will be created.
Profesor: In summary, the Builder pattern focuses on constructing complex objects, and the Factory Method pattern focuses on creating objects without specifying their concrete classes.
Alumno: I see the differences now. Can we test our understanding with a quiz?
Profesor: Of course! Let's do a quick multiple-choice quiz to reinforce what we've learned.
Profesor: Quiz:
Which pattern is best suited for creating complex objects step by step?
a) Factory Method
b) Builder
c) Singleton
d) Prototype
Alumno: b) Builder
Profesor: Correct! Next question.
Which pattern defines an interface for creating an object but lets subclasses alter the type of objects that will be created?
a) Abstract Factory
b) Builder
c) Factory Method
d) Prototype
Alumno: c) Factory Method
Profesor: Well done! Last question.
Which pattern promotes loose coupling by eliminating the need to bind application-specific classes into your code?
a) Singleton
b) Builder
c) Prototype
d) Factory Method
Alumno: d) Factory Method
Profesor: Excellent! You've got a good grasp of these concepts.
Profesor: In conclusion, understanding and applying creational patterns like Builder and Factory Method can significantly enhance the flexibility and reusability of your software designs. By abstracting the object creation process, these patterns allow you to create systems that are easier to maintain and extend.
Profesor: I hope you enjoyed this session and found it informative. Keep exploring and applying these patterns in your projects to see their benefits firsthand.
Profesor: See you next time!
Alumno: Thank you! This was very insightful.

"""
    res = call_json_output_parser(phrase)
    mapped_questions = list(map(translate,res["elements"]))
    parsed_relations = list(map(parse_relation,res["relations"]))
    output = {
        "elements": mapped_questions,
        "relations": parsed_relations
    }
    print(output)