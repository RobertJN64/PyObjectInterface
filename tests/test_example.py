import pytest
import RobertJN64TemplatePackage as project


def test_add_one():
    assert project.add(5, 1) == 6

def test_error():
    with pytest.raises(Exception):
        project.error()

def test_file():
    assert project.openFile() == "Some text"

def test_tabulate(capture_stdout):
    project.printTable()
    assert capture_stdout['stdout'] == '  a    b    c\n---  ---  ---\n  1    2    3\n'
