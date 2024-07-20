"""Models for the SMT FHIR resources."""

from pydantic import BaseModel


class TagItem(BaseModel):
    """The tag item class."""

    system: str
    code: str
    display: str


class Meta(BaseModel):
    """The meta class."""

    lastUpdated: str
    tag: list[TagItem]


class LinkItem(BaseModel):
    """The link item class."""

    relation: str
    url: str


class TagItem1(BaseModel):
    """The entry tag item class."""

    system: str
    code: str
    display: str


class Meta1(BaseModel):
    """The entry meta item class."""

    versionId: str
    lastUpdated: str
    profile: list[str]
    tag: list[TagItem1]


class IdentifierItem(BaseModel):
    """The identifier item class."""

    system: str
    value: str


class Resource(BaseModel):
    """The resource class."""

    resourceType: str
    id: str
    meta: Meta1
    url: str
    identifier: list[IdentifierItem]
    version: str
    name: str
    status: str
    experimental: bool
    date: str
    publisher: str


class EntryItem(BaseModel):
    """The entry item class."""

    fullUrl: str
    resource: Resource


class Model(BaseModel):
    """The Bundle (Model) class."""

    resourceType: str
    id: str
    meta: Meta
    type: str
    total: int
    link: list[LinkItem]
    entry: list[EntryItem]
