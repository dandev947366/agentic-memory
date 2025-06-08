from weaviate.classes.config import Property, DataType, Configure, Tokenization
from episodic_helper import add_episodic_memory, episodic_recall, episodic_system_prompt

vdb_client.collections.create(
    name="episodic_memory",
    description="Collection containing historical chat interactions and takeaways.",
    vectorizer_config=[
        Configure.NamedVectors.text2vec_ollama(
            name="title_vector",
            source_properties=["title"],
            api_endpoint="http://host.docker.internal:11434",  # If using Docker, use this to contact your local Ollama instance
            model="nomic-embed-text",
        )
    ],
    properties=[
        Property(name="conversation", data_type=DataType.TEXT),
        Property(name="context_tags", data_type=DataType.TEXT_ARRAY),
        Property(name="conversation_summary", data_type=DataType.TEXT),
        Property(name="what_worked", data_type=DataType.TEXT),
        Property(name="what_to_avoid", data_type=DataType.TEXT),
    ],
)


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

    # Add current user message
    messages.append(user_message)

    # Pass Entire Message Sequence to LLM to Generate Response
    response = llm.invoke(messages)
    print("\nAI Message: ", response.content)

    # Add AI's Response to Message List
    messages.append(response)

# Looking into our Memory

for i in range(len(messages)):
    print(f"\nMessage {i+1} - {messages[i].type.upper()}: ", messages[i].content)
    i += 1
