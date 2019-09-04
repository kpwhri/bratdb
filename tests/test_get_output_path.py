import pytest

from bratdb.funcs.utils import get_output_path


@pytest.mark.parametrize(('target', 'expected'), [
    (r'C:\test\example.pkl', r'C:\test\example.txt'),
    ('this.db', 'this.txt'),
    ('this.freq.db', 'this.txt'),
])
def test_default(target, expected):
    actual = get_output_path(target)
    assert expected == actual


@pytest.mark.parametrize(('target', 'expected', 'exts'), [
    (r'C:\test\example.pkl', r'C:\test\example.freq.docx', ('freq', 'docx')),
    ('this.db', 'this.freq.docx', ('freq', 'docx')),
    ('this.ext.db', 'this.freq.docx', ('freq', 'docx')),
])
def test_exts(target, expected, exts):
    actual = get_output_path(target, exts=exts)
    assert expected == actual


def test_valid_output():
    target = r'C:\test\example.pkl'
    outpath = expected = r'D:\test\this.txt'
    actual = get_output_path(target, outpath=outpath)
    assert expected == actual
