from typing import Literal

from pydantic import BaseModel, Field


SourceKind = Literal["paper", "repo", "note", "dataset", "benchmark", "metric"]
ReadingStatus = Literal[
    "unread",
    "skimmed",
    "read",
    "noted",
    "reproduced",
    "compared",
    "rejected",
    "not_relevant",
    "later",
]
GapType = Literal[
    "concept_gap",
    "baseline_gap",
    "benchmark_gap",
    "metric_gap",
    "implementation_gap",
]
NoveltyRisk = Literal["low", "medium", "high", "unknown"]


class Project(BaseModel):
    id: str
    name: str
    goal: str
    keywords: list[str] = Field(default_factory=list)


class SourceItem(BaseModel):
    id: str
    title: str
    kind: SourceKind
    status: ReadingStatus
    citation: str


class CoverageItem(BaseModel):
    source_id: str
    source_title: str
    learned: str
    useful_for_project: str
    limitation_for_project: str
    citation: str


class Gap(BaseModel):
    id: str
    gap_type: GapType
    missing: str
    reason: str
    evidence: str
    severity: int = Field(ge=1, le=5)


class NoveltyOverlap(BaseModel):
    compared_item: str
    similarity_points: list[str]
    difference_points: list[str]
    novelty_risk: NoveltyRisk
    differentiation_hint: str
    citation: str


class StatusQuestion(BaseModel):
    item: str
    question: str
    allowed_statuses: list[ReadingStatus]


class EvidencePath(BaseModel):
    path: list[str]
    explanation: str
    citation: str


class Recommendation(BaseModel):
    action: str
    target: str
    addresses_gap_id: str
    reason: str
    evidence_path: EvidencePath


class ResearchStateReport(BaseModel):
    project: Project
    short_answer: str
    covered: list[CoverageItem]
    gaps: list[Gap]
    novelty_overlaps: list[NoveltyOverlap]
    status_questions: list[StatusQuestion]
    recommendations: list[Recommendation]
