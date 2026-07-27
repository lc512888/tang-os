"""TangExtension — DI-001: Capability Construction, Not Identity Authoring.

Developers build Extensions here. They cannot create personas.
"""

from src.tang_os_sdk.manifest.models import ManifestModel


class TangExtension:
    """SDK entry point for creating a Tang OS Extension.

    Usage:
        ext = TangExtension("fall_detector", "检测老年人跌倒")
        ext.set_category("C3").add_permission("sensor_read")
        manifest = ext.build()
    """

    def __init__(self, extension_id: str, purpose: str):
        self._manifest = ManifestModel(
            extension_id=extension_id,
            purpose=purpose,
            category="C1",
            authority_level="A1",
        )

    def set_category(self, category: str) -> "TangExtension":
        self._manifest.category = category; return self

    def set_authority_level(self, level: str) -> "TangExtension":
        self._manifest.authority_level = level; return self

    def add_permission(self, perm: str) -> "TangExtension":
        self._manifest.required_permissions.append(perm); return self

    def set_human_impact(self, impact: str) -> "TangExtension":
        self._manifest.human_impact = impact; return self

    def set_risk_class(self, risk: str) -> "TangExtension":
        self._manifest.risk_class = risk; return self

    def build(self) -> ManifestModel:
        return self._manifest
