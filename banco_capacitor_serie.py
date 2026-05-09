from __future__ import annotations

from plotters.scenes import (
    FirstFourSlidesScene as _FirstFourSlidesScene,
    FirstSlideScene as _FirstSlideScene,
    FirstThreeSlidesScene as _FirstThreeSlidesScene,
    FirstTwoSlidesScene as _FirstTwoSlidesScene,
    SeriesCapacitorScene as _SeriesCapacitorScene,
)


class SeriesCapacitorScene(_SeriesCapacitorScene):
    """Main scene name exposed to Manim."""


class FirstSlideScene(_FirstSlideScene):
    """Render only the opening slide."""


class FirstTwoSlidesScene(_FirstTwoSlidesScene):
    """Render only the first two slides."""


class FirstThreeSlidesScene(_FirstThreeSlidesScene):
    """Render only the first three slides."""


class FirstFourSlidesScene(_FirstFourSlidesScene):
    """Render only the first four slides."""


class BancoCapacitorSerieScene(SeriesCapacitorScene):
    """Compatibility name for older Manim commands."""


class BancoCapacitorSeriePrimeiroSlideScene(FirstSlideScene):
    """Compatibility name for older Manim commands."""


class BancoCapacitorSerieDoisPrimeirosSlidesScene(FirstTwoSlidesScene):
    """Compatibility name for older Manim commands."""


class BancoCapacitorSerieTresPrimeirosSlidesScene(FirstThreeSlidesScene):
    """Compatibility name for older Manim commands."""


class BancoCapacitorSerieQuatroPrimeirosSlidesScene(FirstFourSlidesScene):
    """Compatibility name for older Manim commands."""


__all__ = [
    "BancoCapacitorSerieDoisPrimeirosSlidesScene",
    "BancoCapacitorSeriePrimeiroSlideScene",
    "BancoCapacitorSerieQuatroPrimeirosSlidesScene",
    "BancoCapacitorSerieScene",
    "BancoCapacitorSerieTresPrimeirosSlidesScene",
    "FirstFourSlidesScene",
    "FirstSlideScene",
    "FirstThreeSlidesScene",
    "FirstTwoSlidesScene",
    "SeriesCapacitorScene",
]
