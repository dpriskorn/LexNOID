from typing import List
from urllib.parse import quote

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


class SourceFields(BaseModel):
    chronology: None | int = None


class Source(BaseModel):
    """An entry in NOID"""
    fields: SourceFields
    title_headword: str
    headword_id: str
    html_list: str

    @property
    def url(self):
        return f"https://noid.dsn.dk/ordbog/{quote(self.noid)}/"

    @property
    def noid(self):
        return self.headword_id

    @property
    def lemma(self):
        return self.title_headword

    @property
    def year(self) -> int:
        return self.fields.chronology

    @property
    def definition(self) -> str:
        """Return the text content of the first <span class='defpar'> or empty string if none."""
        soup = BeautifulSoup(self.html_list, "lxml")
        span = soup.find("span", class_="defpar")
        return span.get_text(strip=True) if span else ""

class Hit(BaseModel):
    """Search hit"""
    source: Source = Field(..., alias="_source")

    class Config:
        validate_by_name = True

    def __hash__(self):
        return hash(self.noid)

    def __eq__(self, other):
        if not isinstance(other, Hit):
            return NotImplemented
        return self.noid == other.noid

    @property
    def lemma(self):
        return self.source.title_headword

    @property
    def url(self) -> str:
        return self.source.url

    @property
    def noid(self) -> str:
        return self.source.noid

    @property
    def year(self) -> int:
        return self.source.fields.chronology

    @property
    def definition(self) -> str:
        return self.source.definition

class Hits(BaseModel):
    hits: List[Hit]


class SearchResult(BaseModel):
    hits: Hits
