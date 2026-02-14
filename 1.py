from langchain_openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
import os


embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=1536)


client = MongoClient(os.getenv("MONGO"))

DB_NAME = "langchain"
COLLECTION_NAME = "vector_store"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain_index_1536"

MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]

vector_store = MongoDBAtlasVectorSearch(
    collection=MONGODB_COLLECTION,
    embedding=embeddings,
    index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
    relevance_score_fn="cosine",
)

# 下面的代码尝试创建向量搜索索引
# vector_store.create_vector_search_index(dimensions=1536)
# print("Vector search index created or already exists.")


import pandas as pd
import random

rand = random.randint(0,547)

databases = "Spider2-main/spider2-snow/resources/databases"
documents = "Spider2-main/spider2-snow/resources/documents"

df = pd.read_json("Spider2-main/spider2-snow/spider2-snow.jsonl", lines=True)

for index, row in df.iloc[rand:rand+1].iterrows():
    
    instance_id = row['instance_id']
    instruction = row['instruction']
    db_id = row['db_id']
    external_knowledge = row['external_knowledge']

print(instance_id)
print(instruction)
print(db_id)
print(external_knowledge)

database = f"{databases}/{db_id}"
knowledge = f"{documents}/{external_knowledge}" if not pd.isna(external_knowledge) else None

print(database)
print(knowledge)



from langchain_core.documents import Document
from uuid import uuid4

# # 创建一个示例文档
# doc = Document(
#     page_content="这是一个测试文档，用于验证MongoDB Atlas Vector Search的功能。"
# )

# docs = [doc]
# ids = [str(uuid4()) for _ in docs]

# # 将文档添加到向量存储中
# vector_store.add_documents(documents=docs, ids=ids)
# print("Document added to vector store.")
# print("Document IDs:", ids)

# 查询向量存储
query = "测试文档"
results = vector_store.similarity_search(query, k=5)
print("Search results:")
for result in results:
    print(result)
