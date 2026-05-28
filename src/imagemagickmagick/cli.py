import sys

import click

from imagemagickmagick.exceptions import CommandExecutionError, ImageMagickMagickError
from imagemagickmagick.executor import find_imagemagick, resolve_command, run_command
from imagemagickmagick.model import DEFAULT_FILE, DEFAULT_REPO, ensure_model, generate_command
from imagemagickmagick.parser import extract_command
from imagemagickmagick.prompt import substitute_placeholders


@click.command()
@click.argument("input_file", type=click.Path(exists=True, readable=True))
@click.argument("description")
@click.argument("output_file")
@click.option("--dry-run", is_flag=True, help="Print the generated command without executing it.")
@click.option("--model-repo", default=DEFAULT_REPO, hidden=True)
@click.option("--model-file", default=DEFAULT_FILE, hidden=True)
def main(
    input_file: str,
    description: str,
    output_file: str,
    dry_run: bool,
    model_repo: str,
    model_file: str,
) -> None:
    """Describe an image transformation in plain English and let ImageMagick do the work.

    \b
    Examples:
      imagemagickmagick input.jpg "make it grayscale" output.jpg
      imagemagickmagick input.jpg "rotate 90 degrees" output.jpg --dry-run
    """
    try:
        binary = find_imagemagick()

        model_path = ensure_model(model_repo, model_file)

        click.echo("Generating command...")
        raw = generate_command(model_path, description)

        template = extract_command(raw)
        command = resolve_command(substitute_placeholders(template, input_file, output_file), binary)

        if dry_run:
            click.echo(command)
            return

        click.echo(f"Running: {command}")
        run_command(command)
        click.echo(f"Done. Output: {output_file}")

    except CommandExecutionError as e:
        _echo_error(f"Error: {e}")
        if e.stderr:
            _echo_error(e.stderr)
        sys.exit(1)
    except ImageMagickMagickError as e:
        _echo_error(f"Error: {e}")
        sys.exit(1)


def _echo_error(msg: str) -> None:
    try:
        click.echo(msg, err=True)
    except OSError:
        click.echo(msg)
