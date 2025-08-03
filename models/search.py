import csv
from typing import Optional, List, ClassVar, Set

import requests
from pydantic import BaseModel

from models.search_result import SearchResult, Hit


class Search(BaseModel):
    source: str = "noid"
    from_index: int = 0
    size: int = 10000
    base_url: str = "https://search.dsn.dk/api/"
    danish_alphabet: ClassVar[List[str]] = list("abcdefghijklmnopqrstuvwxyzæøå")
    hits: Set[Hit] = set()

    def search_letter(self, letter: str) -> Optional[SearchResult]:
        print(f"Fetching letter: {letter}")
        params = {
            "source": self.source,
            "search": letter,
            "from": self.from_index,
            "size": self.size,
        }
        response = requests.get(self.base_url, params=params)
        if response.ok:
            # pprint(response.json())
            sr = SearchResult.model_validate(response.json())
            print(response.url)
            # exit(0)
            return sr
        else:
            raise Exception(f"Failed to fetch for letter '{letter}': {response.status_code}")
            # return None

    def run(self):
        self.fetch_all()
        self.save_to_tsv()

    def fetch_all(self) -> None:
        for letter in self.danish_alphabet:
            print(f"Fetching for: {letter}")
            result: SearchResult = self.search_letter(letter)
            if result:
                for hit in result.hits.hits:
                    self.hits.add(hit)

    @property
    def number_of_hits(self):
        return len(self.hits)

    def save_to_tsv(self):
        """Methods that save to tsv file with columns lemma, id, definition"""
        print(f"Writing TSV with all {self.number_of_hits} records")
        with open("noid.tsv", "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, delimiter="\t")
            writer.writerow(["id", "lemma", "category", "definition"])

            for hit in self.hits:
                lemma = hit.lemma
                noid = hit.noid
                definition = hit.definition
                category = hit.lexical_category
                writer.writerow([noid, lemma, category, definition])
