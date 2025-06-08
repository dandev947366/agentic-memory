from prompts.procedural import procedural_prompt


def episodic_system_prompt(query, vdb_client):
    # Get new memory
    memory = episodic_recall(query, vdb_client)

    # Load Existing Procedural Memory Instructions
    with open("./procedural_memory.txt", "r") as content:
        procedural_memory = content.read()

    # Get current conversation
    current_conversation = memory.objects[0].properties["conversation"]

    # Update memory stores, excluding current conversation from history
    if current_conversation not in conversations:
        conversations.append(current_conversation)
    what_worked.update(memory.objects[0].properties["what_worked"].split(". "))
    what_to_avoid.update(memory.objects[0].properties["what_to_avoid"].split(". "))

    # Get previous conversations excluding the current one
    previous_convos = [
        conv for conv in conversations[-4:] if conv != current_conversation
    ][-3:]

    # Create prompt with accumulated history
    episodic_prompt = f"""You are a helpful AI Assistant. Answer the user's questions to the best of your ability.
    You recall similar conversations with the user, here are the details:
    
    Current Conversation Match: {current_conversation}
    Previous Conversations: {' | '.join(previous_convos)}
    What has worked well: {' '.join(what_worked)}
    What to avoid: {' '.join(what_to_avoid)}
    
    Use these memories as context for your response to the user.
    
    Additionally, here are 10 guidelines for interactions with the current user: {procedural_memory}"""

    return SystemMessage(content=episodic_prompt)


def procedural_memory_update(what_worked, what_to_avoid):

    # Load Existing Procedural Memory Instructions
    with open("./procedural_memory.txt", "r") as content:
        current_takeaways = content.read()

    # Generate New Procedural Memory
    procedural_memory = llm.invoke(procedural_prompt)

    # Write to File
    with open("./procedural_memory.txt", "w") as content:
        content.write(procedural_memory.content)

    return


# prompt = procedural_memory_update(what_worked, what_to_avoid)
