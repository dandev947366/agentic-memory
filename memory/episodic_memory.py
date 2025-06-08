from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from formatter import format_conversation
from prompts.episodic import academic_research_reflection_prompt
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

# Initialize local model via Ollama
llm = ChatOllama(model="llama3", temperature=0.7)

# Define System Prompt
system_prompt = SystemMessage(
    content="You are a helpful AI Assistant. Answer the User's queries succinctly in one sentence."
)

# Initialize message history
messages = [system_prompt]

while True:
    # Get user input
    user_input = input("\nUser: ")

    if user_input.lower() == "exit":
        break

    user_message = HumanMessage(content=user_input)
    messages.append(user_message)

    # Generate response from local model
    response = llm.invoke(messages)

    print("\nAI Message:", response.content)

    # Add AI response to history
    messages.append(response)

# Print the full chat history
for i, msg in enumerate(messages, start=1):
    print(f"\nMessage {i} - {msg.type.upper()}: {msg.content}")

# Reflect on the conversation after chat ends
reflection_prompt = ChatPromptTemplate.from_template(
    academic_research_reflection_prompt
)
reflect = reflection_prompt | llm | JsonOutputParser()

conversation_text = format_conversation(messages)
reflection = reflect.invoke({"conversation": conversation_text})

print("\nReflection Output:")
print(reflection)
