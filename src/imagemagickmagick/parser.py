import re

from imagemagickmagick.exceptions import CommandParseError


def extract_command(raw: str) -> str:
    text = raw.strip()

    # Strategy 1: whole output is the command
    if text.lower().startswith("convert "):
        cmd = text.splitlines()[0].strip()
        return _validate(cmd)

    # Strategy 2: scan lines for first starting with 'convert'
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("convert "):
            return _validate(line)

    # Strategy 3: extract from markdown code fence, retry line scan
    fence_match = re.search(r"```(?:\w*\n)?(.*?)```", text, re.DOTALL)
    if fence_match:
        inner = fence_match.group(1).strip()
        for line in inner.splitlines():
            line = line.strip()
            if line.lower().startswith("convert "):
                return _validate(line)

    # Strategy 4: loose regex
    match = re.search(r"\bconvert\s+\S.*", text)
    if match:
        return _validate(match.group(0))

    raise CommandParseError(
        f"Could not extract a convert command from model output:\n{raw}"
    )


def _validate(cmd: str) -> str:
    if "INPUT_FILE" not in cmd:
        raise CommandParseError(
            f"Generated command missing INPUT_FILE placeholder:\n{cmd}"
        )
    if "OUTPUT_FILE" not in cmd:
        raise CommandParseError(
            f"Generated command missing OUTPUT_FILE placeholder:\n{cmd}"
        )
    return cmd
