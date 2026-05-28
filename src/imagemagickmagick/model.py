from pathlib import Path

from imagemagickmagick.exceptions import ModelDownloadError
from imagemagickmagick.prompt import SYSTEM_PROMPT, build_user_prompt

CACHE_DIR = Path.home() / ".cache" / "imagemagickmagick"

DEFAULT_REPO = "bartowski/Llama-3.2-1B-Instruct-GGUF"
DEFAULT_FILE = "Llama-3.2-1B-Instruct-Q4_K_M.gguf"


def ensure_model(repo_id: str = DEFAULT_REPO, filename: str = DEFAULT_FILE) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cached = CACHE_DIR / filename

    if cached.exists() and cached.stat().st_size > 0:
        return cached

    try:
        from huggingface_hub import hf_hub_download
        from huggingface_hub.errors import EntryNotFoundError, RepositoryNotFoundError
    except ImportError as e:
        raise ModelDownloadError(f"huggingface_hub not installed: {e}") from e

    click_echo = _get_click_echo()
    click_echo(f"Downloading model (first run only, ~770MB)...")

    try:
        hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=str(CACHE_DIR),
            local_dir_use_symlinks=False,
        )
    except RepositoryNotFoundError as e:
        raise ModelDownloadError(f"Model repo not found: {repo_id}") from e
    except EntryNotFoundError as e:
        raise ModelDownloadError(f"Model file not found: {filename} in {repo_id}") from e
    except Exception as e:
        raise ModelDownloadError(f"Download failed: {e}") from e

    if not cached.exists() or cached.stat().st_size == 0:
        raise ModelDownloadError("Download completed but file is missing or empty.")

    return cached


def generate_command(
    model_path: Path,
    description: str,
    previous_attempts: list[tuple[str, str]] | None = None,
) -> str:
    try:
        from llama_cpp import Llama
    except ImportError as e:
        raise ModelDownloadError(f"llama-cpp-python not installed: {e}") from e

    try:
        llm = Llama(
            model_path=str(model_path),
            n_ctx=1024,
            verbose=False,
        )
    except Exception as e:
        raise ModelDownloadError(f"Failed to load model: {e}") from e

    messages: list[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(description)},
    ]
    for template, error in (previous_attempts or []):
        messages.append({"role": "assistant", "content": template})
        messages.append({"role": "user", "content": f"That command failed: {error}\nTry a different approach."})

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=256,
        temperature=0.1,
        stop=["\n\n"],
    )
    return response["choices"][0]["message"]["content"]


def _get_click_echo():
    try:
        import click
        return click.echo
    except ImportError:
        return print
