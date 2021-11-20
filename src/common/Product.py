from dataclasses import dataclass


@dataclass
class Product:
    id: str
    name: str
    major_version: int
    minor_version: int
    hotfix_version: int
    release_notes_link: str

    def get_full_version(self) -> str:
        return f"{self.major_version}.{self.minor_version}.{self.hotfix_version}"
