from langchain_openai import ChatOpenAI
import llm as templates
from llm import GeneralChain
from config import settings


def generate_sql(user_query: str) -> str:
    texttosql_template = templates.TextToSqlTemplate()
    prompt_template = texttosql_template.create_template()

    model = ChatOpenAI(model=settings.OPENAI_MODEL_ID)
    chain = GeneralChain.get_chain(
        llm=model, output_key="text_sql", template=prompt_template
    )

    response = chain.invoke({"query": user_query})
    return response["text_sql"]
