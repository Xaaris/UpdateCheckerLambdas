from dataclasses import dataclass


@dataclass
class Product:
    id: str
    major_version: int
    minor_version: int
    hotfix_version: int
    release_notes_link: str
