from langchain_ollama import ChatOllama
from langchain_core.messages import ToolMessage

from tools.hospital_tools import (
    get_available_beds,
    get_equipment_status,
    create_maintenance_ticket
)

model = ChatOllama(
    model="llama3.2",
    temperature=0
)

tools = [
    get_available_beds,
    get_equipment_status,
    create_maintenance_ticket
]

model_with_tools = model.bind_tools(tools)

# response = model_with_tools.invoke(
#     "Are there any ICU beds available?"
# )

# print(response)

#================================


# questions = [
#     "Are there any ICU beds available?",
#     "What is the status of the MRI machine?",
#     "The ECG machine in Room 3 is not working."
# ]


# for question in questions:

#     print("\n" + "=" * 60)
#     print("USER:", question)

#     response = model_with_tools.invoke(question)

#     print("\nLLM RESPONSE:")
#     print(response)

#     print("\nTOOL CALLS:")
#     print(response.tool_calls)

#================================

#Create tool lookup
tool_map = {
    tool.name: tool
    for tool in tools
}

#User question
# question = "Are there any ICU beds available?"
# question = "What is the status of the MRI machine?"
question = "The X-Ray machine in Radiology Room 3 is not working."


#Ask the LLM
response = model_with_tools.invoke(question)

print("\nLLM TOOL CALL:")
print(response.tool_calls)

#Execute selected tools

tool_results = []
tool_messages = []

for tool_call in response.tool_calls:

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    tool = tool_map[tool_name]

    result = tool.invoke(tool_args)

    tool_message = ToolMessage(
        content=str(result),
        tool_call_id=tool_call["id"]
    )

    tool_messages.append(tool_message)


#generate final response with tool results
final_response = model_with_tools.invoke(
    [
        {
            "role": "user",
            "content": question
        },
        response,
        *tool_messages
    ]
)

print("\nFINAL ANSWER:")
print(final_response.content)