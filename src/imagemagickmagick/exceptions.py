class ImageMagickMagickError(Exception):
    pass


class ImageMagickNotFoundError(ImageMagickMagickError):
    pass


class ModelDownloadError(ImageMagickMagickError):
    pass


class CommandParseError(ImageMagickMagickError):
    pass


class CommandExecutionError(ImageMagickMagickError):
    def __init__(self, message: str, returncode: int, stderr: str) -> None:
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr
