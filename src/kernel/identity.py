"""Identity Runtime — Core-001 Identity Constitution enforcement.

Three-layer hierarchy: 益友(companion) → 智者(wise) → 倾听者(listener).
Each layer has distinct behavioural constraints frozen from the Core Standard.
"""

from dataclasses import dataclass, field
from src.kernel.models import IdentityLayer
from src.kernel.exceptions import IdentityViolationError


@dataclass
class IdentityTransition:
    """Record of a layer activation."""
    from_layer: IdentityLayer
    to_layer: IdentityLayer
    context: dict


@dataclass
class IdentityProfile:
    """Serialisable identity profile that persists across sessions."""
    current_layer: IdentityLayer = IdentityLayer.LISTENER
    context_tags: list[str] = field(default_factory=list)


DISMISSAL_PATTERNS = [
    "别想太多",
    "这没什么大不了",
    "你太敏感了",
    "至于吗",
    "放宽心就好",
]

CONDESCENSION_PATTERNS = [
    "你这个层次",
    "你理解不了",
    "你不懂",
    "以你的水平",
]

ESCAPE_PATTERNS = [
    "我只是个",
    "别问我",
    "这不关我的事",
    "我不管",
]


class IdentityRuntime:
    """Enforces the Identity Constitution (Core-001).

    Validates that responses and actions conform to the active identity layer,
    preventing identity drift, condescension, and responsibility evasion.
    """

    def __init__(self, profile: IdentityProfile | None = None):
        self._profile = profile or IdentityProfile()
        self._transcript: list[IdentityTransition] = []

    @property
    def current_layer(self) -> IdentityLayer:
        return self._profile.current_layer

    @property
    def transcript(self) -> list[IdentityTransition]:
        return list(self._transcript)

    @property
    def profile(self) -> IdentityProfile:
        return self._profile

    def can_escalate_to(self, target: IdentityLayer) -> bool:
        """Check whether the target layer is reachable from the current layer."""
        layers = list(IdentityLayer)
        current_idx = layers.index(self.current_layer)
        target_idx = layers.index(target)
        return target_idx <= current_idx  # higher priority = lower index

    def activate_layer(self, layer: IdentityLayer, context: dict | None = None) -> None:
        """Activate a new identity layer with required context.

        Raises IdentityViolationError if:
        - Already at the requested layer
        - Missing required context for promotion
        """
        context = context or {}

        if layer == self.current_layer:
            raise IdentityViolationError(f"Already at {layer.value} layer")

        # Layer hierarchy enforcement
        if not self.can_escalate_to(layer):
            raise IdentityViolationError(
                f"Cannot descend from {self.current_layer.value} to {layer.value}"
            )

        # Context validation per layer
        if layer == IdentityLayer.COMPANION and not context:
            raise IdentityViolationError(
                "Promoting to 益友 requires emotional context"
            )

        from_layer = self.current_layer
        self._profile.current_layer = layer
        self._transcript.append(IdentityTransition(
            from_layer=from_layer,
            to_layer=layer,
            context=context
        ))

    def validate_response(self, response: str) -> bool:
        """Validate that a response conforms to the active identity layer.

        Raises IdentityViolationError on violation.
        Returns True if valid.
        """
        if not response:
            return True  # empty responses are not violations

        if self.current_layer == IdentityLayer.WISE:
            self._check_wise_constraints(response)
        elif self.current_layer == IdentityLayer.COMPANION:
            self._check_companion_constraints(response)
        elif self.current_layer == IdentityLayer.LISTENER:
            self._check_listener_constraints(response)

        return True

    def get_profile_state(self) -> IdentityProfile:
        """Return current profile for serialisation."""
        return self._profile

    # --- Layer-specific constraint checks ---

    def _check_wise_constraints(self, response: str) -> None:
        """Core-001: 不以智者姿态否定情绪."""
        for pattern in DISMISSAL_PATTERNS:
            if pattern in response:
                raise IdentityViolationError(
                    f"Wise layer must not dismiss emotions: contains '{pattern}'"
                )

    def _check_companion_constraints(self, response: str) -> None:
        """Core-001: 不以身份降维回应痛苦."""
        for pattern in CONDESCENSION_PATTERNS:
            if pattern in response:
                raise IdentityViolationError(
                    f"Companion layer must not condescend: contains '{pattern}'"
                )

    def _check_listener_constraints(self, response: str) -> None:
        """Core-001: 不以倾听者角色逃避责任."""
        for pattern in ESCAPE_PATTERNS:
            if pattern in response:
                raise IdentityViolationError(
                    f"Listener must not escape responsibility: contains '{pattern}'"
                )
