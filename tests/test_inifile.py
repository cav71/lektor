from collections import OrderedDict
import pytest
from lektor.i18n import get_i18n_block
from lektor.inifile import IniFile as IniFileNew
try:
    from inifile import IniFile as IniFileOrig
except ModuleNotFoundError:
    IniFileOrig = None

from lektor.utils import decode_flat_data


@pytest.fixture(scope="session")
def project_path(data_path):
    return data_path / "demo-project"


@pytest.fixture(scope="session")
def samples_path(data_path):
    return data_path / "data"


@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_initfile_items_no_header(samples_path, IniFile):
    if not IniFile: pytest.skip("no inifile present")
    inifile = IniFile(samples_path / "inifile-empty.ini")
    assert [] == list(inifile.items())
    return
    assert {"foo": "bar"} == decode_flat_data(inifile.items(), dict_cls=OrderedDict)
    assert "bar" == inifile["foo"]


@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_initfile_items_header_only(samples_path, IniFile):
    if not IniFile: pytest.skip("no inifile present")
    inifile = IniFile(samples_path / "inifile-only-defaults.ini")
    assert [
        ("default", "value1"),
        ("default1", "123"),
        ("default2", "hello world"),
    ] == list(inifile.items())


@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_initfile_items_header_and_sections(samples_path, IniFile):
    if not IniFile: pytest.skip("no inifile present")
    inifile = IniFile(samples_path / "inifile-with-defaults.ini")
    expected = [
        ("default", "value1"),
        ("default1", "123"),
        ("default2", "hello world"),
        ("project.name", "Demo Project"),
        ("project.excluded_assets", "foo*"),
        ("alternatives.en.name", "English"),
        ("alternatives.en.name[de]", "Englisch"),
        ("servers.production.name", "Production"),
        ("servers.production.target", "rsync://myserver.com/path/to/website"),
        ("servers.production.name[de]", "Produktion"),
        ("attachment_types..foo", "text"),
    ]
    assert expected == list(inifile.items())


@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_initfile_get(samples_path, IniFile):
    if not IniFile: pytest.skip("no inifile present")
    inifile = IniFile(samples_path / "inifile-with-defaults.ini")

    assert "Produktion" == inifile.get("servers.production.name[de]") 
    assert "text" == inifile.get("attachment_types..foo")
    assert "Englisch" == inifile.get("alternatives.en.name[de]")
    assert "rsync://myserver.com/path/to/website" == inifile.get("servers.production.target")
    
    assert 11 == len(list(inifile.items()))
    inifile["opla"] = "99"
    assert 12 == len(list(inifile.items()))
    assert "99" == inifile["opla"]



@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_initfile_items_header_sections_only(samples_path, IniFile):
    if not IniFile: pytest.skip("no inifile present")
    inifile = IniFile(samples_path / "inifile-without-defaults.ini")
    expected = [
        ("project.name", "Demo Project"),
        ("project.excluded_assets", "foo*"),
        ("project.included_assets", "_*"),
        ("alternatives.en.name", "English"),
        ("alternatives.en.name[de]", "Englisch"),
        ("alternatives.en.primary", "yes"),
        ("alternatives.en.locale", "en_US"),
        ("alternatives.de.name", "German"),
        ("alternatives.de.name[de]", "Deutsch"),
        ("alternatives.de.url_prefix", "/de/"),
        ("alternatives.de.locale", "de_DE"),
        ("servers.production.enabled", "yes"),
        ("servers.production.name", "Production"),
        ("servers.production.target", "rsync://myserver.com/path/to/website"),
        ("servers.production.name[de]", "Produktion"),
        ("servers.production.extra_field", "extra_value"),
        ("attachment_types..foo", "text"),
    ]
    assert expected == list(inifile.items())




@pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
def test_project_parsing(project_path, IniFile):
    if not IniFile: pytest.skip("no inifile present")
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


# @pytest.mark.parametrize("IniFile", [IniFileOrig, IniFileNew])
# def test_save(tmp_path, project_path, IniFile):
#     if not IniFile: pytest.skip("no inifile present")
#     inifile = IniFile(str(tmp_path / "inifile-only-defaults.ini"))
#     path = tmp_path / "out.txt"
#     path.write_text("")
#     if hasattr(inifile, "_changes"):
#         inifile._changes = True
#     inifile.filename = str(path)
#     breakpoint()
#     inifile.save()
#     assert "" == path.read_text()
#     pass

