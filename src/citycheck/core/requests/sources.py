from dataclasses import dataclass


@dataclass
class SourceAPI:
    base_url: str
    api_version: str
    endpoint: str

    @property
    def url(self) -> str:
        return f"{self.base_url}/v{self.api_version}/{self.endpoint}"
