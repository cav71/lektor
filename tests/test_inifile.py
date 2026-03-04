import pytest


@pytest.fixture(scope="session")
def webadmin(tmp_path_factory, project_path):
    project = Project.from_path(project_path)


@pytest.fixture(scope="session")
def project_path(data_path):
    return data_path / "demo-project"


def test_me(project_path):
    print(project_path)
