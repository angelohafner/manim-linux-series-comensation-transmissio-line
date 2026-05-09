from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ElectricalSymbols:
    """LaTeX symbols used in the educational animation."""

    source_voltage: str
    receiver_voltage: str
    inductive_reactance: str
    capacitive_reactance: str
    equivalent_reactance: str
    maximum_power: str


@dataclass(frozen=True)
class NumericalParameters:
    """Numerical values used by the visual explanations."""

    uncompensated_capacity_fraction: float
    before_capacity_fraction: float
    after_capacity_fraction: float
