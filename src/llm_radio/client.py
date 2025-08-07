import subprocess

import gradio as gr


def run_dig(message: str, history: list, server_address: str, server_port: int) -> str:
    """
    Executes the dig command and returns the output.
    """
    if not server_address or not server_port:
        return "Error: Server Address and Port must be provided."
    try:
        command = [
            "dig",
            f"@{server_address}",
            "-p",
            str(server_port),
            message,
            "TXT",
            "+short",
        ]
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        # The output from dig includes quotes, which we can remove for a cleaner display.
        return result.stdout.strip().replace('"', "")
    except FileNotFoundError:
        return "Error: 'dig' command not found. Please ensure it is installed and in your PATH."
    except subprocess.CalledProcessError as e:
        return f"Error executing dig command:\n{e.stderr}"
    except subprocess.TimeoutExpired:
        return "Error: dig command timed out."


def create_chat_interface() -> gr.Blocks:  # pragma: no cover
    """
    Creates the Gradio chat interface.
    """
    with gr.Blocks(theme=gr.themes.Soft(), title="LLM Radio") as demo:  # type: ignore
        gr.Markdown("# LLM Radio 📻")
        gr.Markdown("Query a Large Language Model over the DNS protocol.")

        with gr.Row():
            server_address = gr.Textbox(label="DNS Server Address", value="127.0.0.1")
            server_port = gr.Number(label="DNS Server Port", value=1053, precision=0)

        gr.ChatInterface(
            fn=run_dig,
            additional_inputs=[server_address, server_port],
            examples=[
                ["What is the capital of France?"],
                ["Explain the DNS protocol in one sentence."],
            ],
            title="Chat with LLM Radio",
            chatbot=gr.Chatbot(type="messages"),
        )
    return demo


def main() -> None:  # pragma: no cover
    """Launches the Gradio interface."""
    demo = create_chat_interface()
    demo.launch()


if __name__ == "__main__":  # pragma: no cover
    main()
