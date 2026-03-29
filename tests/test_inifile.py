from collections import OrderedDict
import pytest
from lektor.i18n import get_i18n_block
from inifile import IniFile as IniFileOrig
from lektor.inifile import IniFileNew

from lektor.utils import decode_flat_data

@pytest.fixture(scope="session")
def project_path(data_path):
    return data_path / "demo-project"


@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_initfile_no_header(tmp_path, IniFile):
    path = tmp_path / "project.ini"
    path.write_text("""
foo = bar
    """)
    inifile = IniFile(path)
    assert {'foo': 'bar'} == decode_flat_data(inifile.items(), dict_cls=OrderedDict)
    assert "bar" == inifile["foo"]


@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_me(project_path, IniFile):
    path = project_path / "Website.lektorproject"
    assert path.exists()

    inifile = IniFile(path)
    assert not inifile.is_new

    assert "Demo Project" == inifile.get("project.name")
    assert None == inifile.get("project.path")
    assert None == inifile.get("project.themes")
    assert "yes" == inifile.get("alternatives.en.primary")
    assert "en_US" == inifile.get("alternatives.en.locale")

    assert "English" == inifile.get("alternatives.en.name")
    assert {"en": "English", "de": "Englisch"} == get_i18n_block(
        inifile, "alternatives.en.name"
    )
    assert {"en": "German", "de": "Deutsch"} == get_i18n_block(
        inifile, "alternatives.de.name"
    )

    assert "Deutsch" == inifile.get("alternatives.de.name[de]")
    assert "Englisch" == inifile.get("alternatives.en.name[de]")

    assert {
        "name": "Demo Project",
        "excluded_assets": "foo*",
        "included_assets": "_*",
    } == inifile.section_as_dict("project")
    assert {".foo": "text"} == inifile.section_as_dict("attachment_types")
    assert {
        "name": "English",
        "name[de]": "Englisch",
        "primary": "yes",
        "locale": "en_US",
    } == inifile.section_as_dict("alternatives.en")
    pass
