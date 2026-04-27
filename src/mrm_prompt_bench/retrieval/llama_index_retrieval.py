# Install llama-index if not already installed
# !pip install llama-index llama-cpp-python

from llama_index import SimpleDirectoryReader, VectorStoreIndex, ServiceContext
from llama_index.llms import OpenAI
from llama_index.node_parser import SimpleNodeParser

# Step 1: Load the document (Assuming it's a text file or PDF)
documents = SimpleDirectoryReader("./data").load_data()  # Ensure document is placed in ./data folder

# Step 2: Parse the document into nodes (chunks for retrieval)
parser = SimpleNodeParser()
nodes = parser.get_nodes_from_documents(documents)

# Step 3: Create an index for the document
service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo"))  # Use LlamaIndex with OpenAI model
index = VectorStoreIndex(nodes, service_context=service_context)

# Step 4: Query the document
query_engine = index.as_query_engine()
query = "What are the key validation assessment instructions for the ReAct algorithm?"
response = query_engine.query(query)

# Print the response
print(response)