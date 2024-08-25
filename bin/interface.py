import gradio as gr
from downloader import Downloader


def search(url, ext, progress=gr.Progress()):
    down = Downloader()

    def progress_callback(status, downloaded_bytes, total_bytes):
        if total_bytes > 0:
            progress(progress=downloaded_bytes / total_bytes)

    result = down.search_yt(url, ext, progress_callback)
    return result['file_path'] if result else None


def interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Video and Music converter")

        gr.Markdown("## This app converts URLs into mp4 and mp3 files")
        url = gr.Text(type="text", label="Insert the URL")
        ext = gr.Dropdown(["mp3", "wav", "mp4"], label="Choose the type to convert into")
        submit_btn = gr.Button("Submit")
        progress_bar = gr.Progress()
        download_btn = gr.Button("Download", interactive=False)
        output_file = gr.File(label="Converted file")

        def on_submit(url, ext):
            file_path = search(url, ext, progress_bar)
            return {download_btn: gr.Button(interactive=True), output_file: file_path}

        submit_btn.click(on_submit, inputs=[url, ext], outputs=[download_btn, output_file])

    demo.launch(inbrowser=True)


if __name__ == "__main__":
    interface()
