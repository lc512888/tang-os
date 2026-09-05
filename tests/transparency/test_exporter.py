"""Tests: Description Exporter — multiple format outputs."""

import yaml

from tang_os.transparency.exporter import DescriptionExporter


class TestExporter:
    def test_to_dict(self):
        exp = DescriptionExporter()
        d = exp.to_dict()
        assert d["identity"]["name"] == "Tang OS"

    def test_to_yaml(self):
        exp = DescriptionExporter()
        y = exp.to_yaml()
        assert "controlled_by" in y.lower()
        assert "permitted: false" in y

    def test_to_markdown(self):
        exp = DescriptionExporter()
        md = exp.to_markdown()
        assert "# Tang OS System Description" in md

    def test_to_json(self):
        exp = DescriptionExporter()
        j = exp.to_json()
        assert '"name": "Tang OS"' in j

    def test_all_formats_consistent(self):
        exp = DescriptionExporter()
        d = exp.to_dict()
        y = exp.to_yaml()
        md = exp.to_markdown()
        assert d["specification"]["version"] == "1.0"
        assert yaml.safe_load(y)["specification"]["version"] == "1.0"
        assert "Version: 1.0" in md

    def test_yaml_is_safe_loadable_and_matches_description(self):
        exp = DescriptionExporter()
        assert yaml.safe_load(exp.to_yaml()) == exp.to_dict()

    def test_yaml_serializes_missing_verification_values_as_null(self):
        loaded = yaml.safe_load(DescriptionExporter().to_yaml())
        assert loaded["verification"]["test_count"] is None
        assert loaded["verification"]["last_validated"] is None
