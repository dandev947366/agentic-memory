from chunking_evaluation.chunking import RecursiveTokenChunker
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./CoALA_Paper.pdf")
pages = []
for page in loader.load():
    pages.append(page)

# Combine all page contents into one string
document = " ".join(page.page_content for page in pages)

# Set up the chunker with your specified parameters
recursive_character_chunker = RecursiveTokenChunker(
    chunk_size=800,
    chunk_overlap=0,
    length_function=len,
    separators=["\n\n", "\n", ".", "?", "!", " ", ""],
)

# Split the combined text
recursive_character_chunks = recursive_character_chunker.split_text(document)

vdb_client.collections.create(
    name="CoALA_Paper",
    description="Collection containing split chunks from the CoALA Paper",
    vectorizer_config=[
        Configure.NamedVectors.text2vec_ollama(
            name="title_vector",
            source_properties=["title"],
            api_endpoint="http://host.docker.internal:11434",  # If using Docker, use this to contact your local Ollama instance
            model="nomic-embed-text",
        )
    ],
    properties=[
        Property(name="chunk", data_type=DataType.TEXT),
    ],
)
# Load Database Collection
coala_collection = vdb_client.collections.get("CoALA_Paper")

for chunk in recursive_character_chunks:
    # Insert Entry Into Collection
    coala_collection.data.insert(
        {
            "chunk": chunk,
        }
    )


def semantic_recall(query, vdb_client):

    # Load Database Collection
    coala_collection = vdb_client.collections.get("CoALA_Paper")

    # Hybrid Semantic/BM25 Retrieval
    memories = coala_collection.query.hybrid(
        query=query,
        alpha=0.5,
        limit=15,
    )

    combined_text = ""

    for i, memory in enumerate(memories.objects):
        # Add chunk separator except for first chunk        if i > 0:

        # Add chunk number and content
        combined_text += f"\nCHUNK {i+1}:\n"
        combined_text += memory.properties["chunk"].strip()

    return combined_text


memories = semantic_recall("What are the four kinds of memory", vdb_client)

print(memories)


def semantic_rag(query, vdb_client):

    memories = semantic_recall(query, vdb_client)

    semantic_prompt = f""" If needed, Use this grounded context to factually answer the next question.
    Let me know if you do not have enough information or context to answer a question.
    
    {memories}
    """

    return HumanMessage(semantic_prompt)


message = semantic_rag("What are the four kinds of memory", vdb_client)
print(message)
# Simple storage for accumulated memories
conversations = []
what_worked = set()
what_to_avoid = set()

# Start Storage for Historical Message History
messages = []

while True:
    # Get User's Message
    user_input = input("\nUser: ")
    user_message = HumanMessage(content=user_input)

    # Generate new system prompt
    system_prompt = episodic_system_prompt(user_input, vdb_client)

    # Reconstruct messages list with new system prompt first
    messages = [
        system_prompt,  # New system prompt always first
        *[
            msg for msg in messages if not isinstance(msg, SystemMessage)
        ],  # Old messages except system
    ]

    if user_input.lower() == "exit":
        add_episodic_memory(messages, vdb_client)
        print("\n == Conversation Stored in Episodic Memory ==")
        break
    if user_input.lower() == "exit_quiet":
        print("\n == Conversation Exited ==")
        break

    # Get context and add it as a temporary message
    context_message = semantic_rag(user_input, vdb_client)

    # Pass messages + context + user input to LLM
    response = llm.invoke([*messages, context_message, user_message])
    print("\nAI Message: ", response.content)

    # Add only the user message and response to permanent history
    messages.extend([user_message, response])
print(format_conversation(messages))
print(context_message.content)

# Simple storage for accumulated memories
conversations = []
what_worked = set()
what_to_avoid = set()

# Start Storage for Historical Message History
messages = []

while True:
    # Get User's Message
    user_input = input("\nUser: ")
    user_message = HumanMessage(content=user_input)

    # Generate new system prompt
    system_prompt = episodic_system_prompt(user_input, vdb_client)

    # Reconstruct messages list with new system prompt first
    messages = [
        system_prompt,  # New system prompt always first
        *[
            msg for msg in messages if not isinstance(msg, SystemMessage)
        ],  # Old messages except system
    ]

    if user_input.lower() == "exit":
        add_episodic_memory(messages, vdb_client)
        print("\n == Conversation Stored in Episodic Memory ==")
        procedural_memory_update(what_worked, what_to_avoid)
        print("\n== Procedural Memory Updated ==")
        break
    if user_input.lower() == "exit_quiet":
        print("\n == Conversation Exited ==")
        break

    # Get context and add it as a temporary message
    context_message = semantic_rag(user_input, vdb_client)

    # Pass messages + context + user input to LLM
    response = llm.invoke([*messages, context_message, user_message])
    print("\nAI Message: ", response.content)

    # Add only the user message and response to permanent history
    messages.extend([user_message, response])
print(format_conversation(messages))
print(system_prompt.content)
print(context_message.content)
