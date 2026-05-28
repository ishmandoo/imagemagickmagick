import shlex
import shutil
import subprocess

from imagemagickmagick.exceptions import CommandExecutionError, ImageMagickNotFoundError


def find_imagemagick() -> str:
    """Return the ImageMagick binary to use: 'magick' (IM7/Windows) or 'convert' (IM6/Linux)."""
    for binary in ("magick", "convert"):
        if shutil.which(binary) is None:
            continue
        result = subprocess.run([binary, "--version"], capture_output=True, text=True)
        if "ImageMagick" in result.stdout:
            return binary
    raise ImageMagickNotFoundError(
        "ImageMagick not found in PATH.\n"
        "Install it with:\n"
        "  apt install imagemagick    (Debian/Ubuntu)\n"
        "  brew install imagemagick   (macOS)\n"
        "  winget install ImageMagick.ImageMagick (Windows)"
    )


def resolve_command(command: str, binary: str) -> str:
    """Prefix the LLM-generated 'convert ...' command with the correct binary."""
    if binary == "magick":
        return "magick " + command
    return command


def run_command(command: str) -> None:
    args = shlex.split(command)
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise CommandExecutionError(
            f"ImageMagick failed (exit {result.returncode})",
            returncode=result.returncode,
            stderr=result.stderr.strip(),
        )
