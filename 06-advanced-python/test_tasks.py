import pytest
from .task1 import PrintableFolder, PrintableFile
from .task2 import Graph
from .task3 import ShiftDescriptor


@pytest.fixture
def make_testdir():
    class GetPrintable:
        file_1 = PrintableFile('file_1')
        file_2 = PrintableFile('file_2')
        file_3 = PrintableFile('file_3')
        file_4 = PrintableFile('file_4')

        folder_1 = PrintableFolder('Folder_1', [])
        folder_2 = PrintableFolder('Folder_2', [file_1])
        folder_3 = PrintableFolder('Folder_3', [folder_1, folder_2, file_2])
        folder_4 = PrintableFolder('Folder_4', [folder_3, file_3])
        folder_5 = PrintableFolder('Folder_5', [folder_4, file_4])

    return GetPrintable


def test_printablefolder(make_testdir, capsys):
    result_out = ['V Folder_5', '|    V Folder_4', '|    |    V Folder_3', '|    |    |    V Folder_1',
                  '|    |    |    V Folder_2', '|    |    |    |-> file_1', '|    |    |-> file_2',
                  '|    |-> file_3', '|-> file_4\n']
    printablefolder = make_testdir.folder_5
    print(printablefolder)
    captured = capsys.readouterr()
    assert captured.out == '\n'.join(result_out)


def test_printablefile(capsys, make_testdir):
    print(make_testdir.file_1 in make_testdir.folder_5)
    captured = capsys.readouterr()
    assert captured.out == 'True\n'

    print(make_testdir.file_1 in make_testdir.folder_1)
    captured = capsys.readouterr()
    assert captured.out == 'False\n'

    print(make_testdir.folder_5 in make_testdir.folder_4)
    captured = capsys.readouterr()
    assert captured.out == 'False\n'

    print(make_testdir.folder_1 in make_testdir.folder_5)
    captured = capsys.readouterr()
    assert captured.out == 'True\n'


@pytest.mark.parametrize('graph, expected', [
    ({'A':[]}, ['A']), ({'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['F', 'G']}, ['A', 'B', 'C', 'D', 'E', 'F', 'G']),
    ({'A': ['B', 'C', 'D'], 'B': ['C'], 'C': [], 'D': ['A']}, ['A', 'B', 'C', 'D'])])
def test_graph_iter(graph, expected):
    assert list(Graph(graph)) == expected


@pytest.fixture
def get_messages():
    class CeaserSipher:
        message_1 = ShiftDescriptor(1)
        message_2 = ShiftDescriptor(1)
        message_3 = ShiftDescriptor(26)
        message_4 = ShiftDescriptor(30)

    return CeaserSipher


def test_descriptor(get_messages):
    b = get_messages()
    b.message_1 = 'abc'
    b.message_2 = 'def'
    b.message_3 = 'abc'
    b.message_4 = 'abc'

    assert b.message_1 == 'bcd'
    assert b.message_2 == 'efg'
    assert b.message_3 == 'abc'
    assert b.message_4 == 'efg'
