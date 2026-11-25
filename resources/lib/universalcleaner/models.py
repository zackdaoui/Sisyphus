# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import List


@dataclass
class Step:
    """One official cleaning command."""
    label: str
    command: str


@dataclass
class StepResult:
    label: str
    ok: bool
    detail: str = ""


@dataclass
class AddonResult:
    addon_id: str
    name: str
    steps: List[StepResult] = field(default_factory=list)
    error: str = ""  # set when the add-on could not be cleaned at all

    @property
    def ok(self):
        return not self.error and all(s.ok for s in self.steps)

    @property
    def ops_ok(self):
        return sum(1 for s in self.steps if s.ok)

    @property
    def ops_failed(self):
        return sum(1 for s in self.steps if not s.ok) + (1 if self.error else 0)


@dataclass
class SupportedAddon:
    integration: object
    name: str
    icon: str
    version: str
