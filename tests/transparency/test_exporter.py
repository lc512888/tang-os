"""Tests: Description Exporter — multiple format outputs."""

from src.tang_os.transparency.exporter import DescriptionExporter


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
        assert "version: 1.0" in y
        assert "Version: 1.0" in md
