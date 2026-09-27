# 💻 AI Coding Agent Harness

An elite autonomous software engineering agent harness built with Python and Streamlit. This harness doesn't just generate text—it maps your repository, surgically patches files, executes commands, and autonomously compiles your code to verify it works without human intervention.

## 🚀 Features

- **Autonomous Orchestration:** Scans repositories in O(1) time using optimized `find_files`.
- **Surgical Diff Editing:** Uses `replace_file_content` to edit specific lines of code without overwriting massive files (saving tokens and time).
- **Closed-Loop Verification:** Natively calls compilers (like `g++`, `python`, `node`) via `execute_command` to verify zero exit codes before terminating.
- **Auto-Recovery Engine:** Automatically detects and recovers from JSON parse errors or empty LLM responses by feeding the error back to the agent.
- **Aggressive Multi-Provider Routing:** Hot-swaps between providers instantly on any API error (Rate Limits, 500s, 401s). Supports Groq, DeepSeek, Qwen (DashScope), Gemini, Requesty, and Local (Ollama).

## 🛠️ Installation & Local Setup

1. **Clone the repository and enter the directory:**
   ```bash
   cd agent_harness
   ```

2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure your Environment Variables:**
   Create a `.env` file in the root directory. You do **not** need all of these keys. The routing engine will automatically use whichever keys are available and dynamically cascade down the list if one fails.

   ```env
   # ==========================================
   # 🔑 API KEY CONFIGURATION
   # ==========================================
   
   # 1. Groq (Primary High-Speed Provider)
   GROQ_API_KEYS="sk-groqkey1,sk-groqkey2"
   
   # 2. DeepSeek (Advanced Coding Fallback)
   DEEPSEEK_API_KEY="sk-deepseekkey"
   
   # 3. Qwen via DashScope (Alibaba Native)
   QWEN_API_KEY="sk-qwenkey"
   
   # 4. Google Gemini (Via OpenAI compatibility layer)
   GEMINI_API_KEY="AIzaSy-geminikey"
   
   # 5. Requesty AI (OpenRouter Alternative)
   REQUESTY_API_KEY="sk-requestykey"
   REQUESTY_MODEL="meta-llama/llama-3.1-70b-instruct"
   
   # 6. Local Hosted AI (Ollama, LM Studio) - Offline Safety Net
   LOCAL_API_BASE_URL="http://localhost:11434/v1"
   LOCAL_MODEL_NAME="qwen3.5:9b"
   ```

4. **Run the Harness:**
   ```bash
   streamlit run app.py
   ```

## 🌍 Deployment Options

⚠️ **Note on Vercel:** You **cannot** deploy this directly to Vercel. Vercel is designed for stateless Serverless functions, but Streamlit requires a persistent, long-running WebSockets connection to maintain the chat UI and agent state. 

Here are the two best free platforms to deploy this system for a hackathon:

### Option 1: Streamlit Community Cloud (Recommended & Easiest)
1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io/).
3. Connect your GitHub account and click **New App**.
4. Select your repository and set the main file to `app.py`.
5. In the Streamlit Cloud dashboard, click **Advanced Settings** and paste the contents of your `.env` file into the "Secrets" box.
6. Click Deploy!

### Option 2: Render.com (Most Robust)
1. Push this repository to GitHub.
2. Go to [Render.com](https://render.com/) and create a new **Web Service**.
3. Connect your repository.
4. Set the Build Command to: `pip install -r requirements.txt`
5. Set the Start Command to: `streamlit run app.py --server.port $PORT`
6. Add your `.env` keys in the "Environment Variables" section.
7. Click Deploy!

