import streamlit as st
import os
import json
import tempfile
from llm import GroqClient
from tools import tools_schema, TOOL_FUNCTIONS

# --- UI Configuration ---
st.set_page_config(page_title="AI Harness (Antigravity Clone)", layout="wide")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are an elite autonomous software engineering agent. You are the core intelligence of a sophisticated Coding Harness.\n\n"
        "CORE RESPONSIBILITIES & INSTRUCTIONS:\n"
        "1. ORCHESTRATION & PLANNING: Do not guess randomly. ALWAYS run `find_files` on the root directory ('.') first to map out the codebase.\n"
        "2. TARGET IDENTIFICATION: If the user asks you to fix issues, they are referring to FATAL syntax and logic errors that prevent compilation. Do not try to fix the Python files of this agent harness itself.\n"
        "3. NO PEDANTIC REFACTORING: DO NOT refactor working code. DO NOT fix 'bad practices' like Variable Length Arrays (VLAs) or shadowing unless they actually throw a hard compiler error. Only fix broken code.\n"
        "4. TOOL USAGE: Read the code using `read_file`. If you spot a fatal error, use `write_file` to completely overwrite the file with the corrected code.\n"
        "5. COMPILER/RUNTIME VERIFICATION (CRITICAL): After editing a file, you MUST use `execute_command` to run the appropriate compiler (e.g., `g++` for C++) to verify it compiles. If it throws an error, read the output, fix the file, and test it again until it succeeds.\n"
        "6. RECOVERY: If a tool fails, adapt and try a different solution."
    )
if "project_dir" not in st.session_state:
    st.session_state.project_dir = os.getcwd()

# --- Sidebar UI ---
with st.sidebar:
    st.title("🚀 AI Harness Control")
    
    st.subheader("Session Management")
    if st.button("🆕 New Session", use_container_width=True):
        st.session_state.messages = []
        st.toast("Started a new session!")
        st.rerun()
        
    st.divider()
    
    st.subheader("Project Settings")
    
    # Text input for direct path pasting
    new_project_path = st.text_input(
        "Active Project Path:", 
        value=st.session_state.project_dir,
        help="Paste an absolute path here and press Enter."
    )
    
    if new_project_path != st.session_state.project_dir:
        if os.path.isdir(new_project_path):
            st.session_state.project_dir = new_project_path
            st.session_state.messages = []
            st.toast("Active project updated!")
            st.rerun()
        else:
            st.error("Invalid path. Directory does not exist.")
            
    with st.expander("📁 Browse Filesystem"):
        if "nav_dir" not in st.session_state:
            st.session_state.nav_dir = st.session_state.project_dir
            
        current_nav_dir = st.session_state.nav_dir
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("⬆️ Up", help="Go up one directory"):
                st.session_state.nav_dir = os.path.dirname(current_nav_dir)
                st.rerun()
        with col2:
            st.code(current_nav_dir, language="bash")
            
        try:
            dirs = [d for d in os.listdir(current_nav_dir) if os.path.isdir(os.path.join(current_nav_dir, d))]
            dirs.sort()
            selected_dir = st.selectbox("Open folder:", ["(current)"] + dirs, label_visibility="collapsed")
            
            if selected_dir != "(current)":
                st.session_state.nav_dir = os.path.join(current_nav_dir, selected_dir)
                st.rerun()
                
            if st.button("✅ Use This Folder", type="primary", use_container_width=True):
                st.session_state.project_dir = current_nav_dir
                st.session_state.messages = []
                st.toast(f"Active project set to {current_nav_dir}")
                st.rerun()
        except Exception as e:
            st.error(f"Cannot read directory: {e}")
    
    if st.button("⚡ Create Temporary Project", use_container_width=True):
        temp_dir = tempfile.mkdtemp(prefix="ai_harness_")
        st.session_state.project_dir = temp_dir
        st.session_state.messages = []
        st.toast("Temporary project created!")
        st.rerun()

    st.divider()
    
    st.subheader("Prompt Management")
    new_system_prompt = st.text_area(
        "System Prompt", 
        value=st.session_state.system_prompt,
        height=200
    )
    if new_system_prompt != st.session_state.system_prompt:
        st.session_state.system_prompt = new_system_prompt
        st.toast("System prompt updated!")

