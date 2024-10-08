from langchain_openai import ChatOpenAI

import llm as templates
from llm.chain import GeneralChain
from config import settings


def evaluate(query: str, context: list[str], output: str) -> str:
    evaluation_template = templates.RAGEvaluationTemplate()
    prompt_template = evaluation_template.create_template()

    model = ChatOpenAI(model=settings.OPENAI_MODEL_ID)
    chain = GeneralChain.get_chain(
        llm=model, output_key="rag_eval", template=prompt_template
    )

    response = chain.invoke({"query": query, "context": context, "output": output})

    return response["rag_eval"]
