import pandas as pd
from langchain_openai import ChatOpenAI
from llm.chain import GeneralChain
from evaluation import evaluate_rag
from llm.prompt_templates import InferenceTemplate
# from monitoring import PromptMonitoringManager
from rag.retriever import VectorRetriever
from textTosql.txtSql import  csvRetriever
from router.router import routeLayer
from feature_pipeline.config import settings


class LLMTikTok:
    def __init__(self) -> None:
        # self.qwak_client = RealTimeClient(
        #     model_id=settings.QWAK_DEPLOYMENT_MODEL_ID,
        #     model_api=settings.QWAK_DEPLOYMENT_MODEL_API,
        # )
        # self.prompt = InferenceTemplate().create_template()
        self.model = ChatOpenAI(
            model=settings.OPENAI_MODEL_ID,
            api_key=settings.OPENAI_API_KEY,
            temperature=0,
        )
        self.chain = GeneralChain().get_chain(
            llm=self.model, output_key="answer"
        )
        self.template = InferenceTemplate()
        # self.prompt_monitoring_manager = PromptMonitoringManager()

    def generate(
        self,
        query: str,
        mechanism: str,
        enable_rag: bool = False,
        enable_evaluation: bool = False,
        enable_monitoring: bool = True,
    ) -> dict:
        prompt_template = self.template.create_template(enable_rag=enable_rag)
        prompt_template_variables = {
            "question": query,
        }

        if mechanism == "SemanticRAG" and enable_rag is True:
            retriever = VectorRetriever(query=query)
            hits = retriever.retrieve_top_k(
                k=settings.TOP_K, to_expand_to_n_queries=settings.EXPAND_N_QUERY
            )
            context = retriever.rerank(hits=hits, keep_top_k=settings.KEEP_TOP_K)
            prompt_template_variables["context"] = context

            prompt = prompt_template.format(question=query, context=context)
        elif mechanism == "TextToSQL" and enable_rag is True:
            context = csvRetriever.generate_sql(query=query)
            prompt_template_variables["context"] = context

            prompt = prompt_template.format(question=query, context=context)
        else:
            prompt = prompt_template.format(question=query)

        input_ = pd.DataFrame([{"instruction": prompt}]).to_json()

        response: list[dict] = self.chain.invoke(input_)##self.qwak_client.predict(input_)
        answer = response[0]["content"][0]

        if enable_evaluation is True:
            evaluation_result = evaluate_rag(query=query, output=answer)
        else:
            evaluation_result = None

        if enable_monitoring is True:
            if evaluation_result is not None:
                metadata = {"llm_evaluation_result": evaluation_result}
            else:
                metadata = None

            # self.prompt_monitoring_manager.log(
            #     prompt=prompt,
            #     prompt_template=prompt_template.template,
            #     prompt_template_variables=prompt_template_variables,
            #     output=answer,
            #     metadata=metadata,
            # )
            self.prompt_monitoring_manager.log_chain(
                query=query, response=answer, eval_output=evaluation_result
            )

        return {"answer": answer, "llm_evaluation_result": evaluation_result}
