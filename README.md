# imagemagickmagick

ImageMagick is powerful but hard to use. `imagemagickmagick` lets you describe what you want in plain English and does the rest.

```
imagemagickmagick input.jpg "make it grayscale" output.jpg
imagemagickmagick input.jpg "add a vintage filter" output.jpg
imagemagickmagick input.jpg "crop to 800x600 centered" output.jpg
imagemagickmagick input.jpg "rotate 90 degrees clockwise" output.jpg --dry-run
```

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- ImageMagick (`apt install imagemagick` or `brew install imagemagick`)

## Installation

```bash
git clone https://github.com/ishmandoo/imagemagickmagick
cd imagemagickmagick
uv tool install .
```

The first time you run a command, the tool downloads a ~770MB language model to `~/.cache/imagemagickmagick/`. Subsequent runs load it from the cache.

## Usage

```
imagemagickmagick INPUT_FILE DESCRIPTION OUTPUT_FILE [--dry-run]
```

| Argument | Description |
|---|---|
| `INPUT_FILE` | Path to the source image |
| `DESCRIPTION` | Plain-English description of the transformation |
| `OUTPUT_FILE` | Path to write the result |
| `--dry-run` | Print the generated ImageMagick command without executing it |

## How it works

1. Your description is sent to a local 1B-parameter LLM ([Llama-3.2-1B-Instruct](https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF)) running via [llama-cpp-python](https://github.com/abetlen/llama-cpp-python)
2. The model generates an ImageMagick `convert` command
3. The command is executed locally — no data leaves your machine
