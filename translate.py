# translation_module.py

from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

translation_template = """
Translate the following sentence into {language} or if it is in {language} return in english , return ONLY the translation, nothing else.

Sentence: {sentence}
"""

output_parser = StrOutputParser()
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash-latest", google_api_key=os.environ["GOOGLE_API_KEY"]
)
translation_prompt = ChatPromptTemplate.from_template(translation_template)

translation_chain = (
    {"language": RunnablePassthrough(), "sentence": RunnablePassthrough()}
    | translation_prompt
    | llm
    | output_parser
)


def translate(sentence, language="French"):
    data_input = {"language": language, "sentence": sentence}
    translation = translation_chain.invoke(data_input)
    return translation
