import gradio as gr
import asyncio
import time
import textwrap

# --- 1. CSS for Styling ---
app_css = """
/* General Styling */
.gradio-container { font-family: 'Inter', sans-serif; background-color: #f8fafc; }

/* Main Layout */
.main-container { display: flex; flex-direction: row; gap: 2rem; }
.sidebar-column { flex-grow: 1; min-width: 350px; }
.chat-column { flex-grow: 2; }

/* Panel Styling */
.panel {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 1rem;
    padding: 1.5rem;
    height: 100%;
}
.panel h2 {
    font-size: 1.25rem;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}
.panel h2 i { margin-right: 0.75rem; }

/* Chatbot Styling */
.chatbot { background-color: #f1f5f9; border-radius: 1rem; }
.chatbot .message-bubble { box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1) !important; }

/* Icon Styling */
.fa-spinner { animation: fa-spin 2s infinite linear; }
@keyframes fa-spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
"""

# --- 2. SIMULATED AGENT LOGIC ---
# This async function simulates the MCP agent's execution.
async def run_docs_agent(message, history, api_key, doc_url):
    """
    Simulates a conversational response from the documentation agent.
    """
    if not api_key:
        yield "⚠️ **Error:** Please enter your Nebius API key in the sidebar to continue."
        return

    # Start with a thinking message
    yield "<i class='fas fa-spinner fa-spin'></i> Thinking..."
    await asyncio.sleep(2.5) # Simulate processing time

    # --- Generate response based on query content ---
    query = message.lower()
    if "migrate" in query:
        response = """
        ### Migrating to Mintlify

        Migrating your documentation from other platforms is straightforward. Here are the general steps:

        1.  **Export Your Content:** Most platforms allow you to export your content, usually in Markdown format.
        2.  **Set Up Your Mintlify Project:** Create a new project and configure the basic settings in `mint.json`.
        3.  **Import Markdown Files:** Place your exported Markdown files into the appropriate directories in your new project.
        4.  **Adjust Frontmatter:** You may need to update the frontmatter (the metadata at the top of your files) to match Mintlify's format for titles, icons, and navigation.
        5.  **Deploy:** Push your changes to GitHub, and your new documentation site will be deployed automatically.
        """
    elif "key features" in query:
        response = """
        ### Key Features
        - **Automatic Deployments:** Integrates directly with GitHub for continuous deployment.
        - **Powerful Search:** Fast, AI-powered search that understands natural language.
        - **Interactive Components:** Includes interactive elements like code tabs, callouts, and API playgrounds.
        - **Built-in Analytics:** Track page views, user feedback, and search queries without third-party tools.
        """
    elif "authentication" in query:
        response = """
        ### Setting Up Authentication
        You can protect your documentation with a password or by requiring users to log in with supported providers.

        To enable authentication, add the `auth` object to your `mint.json` file:
        ```json
        "auth": {
          "password": "your-secure-password"
        }
        ```
        For more advanced options like SSO, please refer to the official security documentation.
        """
    else:
        response = "I'm sorry, I couldn't find specific information on that topic. Could you try rephrasing your question?"

    yield textwrap.dedent(response)


# --- 3. GRADIO UI LAYOUT ---
with gr.Blocks(css=app_css, theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        textwrap.dedent("""
        # 📚 Talk to Your Docs
        <p style="font-size:0.9rem; color:#475569;">Ask questions and get answers from any documentation URL.</p>
        """)
    )

    with gr.Row(elem_classes=["main-container"]):
        # --- Left Column: Sidebar ---
        with gr.Column(elem_classes=["sidebar-column"]):
            with gr.Column(elem_classes=["panel"]):
                gr.Markdown('<h2><i class="fas fa-key" style="color:#f59e0b;"></i>Configuration</h2>')
                api_key_input = gr.Textbox(label="Nebius API Key", type="password")
                doc_url_input = gr.Textbox(label="Documentation URL", value="https://mintlify.com/docs/mcp")

        # --- Right Column: Chat Interface ---
        with gr.Column(elem_classes=["chat-column"]):
            chatbot = gr.Chatbot(
                label="Chat",
                elem_id="chatbot",
                bubble_full_width=False,
                height=600,
            )
            chat_interface = gr.ChatInterface(
                fn=run_docs_agent,
                chatbot=chatbot,
                additional_inputs=[api_key_input, doc_url_input],
                examples=[
                    "How to migrate documentation from your current platform to Mintlify?",
                    "What are the key features of the documentation platform?",
                    "How do I set up authentication?",
                ],
                title=None, # Use custom title above
                submit_btn="Ask",
                retry_btn=None,
                undo_btn=None,
                clear_btn="🗑️ Clear Chat",
            )

if __name__ == "__main__":
    demo.queue()
    demo.launch(debug=True)
