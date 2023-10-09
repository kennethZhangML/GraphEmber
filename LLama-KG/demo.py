import os 
import logging 
import sys 
import openai 

from llama_index import download_loader

from llama_index import (
    KnowledgeGraphIndex, 
    LLMPredictor, 
    ServiceContext, 
    SimpleDirectoryReader
)

# Run the following command to install the necessary modules
# %pip install ipython-ngql nebula3-python

from llama_index.storage.storage_context import StorageContext
from llama_index.graph_stores import NebulaGraphStore
from llama_index.llms import OpenAI

# Two valid ways of initializing global variables for your api key
os.environ["OPENAI_API_KEY"] = "sk-..."
openai.api_key = "sk-..."

# Init LLM of choosing (for this we use 002 Davinci for text completion)
llm = OpenAI(temperature = 0, model = "text-davinci-002")
service_context = ServiceContext.from_defaults(llm = llm, chunk_size_limit = 512)

class NebulaSetup:
    def __init__(self, user, password, address, space_name, edge_types, prop_names, tags):
        self._user = user 
        self.password = password 
        self.address = address 
        self.space_name = space_name 
        self.edge_types = edge_types
        self.prop_names = prop_names 
        self.tags = tags 
        
        self.graph_store = NebulaGraphStore (
            space_name = self.space_name,
            edge_types = self.edge_types,
            rel_prop_names = self.prop_names,
            tags = self.tags
        )

    def StorageContextConstructor(self):
        return StorageContext.from_defaults(graph_store = self.graph_store)
    
    def build_environ(self):
        os.environ["NEBULA_USER"] = "root"
        os.environ["NEBULA_PASSWORD"] = "nebula"  
        os.environ[
            "NEBULA_ADDRESS"
        ] = "127.0.0.1:9669"  

        space_name = "sample_ccp"
        edge_types, rel_prop_names = ["relationship"], [
            "relationship"
        ]  

        tags = ["entity"]



# return KnowledgeGraphIndex.from_documents(
#             documents,
#             storage_context = self.storage_context,
#             max_triplets_per_chunk = 10,
#             service_context = service_context,
#             space_name = self.space_name,
#             edge_types = self.edge_types,
#             rel_prop_names = self.prop_names,
#             tags = self.tags,
#             include_embeddings = True,
#         )