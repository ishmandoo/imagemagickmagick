import shlex
import shutil
import subprocess

from imagemagickmagick.exceptions import CommandExecutionError, ImageMagickNotFoundError


def check_imagemagick() -> None:
    if shutil.which("convert") is None:
        raise ImageMagickNotFoundError(
            "ImageMagick 'convert' not found in PATH.\n"
            "Install it with:\n"
            "  apt install imagemagick    (Debian/Ubuntu)\n"
            "  brew install imagemagick   (macOS)"
        )
    result = subprocess.run(
        ["convert", "--version"], capture_output=True, text=True
    )
    if "ImageMagick" not in result.stdout:
        raise ImageMagickNotFoundError(
            "'convert' is in PATH but is not ImageMagick.\n"
            f"Got: {result.stdout[:120]}"
        )


def run_command(command: str) -> None:
    args = shlex.split(command)
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise CommandExecutionError(
            f"ImageMagick failed (exit {result.returncode})",
            returncode=result.returncode,
            stderr=result.stderr.strip(),
        )
