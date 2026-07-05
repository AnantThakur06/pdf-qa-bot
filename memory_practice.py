import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

model = ChatGroq(model="llama-3.3-70b-versatile")

# This list IS the memory - it holds the whole conversation
conversation = []

print("Chat with memory! Type 'quit' to exit.")

while True:
    user_input = input("\nYou: ")

    if user_input.lower() == "quit":
        break

    # Add the user's message to memory
    conversation.append(HumanMessage(content=user_input))

    # Send the WHOLE conversation (memory) to the model
    response = model.invoke(conversation)

    # Add the AI's reply to memory too
    conversation.append(AIMessage(content=response.content))

    print("Bot:", response.content)