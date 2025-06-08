def add_episodic_memory(messages, vdb_client):

    # Format Messages
    conversation = format_conversation(messages)

    # Create Reflection
    reflection = reflect.invoke({"conversation": conversation})

    # Load Database Collection
    episodic_memory = vdb_client.collections.get("episodic_memory")

    # Insert Entry Into Collection
    episodic_memory.data.insert(
        {
            "conversation": conversation,
            "context_tags": reflection["context_tags"],
            "conversation_summary": reflection["conversation_summary"],
            "what_worked": reflection["what_worked"],
            "what_to_avoid": reflection["what_to_avoid"],
        }
    )


def episodic_recall(query, vdb_client):

    # Load Database Collection
    episodic_memory = vdb_client.collections.get("episodic_memory")

    # Hybrid Semantic/BM25 Retrieval
    memory = episodic_memory.query.hybrid(
        query=query,
        alpha=0.5,
        limit=1,
    )

    return memory


query = "Talking about my name"

memory = episodic_recall(query, vdb_client)

memory.objects[0].properties


def episodic_system_prompt(query, vdb_client):
    # Get new memory
    memory = episodic_recall(query, vdb_client)

    current_conversation = memory.objects[0].properties["conversation"]
    # Update memory stores, excluding current conversation from history
    if current_conversation not in conversations:
        conversations.append(current_conversation)
    # conversations.append(memory.objects[0].properties['conversation'])
    what_worked.update(memory.objects[0].properties["what_worked"].split(". "))
    what_to_avoid.update(memory.objects[0].properties["what_to_avoid"].split(". "))

    # Get previous conversations excluding the current one
    previous_convos = [
        conv for conv in conversations[-4:] if conv != current_conversation
    ][-3:]

    # Create prompt with accumulated history
    episodic_prompt = f"""You are a helpful AI Assistant. Answer the user's questions to the best of your ability.
    You recall similar conversations with the user, here are the details:
    
    Current Conversation Match: {memory.objects[0].properties['conversation']}
    Previous Conversations: {' | '.join(previous_convos)}
    What has worked well: {' '.join(what_worked)}
    What to avoid: {' '.join(what_to_avoid)}
    
    Use these memories as context for your response to the user."""

    return SystemMessage(content=episodic_prompt)
