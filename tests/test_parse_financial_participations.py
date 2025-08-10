from parse_financial_participations import parse_file


def test_parse_file_missing_or_empty_fields(tmp_path):
    xml_content = """
    <root>
      <participationFinanciereDto>
        <items>
          <items>
            <nomSociete>Acme Corp</nomSociete>
            <evaluation>1000</evaluation>
            <capitalDetenu></capitalDetenu>
            <nombreParts>10</nombreParts>
            <!-- remuneration missing -->
          </items>
          <items>
            <nomSociete>Foo LLC</nomSociete>
            <!-- other fields missing entirely -->
          </items>
        </items>
      </participationFinanciereDto>
    </root>
    """
    xml_path = tmp_path / "sample.xml"
    xml_path.write_text(xml_content)

    rows = list(parse_file(xml_path))
    assert rows == [
        {
            "file": "sample.xml",
            "nomSociete": "Acme Corp",
            "evaluation": "1000",
            "capitalDetenu": "",
            "nombreParts": "10",
            "remuneration": "",
        },
        {
            "file": "sample.xml",
            "nomSociete": "Foo LLC",
            "evaluation": "",
            "capitalDetenu": "",
            "nombreParts": "",
            "remuneration": "",
        },
    ]