# --- Main Chat UI ---
st.title(f"💻 AI Coding Agent ({os.path.basename(st.session_state.project_dir)})")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    elif msg["role"] == "assistant":
        if msg.get("content"):
            with st.chat_message("assistant"):
                st.markdown(msg["content"])
    elif msg["role"] == "tool":
        with st.chat_message("assistant"):
            with st.expander(f"🛠️ Tool Execution: {msg['name']}"):
                st.code(msg["content"])

# Chat input
if prompt := st.chat_input("Ask the agent to do something..."):
    # Display user prompt
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Run Agent Loop
    with st.chat_message("assistant"):
        llm = GroqClient()
        
        # Build history for LLM
        history = [{"role": "system", "content": st.session_state.system_prompt}]
        
        # Format session state messages for Groq API
        for m in st.session_state.messages:
            if m["role"] == "user":
                history.append({"role": "user", "content": m.get("content", "")})
            elif m["role"] == "assistant":
                msg = {"role": "assistant", "content": m.get("content", "")}
                if "tool_calls" in m:
                    msg["tool_calls"] = m["tool_calls"]
                history.append(msg)
            elif m["role"] == "tool":
                history.append({
                    "role": "tool", 
                    "tool_call_id": m.get("tool_call_id"), 
                    "name": m.get("name"), 
                    "content": m.get("content")
                })
        
        status_placeholder = st.empty()
        
        # Loop Prevention State
        loop_count = 0
        executed_tools = set()
        
        # ReAct Loop
        while True:
            loop_count += 1
            if loop_count > 25:
                st.error("🛑 Maximum agent turns (25) reached. Stopping to prevent infinite loops.")
                break
                
            status_placeholder.info(f"🧠 Thinking... (Turn {loop_count})")
            
            # Context Management: Truncate history to stay within Groq's 8k TPM limit
            managed_history = [{"role": "system", "content": st.session_state.system_prompt[:2000]}]
            
            # Keep the last 40 messages (20 tool turns) so the agent actually remembers its plan!
            user_tool_messages = history[1:] if len(history) > 0 and history[0].get("role") == "system" else history
            recent_messages = user_tool_messages[-40:]
            
            # SAFE TRUNCATION: Never orphan tool messages. 
            # If the window starts with a 'tool' message, the API will crash or return an empty string.
            while recent_messages and recent_messages[0].get("role") == "tool":
                recent_messages.pop(0)
            
            for msg in recent_messages:
                # Create a shallow copy to modify content without affecting actual history UI
                managed_msg = dict(msg)
                if "content" in managed_msg and isinstance(managed_msg["content"], str):
                    # Balance TPM limits by limiting massive file reads to 2500 characters
                    if len(managed_msg["content"]) > 2500:
                        managed_msg["content"] = managed_msg["content"][:2500] + "\n...[CONTENT TRUNCATED FOR CONTEXT LIMIT]..."
                managed_history.append(managed_msg)
            
            response = llm.chat_completion(
                messages=managed_history,
                tools=tools_schema
            )
            
            if isinstance(response, str):
                if response.startswith("API_KEY_ROTATED_"):
                    provider_name = response.split("_")[-1]
                    st.success(f"🔄 API Rate Limit Hit! Rotating to the next available API Key for {provider_name}...")
                    continue
                elif response.startswith("PROVIDER_FALLBACK_"):
                    provider_name = response.split("_")[-1]
                    st.success(f"🔄 API Error Detected! Autonomous Agent aggressively hot-swapping to Backup Provider ({provider_name})...")
                    continue
                elif response == "MODEL_FALLBACK_GEMMA":
                    st.warning("⚠️ Critical Token Limit Reached! Autonomous Agent swapping to Last-Resort Backup Model (Gemma 9B) to continue execution...")
                    continue
                elif "Failed to parse tool call arguments as JSON" in response or "tool_use_failed" in response:
                    st.warning("⚠️ Agent generated invalid JSON. Auto-recovering...")
                    error_msg = f"System Error: Your previous tool call failed due to malformed JSON syntax. Please rewrite your tool call using strictly valid JSON. Raw error: {response}"
                    history.append({"role": "user", "content": error_msg})
                    st.session_state.messages.append({"role": "user", "content": f"⚙️ Auto-Recovery Triggered: JSON Syntax Error"})
                    continue
                else:
                    st.error(f"Critical System Failure: {response}")
                    st.info("💡 Every single provider and fallback strategy has been exhausted. Please verify your API keys or check your internet connection.")
                    break
                
            if not response or not hasattr(response, 'choices') or not response.choices:
                st.error(f"Failed to get response from Groq API. Raw Response: {response}")
                break
                
            response_message = response.choices[0].message
            
            # Save assistant message to state and history
            if response_message.content:
                st.markdown(response_message.content)
                
            if not response_message.content and not response_message.tool_calls:
                st.warning("⚠️ The model returned an empty response. Auto-recovering...")
                error_msg = "System Error: You generated an empty response. You MUST either output a text message to the user, or execute a tool (like `write_file` or `replace_file_content`) to complete the task."
                history.append({"role": "user", "content": error_msg})
                # Add to session state so the UI shows the recovery attempt
                st.session_state.messages.append({"role": "user", "content": f"⚙️ Auto-Recovery Triggered: {error_msg}"})
                continue
            
            # Always save the assistant message to session state, even if content is None (it might have tool calls)
            asst_msg = {"role": "assistant", "content": response_message.content or ""}
            if response_message.tool_calls:
                asst_msg["tool_calls"] = [
                    {
                        "id": t.id,
                        "type": "function",
                        "function": {
                            "name": t.function.name,
                            "arguments": t.function.arguments
                        }
                    } for t in response_message.tool_calls
                ]
            st.session_state.messages.append(asst_msg)
            
            # Update history with the clean dictionary to avoid SDK validation errors
            history.append(asst_msg)
            
            if response_message.tool_calls:
                for tool_call in response_message.tool_calls:
                    func_name = tool_call.function.name
                    func_args = json.loads(tool_call.function.arguments)
                    
                    # Anti-Loop Mechanism
                    current_signature = f"{func_name}_{json.dumps(func_args)}"
                    if current_signature in executed_tools:
                        result = "System Error: You have already executed this EXACT tool call previously in this session. You are stuck in a loop. Do not repeat actions! Please do something different, like read a specific file you haven't read yet, or respond to the user."
                        status_placeholder.error(f"⚠️ Caught infinite loop attempt on {func_name}")
                    else:
                        executed_tools.add(current_signature)
                        
                        # Safely resolve paths relative to the active project directory
                        def resolve_path(p):
                            if os.path.isabs(p): return p
                            return os.path.join(st.session_state.project_dir, p)
                        
                        if func_name == "execute_command":
                            if "cwd" not in func_args or func_args["cwd"] in [".", "./", ""]:
                                func_args["cwd"] = st.session_state.project_dir
                            else:
                                func_args["cwd"] = resolve_path(func_args["cwd"])
                        elif func_name == "list_dir" and "directory" in func_args:
                            # Special case for root
                            if func_args["directory"] in [".", "./", ""]:
                                func_args["directory"] = st.session_state.project_dir
                            else:
                                func_args["directory"] = resolve_path(func_args["directory"])
                        elif func_name == "find_files" and "directory" in func_args:
                            if func_args["directory"] in [".", "./", ""]:
                                func_args["directory"] = st.session_state.project_dir
                            else:
                                func_args["directory"] = resolve_path(func_args["directory"])
                        elif func_name == "read_file" and "filepath" in func_args:
                            func_args["filepath"] = resolve_path(func_args["filepath"])
                        elif func_name == "write_file" and "filepath" in func_args:
                            func_args["filepath"] = resolve_path(func_args["filepath"])
                        elif func_name == "replace_file_content" and "filepath" in func_args:
                            func_args["filepath"] = resolve_path(func_args["filepath"])
                            
                        status_placeholder.warning(f"🛠️ Executing `{func_name}`...")
                        
                        if func_name in TOOL_FUNCTIONS:
                            func_to_call = TOOL_FUNCTIONS[func_name]
                            result = func_to_call(**func_args)
                        else:
                            result = f"Error: Unknown tool {func_name}"
                        
                    tool_msg = {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": func_name,
                        "content": str(result),
                    }
                    
                    st.session_state.messages.append(tool_msg)
                    history.append(tool_msg)
                    
                    with st.expander(f"🛠️ Tool Execution: {func_name}"):
                        st.code(str(result))
            else:
                status_placeholder.empty()
                break # Exit loop when no more tools are called
