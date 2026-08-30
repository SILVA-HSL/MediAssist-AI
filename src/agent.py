from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import ToolMessage
import json

from tools.hospital_tools import (
    get_available_beds,
    get_equipment_status,
    create_maintenance_ticket
)

from tools.rag_tools import (
    search_hospital_documents
)


#system prompt for the LLM
SYSTEM_PROMPT = """
You are MediAssist, a hospital AI assistant.

You help users with hospital knowledge and hospital
operational tasks.

For hospital policies, procedures, and information contained
in hospital documents, use the search_hospital_documents tool.

The available hospital knowledge includes:

- Emergency Response Procedure
- Medication Policy
- Patient Admission Procedure

When using search_hospital_documents:

- Treat retrieved hospital documents as the source of truth.
- Use only information contained in the retrieved documents.
- Do not add information from your general knowledge.
- Do not invent medical procedures.
- If the information cannot be found in the provided documents,
  clearly state that it could not be found.

For current operational information, use the appropriate
operational tool.

Available operational tools:

1. get_available_beds
2. get_equipment_status
3. create_maintenance_ticket

Use get_available_beds for current bed availability.

Use get_equipment_status for current equipment status.

Use create_maintenance_ticket when a user reports an equipment
problem.

A maintenance ticket requires:

- Equipment name
- Location
- Issue description

If required information is missing, ask the user for it.

Never invent database information.

Only claim an action was completed if the corresponding tool
successfully completed the action.

Do not claim that staff were notified unless a notification
tool was actually used.
"""


#LLM
model = ChatOllama(
    model="llama3.2",
    temperature=0
)

tools = [
    get_available_beds,
    get_equipment_status,
    create_maintenance_ticket,
    search_hospital_documents
]


#Create MediAssist Agent
agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

#Reusable Chat Function
# def chat_with_agent(message: str):

#     result = agent.invoke(
#         {
#             "messages": [
#                 {
#                     "role": "user",
#                     "content": message
#                 }
#             ]
#         }
#     )

#     return result

#========================================

def chat_with_agent(message: str):

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ]
        }
    )

    sources = []
    ticket_id = None
    ticket_status = None
    used_tools = []

    for msg in result["messages"]:

        if isinstance(msg, ToolMessage):

            tool_name = getattr(msg, "name", None)

            if tool_name:
                used_tools.append(tool_name)

            # -----------------------------
            # RAG RESULT
            # -----------------------------

            if tool_name == "search_hospital_documents":

                try:
                    rag_result = json.loads(msg.content)

                    sources = rag_result.get(
                        "sources",
                        []
                    )

                except (json.JSONDecodeError, TypeError):
                    sources = []

            # -----------------------------
            # MAINTENANCE RESULT
            # -----------------------------

            elif tool_name == "create_maintenance_ticket":

                try:
                    ticket_result = json.loads(msg.content)

                    if isinstance(ticket_result, dict):

                        ticket_id = ticket_result.get(
                            "ticket_id"
                        )

                        ticket_status = ticket_result.get(
                            "status"
                        )

                except (json.JSONDecodeError, TypeError):
                    pass

    final_response = result["messages"][-1].content

    return {
        "response": final_response,
        "sources": sources,
        "ticket_id": ticket_id,
        "ticket_status": ticket_status,
        "tools": used_tools
    }





# model_with_tools = model.bind_tools(tools)

# #Create tool lookup
# tool_map = {
#     tool.name: tool
#     for tool in tools
# }

# #User question
# # question = "Are there any ICU beds available?"
# # question = "What is the status of the MRI machine?"
# question = "The X-Ray machine in Radiology Room 3 is not working."


# #Ask the LLM
# response = model_with_tools.invoke(question)

# print("\nLLM TOOL CALL:")
# print(response.tool_calls)

# #Execute selected tools

# tool_results = []
# tool_messages = []

# for tool_call in response.tool_calls:

#     tool_name = tool_call["name"]
#     tool_args = tool_call["args"]

#     tool = tool_map[tool_name]

#     result = tool.invoke(tool_args)

#     tool_message = ToolMessage(
#         content=str(result),
#         tool_call_id=tool_call["id"]
#     )

#     tool_messages.append(tool_message)


# #generate final response with tool results
# final_response = model_with_tools.invoke(
#     [
#         {
#             "role": "user",
#             "content": question
#         },
#         response,
#         *tool_messages
#     ]
# )

# print("\nFINAL ANSWER:")
# print(final_response.content)