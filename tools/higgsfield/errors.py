"""Error types for the Higgsfield client."""


class HiggsfieldError(Exception):
    """Base class for all Higgsfield-client errors."""


class HiggsfieldConfigError(HiggsfieldError):
    """Required env var is missing or invalid."""

    def __init__(self, missing: list[str]):
        self.missing = list(missing)
        super().__init__(
            "Higgsfield config is incomplete, missing: " + ", ".join(self.missing)
        )


class HiggsfieldAPIError(HiggsfieldError):
    """Non-2xx response from FNF."""

    def __init__(self, status_code: int, body: str, *, path: str = ""):
        self.status_code = status_code
        self.body = body
        self.path = path
        prefix = f"{path}: " if path else ""
        super().__init__(f"{prefix}status {status_code}: {body}")


class HiggsfieldTimeout(HiggsfieldError):
    """Job polling exceeded the configured wall-clock timeout."""

    def __init__(self, job_id: str, elapsed: float):
        self.job_id = job_id
        self.elapsed = elapsed
        super().__init__(f"job {job_id} did not reach terminal status in {elapsed:.0f}s")
