import json
from llm import GroqClient
from tools import tools_schema, TOOL_FUNCTIONS

class AutonomousAgent:
    def __init__(self, system_prompt: str = None):
        self.llm = GroqClient()
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})
        else:
            self.history.append({
                "role": "system", 
                "content": "You are an autonomous software engineering agent. You can understand issues, navigate repositories, use tools intelligently, manage context, and recover from failures. Always verify your changes."
            })

    def run(self, task: str):
        self.history.append({"role": "user", "content": task})
        
        while True:
            response = self.llm.chat_completion(
                messages=self.history,
                tools=tools_schema
            )
            
            if not response or not response.choices:
                print("Error getting response from LLM.")
                break
                
            response_message = response.choices[0].message
            
            # Add assistant's response (or tool call) to history
            self.history.append(response_message)
            
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    print(f"Executing tool: {function_name} with args: {function_args}")
                    
                    if function_name in TOOL_FUNCTIONS:
                        function_to_call = TOOL_FUNCTIONS[function_name]
                        function_response = function_to_call(**function_args)
                        
                        self.history.append(
                            {
                                "tool_call_id": tool_call.id,
                                "role": "tool",
                                "name": function_name,
                                "content": str(function_response),
                            }
                        )
                    else:
                        print(f"Unknown tool requested: {function_name}")
            else:
                # If no tool calls, the agent has responded to the user
                print(f"Agent Output: {response_message.content}")
                break
