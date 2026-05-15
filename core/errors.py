class IssueNotFoundError(Exception):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"Issue {key} not found")


class ClientNotFoundError(Exception):
    """Raised when the acli binary is not on PATH."""
    pass


class ClientError(Exception):
    """Raised when acli returns a non-zero exit code."""
    pass
