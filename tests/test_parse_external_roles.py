import textwrap
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from parse_external_roles import parse_file


def write_xml(tmp_path, xml):
    path = tmp_path / 'sample.xml'
    path.write_text(textwrap.dedent(xml))
    return path


def test_parse_file_participation_missing_fields(tmp_path):
    xml = '''
    <root>
      <participationDirigeantDto>
        <items>
          <items>
            <nomStructure>OrgA</nomStructure>
            <dateDebut>2020-01-01</dateDebut>
          </items>
          <items>
            <descriptionActivite>RoleB</descriptionActivite>
            <dateFin>2021-12-31</dateFin>
          </items>
        </items>
      </participationDirigeantDto>
    </root>
    '''
    path = write_xml(tmp_path, xml)
    rows = parse_file(path)
    assert rows == [
        ['sample.xml', 'participationDirigeant', 'OrgA', '', '', '2020-01-01', ''],
        ['sample.xml', 'participationDirigeant', '', 'RoleB', '', '', '2021-12-31'],
    ]


def test_parse_file_benevole_missing_fields(tmp_path):
    xml = '''
    <root>
      <fonctionBenevoleDto>
        <items>
          <items>
            <nomStructure>CharityX</nomStructure>
          </items>
          <items>
            <descriptionActivite>Helper</descriptionActivite>
            <remuneration><montant>100</montant></remuneration>
            <dateDebut>2020-05-05</dateDebut>
          </items>
        </items>
      </fonctionBenevoleDto>
    </root>
    '''
    path = write_xml(tmp_path, xml)
    rows = parse_file(path)
    assert rows == [
        ['sample.xml', 'fonctionBenevole', 'CharityX', '', '', '', ''],
        ['sample.xml', 'fonctionBenevole', '', 'Helper', '100.0', '2020-05-05', ''],
    ]

