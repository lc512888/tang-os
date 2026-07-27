"""Production Promotion Gate — DI-004-A: Sandbox → Production validation.

Sandbox state cannot become production state automatically.
Must pass through: Scenario Test → Blind Validation → Certification → Registry.
"""


class PromotionGate:
    """Validates that sandbox state is ready for production promotion.

    Required pipeline (cannot skip):
    Scenario Test → Blind Validation → Certification → Registry

    Sandbox Memory → Production Memory: NOT allowed (DI-004-A).
    """

    def __init__(self):
        self._scenarios_passed = False
        self._validation_passed = False
        self._certification_passed = False
        self._log: list[str] = []

    @property
    def log(self) -> list[str]:
        return list(self._log)

    def mark_scenarios_passed(self) -> None:
        self._scenarios_passed = True
        self._log.append("SCENARIO_PASSED")

    def mark_validation_passed(self) -> None:
        self._validation_passed = True
        self._log.append("VALIDATION_PASSED")

    def mark_certification_passed(self) -> None:
        self._certification_passed = True
        self._log.append("CERTIFICATION_PASSED")

    def evaluate(self, runner=None, isolation=None) -> dict:
        """Evaluate whether sandbox state is ready for production.

        Without full pipeline, promotion is denied.
        """
        errors = []
        if not self._scenarios_passed:
            errors.append("Scenario Test not passed")
        if not self._validation_passed:
            errors.append("Blind Validation not passed")
        if not self._certification_passed:
            errors.append("Certification not passed")

        can_promote = len(errors) == 0
        return {
            "can_promote": can_promote,
            "errors": errors,
            "stages": {
                "scenario_test": self._scenarios_passed,
                "blind_validation": self._validation_passed,
                "certification": self._certification_passed,
            },
            "auto_migration_blocked": True,  # DI-004-A
        }

    def reset(self) -> None:
        self._scenarios_passed = False
        self._validation_passed = False
        self._certification_passed = False
        self._log = []
