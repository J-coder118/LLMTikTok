from bytewax.outputs import DynamicSink, StatelessSinkPartition
from qdrant_client.http.api_client import UnexpectedResponse
from qdrant_client.models import Batch

from utils.logging import get_logger
from ddb import QdrantDatabaseConnector
from model.base import VectorDBDataModel

logger = get_logger(__name__)


class QdrantOutput(DynamicSink):
    """
    Bytewax class that facilitates the connection to a Qdrant vector DB.
    Inherits DynamicSink because of the ability to create different sink sources (e.g, vector and non-vector collections)
    """

    def __init__(self, connection: QdrantDatabaseConnector, sink_type: str):
        self._connection = connection
        self._sink_type = sink_type

        try:
            self._connection.get_collection(collection_name="cleaned_TicTokProfiles")
        except UnexpectedResponse:
            logger.info(
                "Couldn't access the collection. Creating a new one...",
                collection_name="cleaned_TicTokProfiles",
            )

            self._connection.create_non_vector_collection(
                collection_name="cleaned_TicTokProfiles"
            )

        
        try:
            self._connection.get_collection(collection_name="vector_TicTokProfiles")
        except UnexpectedResponse:
            logger.info(
                "Couldn't access the collection. Creating a new one...",
                collection_name="vector_TicTokProfiles",
            )

            self._connection.create_vector_collection(collection_name="vector_TicTokProfiles")


    def build(self, worker_index: int, worker_count: int) -> StatelessSinkPartition:
        if self._sink_type == "clean":
            return QdrantCleanedDataSink(connection=self._connection)
        elif self._sink_type == "vector":
            return QdrantVectorDataSink(connection=self._connection)
        else:
            raise ValueError(f"Unsupported sink type: {self._sink_type}")


class QdrantCleanedDataSink(StatelessSinkPartition):
    def __init__(self, connection: QdrantDatabaseConnector):
        self._client = connection

    def write_batch(self, items: list[VectorDBDataModel]) -> None:
        payloads = [item.to_payload() for item in items]
        ids, data = zip(*payloads)
        collection_name = get_clean_collection(data_type=data[0]["type"])
        self._client.write_data(
            collection_name=collection_name,
            points=Batch(ids=ids, vectors={}, payloads=data),
        )

        logger.info(
            "Successfully inserted requested cleaned point(s)",
            collection_name=collection_name,
            num=len(ids),
        )


class QdrantVectorDataSink(StatelessSinkPartition):
    def __init__(self, connection: QdrantDatabaseConnector):
        self._client = connection

    def write_batch(self, items: list[VectorDBDataModel]) -> None:
        payloads = [item.to_payload() for item in items]
        ids, vectors, meta_data = zip(*payloads)
        collection_name = get_vector_collection(data_type=meta_data[0]["type"])
        self._client.write_data(
            collection_name=collection_name,
            points=Batch(ids=ids, vectors=vectors, payloads=meta_data),
        )

        logger.info(
            "Successfully inserted requested vector point(s)",
            collection_name=collection_name,
            num=len(ids),
        )


def get_clean_collection(data_type: str) -> str:
    if data_type == "TicTok":
        return "cleaned_TicTokProfiles"
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def get_vector_collection(data_type: str) -> str:
    if data_type == "TicTok":
        return "vector_TicTokProfiles"
    else:
        raise ValueError(f"Unsupported data type: {data_type}")
