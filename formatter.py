def format_conversation(messages):
    """
    Convert a list of messages into a formatted plain text conversation string.
    Each message is expected to have a 'type' and 'content' attribute.
    """

    formatted_lines = []
    for msg in messages:
        speaker = (
            "User" if msg.type == "human" else "AI" if msg.type == "ai" else "System"
        )
        formatted_lines.append(f"{speaker}: {msg.content}")

    # Join all lines with newlines
    return "\n".join(formatted_lines)
