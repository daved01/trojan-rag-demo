import datetime
from typing import Any
import src.config as config


class ExperimentLogger:
    def __init__(self, experiment_name: str = "attack_demo"):
        """
        Initializes a new log file with a timestamp.
        """

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.filename = f"{experiment_name}_{timestamp}.md"
        self.filepath = config.LOGS_DIR / self.filename
        
        # Initialize the file with a header
        self._write(f"# Experiment: {experiment_name}")
        self._write(f"**Date:** {datetime.datetime.now()}\n")
        self._write(f"**Model:** {config.LLM_MODEL_NAME}")
        self._write(f"**Embedding:** {config.EMBEDDING_MODEL_NAME}\n")
        self._write("---\n")
        
        print(f"Logging to: {self.filepath}")


    def _write(self, text: str):
        """
        Helper to append text to the log file.
        """

        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(text + "\n")


    def log_phase(self, phase_name: str):
        """
        Logs a major section header (e.g. Phase 1).
        """

        self._write(f"\n## {phase_name}")
        self._write("-" * 40)


    def log_query(self, query: str):
        self._write(f"\n### User Query")
        self._write(f"> {query}\n")


    def log_retrieval(self, results: dict[str, Any], top_k: int = 3):
        """
        Logs the raw retrieval results from the vector DB.
        This is the transparent evidence of what the system saw.
        """

        self._write("\n### RAG Retrieval (Top Chunks)")
        
        ids = results['ids'][0]
        distances = results['distances'][0]
        metadatas = results['metadatas'][0]
        documents = results['documents'][0]
        
        for i in range(min(top_k, len(ids))):
            doc_preview = documents[i].replace("\n", " ")[:200] + "..."
            
            self._write(f"**Rank {i+1}:**")
            self._write(f"- **ID:** `{ids[i]}`")
            self._write(f"- **Distance:** `{distances[i]:.4f}` (Lower is better)")
            self._write(f"- **Source:** `{metadatas[i]['source']}`")
            self._write(f"- **Content Preview:**\n`{doc_preview}`\n")


    def log_llm_response(self, prompt: str, response: str):
        """
        Logs the final interaction.
        """

        self._write("\n### Model Response")
        self._write(response)
        
        self._write("\n<details>")
        self._write("<summary>View Full System Prompt</summary>\n")
        self._write(f"```text\n{prompt}\n```")
        self._write("</details>\n")


    def log_image(self, image_filename: str, caption: str = "Retrieval Visualization"):
        """
        Embeds a locally saved image into the markdown log.
        """

        self._write(f"\n### Visualization")
        # Use relative path for markdown compatibility
        rel_plots_path = config.PLOTS_DIR.relative_to(config.BASE_DIR)
        self._write(f"![{caption}](/{rel_plots_path}/{image_filename})\n")
