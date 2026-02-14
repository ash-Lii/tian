import os
import dotenv; dotenv.load_dotenv()
from geoalchemy2 import Geometry
# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain.tools import tool
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import init_chat_model


# embedding_model = HuggingFaceEmbeddings(model_name=os.getenv("EMB_MODEL"))
# vector_store = Chroma(
#     collection_name="postgis-3.6-en",
#     embedding_function=embedding_model,
#     persist_directory=os.path.join(os.getenv("DATA_PATH"), "chroma/"),
# )

# @tool(response_format="content_and_artifact")
# def retrieve_context(query: str):
#     """Retrieve information to help answer a query."""
#     retrieved_docs = vector_store.similarity_search(query, k=2)
#     serialized = "\n\n".join(
#         (f"Source: {doc.metadata}\nContent: {doc.page_content}")
#         for doc in retrieved_docs
#     )
#     return serialized, retrieved_docs

def database_tool():
    db_url = os.getenv("DB_URL").replace("...", os.getenv("DB_NAME"))
    database = SQLDatabase.from_uri(db_url)
    toolkit = SQLDatabaseToolkit(db=database,llm=init_chat_model(os.getenv("TOOL_MODEL")), top_k=int(os.getenv("DB_QURY_TOP_K")))
    tools = toolkit.get_tools()
    return tools

def my_tools(tool_names: list):
    tools = []
    # if "vector_store" in tool_names:
    #     tools.append(retrieve_context)
    if "database" in tool_names:
        tools.extend(database_tool())
    return tools
    

if __name__ == "__main__":
    import pprint
    p = pprint.PrettyPrinter(indent=4)
    tools = my_tools(["database"])
    p.pprint(tools)
    pass