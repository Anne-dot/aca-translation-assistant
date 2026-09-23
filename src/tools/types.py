from typing import TypedDict


class Meaning(TypedDict):
    definition: str
    synonyms: list[str]
    usageExample: str


class Action(TypedDict):
    type: str
    date: str
    data: list | dict


class Term(TypedDict):
    # `term` field should be something like "name", but changing that would
    # be a whole ordeal at the moment.
    term: str
    grammaticalType: str
    seeAlso: list
    meanings: list[Meaning]
    # `pageReferences` should be a list of strings!
    # it's currently a string of newline-delimited entries
    pageReferences: str
    reviewedAt: str
    needsReview: bool
    waitingForUpdate: bool
    actions: list[Action]


# this type, frankly, impolitely, just sucks
# the entire normalization system and how different functions
# deal with appending to the list of issues is making my head hurt.
# so this is how it will stay for now.
type Issue = dict[str, str]
