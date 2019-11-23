#!/usr/bin/env python3
import io
import re
import grep


def test_integrate_stdin_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\npref needle? suf\n'


def test_integrate_stdin_regex_grep(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle?\nneedle? suf\nthe needl\npref needle? suf'))
    grep.main(['-E', 'needle?'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle?\nneedle? suf\nthe needl\npref needle? suf\n'


def test_integrate_stdin_grep_count(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', io.StringIO(
        'pref needle\nneedle suf\nthe needl\npref needle suf'))
    grep.main(['-c', 'needle'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '3\n'


def test_integrate_file_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'pref needle suf\n'


def test_integrate_files_grep(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:pref needle suf\na.txt:pref needle\na.txt:needle suf\n'


def test_integrate_files_grep_count(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('pref needle\nneedle suf\n')
    (tmp_path / 'b.txt').write_text('the needl\npref needle suf')
    monkeypatch.chdir(tmp_path)
    grep.main(['-c', 'needle', 'b.txt', 'a.txt'])
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'b.txt:1\na.txt:2\n'


def test_integrate_print_in_many_inputs_1(capsys):
    list_ = ['Line_1', 'Line_2', 'Line_3', 'Line_4']
    grep.print_in_many_inputs('file_name', list_)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file_name:Line_1\nfile_name:Line_2\nfile_name:Line_3\nfile_name:Line_4\n'


def test_integrate_print_in_many_inputs_2(capsys):
    list_ = ['10']
    grep.print_in_many_inputs('file_name', list_)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file_name:10\n'


def test_integrate_print_in_many_inputs_3(capsys):
    list_ = []
    grep.print_in_many_inputs('file_name', list_)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == ''


def test_integrate_print_single_input_1(capsys):
    list_ = ['Line_1', 'Line_2', 'Line_3', 'Line_4']
    grep.print_single_input(list_)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Line_1\nLine_2\nLine_3\nLine_4\n'


def test_integrate_print_single_input_2(capsys):
    list_ = ['61261242851875618374653453245862345235']
    grep.print_single_input(list_)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '61261242851875618374653453245862345235\n'


def test_integrate_print_line_in_file_1(capsys):
    list_ = ['Line_1', 'Line_2', 'Line_3', 'Line_4']
    grep.print_line_in_file(list_, 'file_name', 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file_name:Line_1\nfile_name:Line_2\nfile_name:Line_3\nfile_name:Line_4\n'
    assert len(list_) == 0


def test_integrate_print_line_in_file_2(capsys):
    list_ = ['Line_1', 'Line_2', 'Line_3', 'Line_4']
    grep.print_line_in_file(list_, 'file_name', 0)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'Line_1\nLine_2\nLine_3\nLine_4\n'


def test_integrate_print_line_in_file_3(capsys):
    list_ = ['10']
    grep.print_line_in_file(list_, 'file_name', 1)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'file_name:10\n'
    assert len(list_) == 0


def test_integrate_print_line_in_file_4(capsys):
    list_ = ['10']
    grep.print_line_in_file(list_, 'file_name', 0)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '10\n'


def test_integrate_save_line_1():
    line = 'example of line with\n'
    lines = []
    pattern = re.escape('exam')
    lines = grep.save_line(line, pattern)
    assert len(lines) == 1
    assert lines[0] == 'example of line with'


def test_integrate_save_line_2():
    line = 'example of line with\n'
    lines = []
    pattern = re.escape('ex.m')
    lines = grep.save_line(line, pattern)
    assert len(lines) == 0


def test_integrate_save_line_3():
    line = 'example of line with\n'
    pattern = 'ex.m'
    lines = grep.save_line(line, pattern)
    # assert len(lines) == 1
    assert lines[0] == 'example of line with'


def test_integrate_save_line_4():
    line = 'example of line with\n'
    lines = []
    pattern = 'exami.ate'
    lines = grep.save_line(line, pattern)
    assert len(lines) == 0


def test_integrate_lines_in_files_1(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    files = ['a.txt']
    monkeypatch.chdir(tmp_path)
    pattern = re.escape('needle')
    grep.lines_in_files(pattern, 0, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needless\n'


def test_integrate_lines_in_files_2(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    files = ['a.txt']
    monkeypatch.chdir(tmp_path)
    pattern = re.escape('needle')
    grep.lines_in_files(pattern, 1, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_lines_in_files_3(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    files = ['a.txt']
    monkeypatch.chdir(tmp_path)
    pattern = 'ne.dle'
    grep.lines_in_files(pattern, 0, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'needless\n'


def test_integrate_lines_in_files_4(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    files = ['a.txt']
    monkeypatch.chdir(tmp_path)
    pattern = 'needle.s'
    grep.lines_in_files(pattern, 1, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == '1\n'


def test_integrate_lines_in_files_5(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('needle noodle\ndoodle')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = re.escape('needle')
    grep.lines_in_files(pattern, 0, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needless\nb.txt:needle noodle\n'


def test_integrate_lines_in_files_6(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('needle noodle\ndoodle')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = re.escape('needle')
    grep.lines_in_files(pattern, 1, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:1\n'


def test_integrate_lines_in_files_7(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('lorem ipsum')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = re.escape('needle')
    grep.lines_in_files(pattern, 0, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needless\n'


def test_integrate_lines_in_files_8(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('dolor sin amet')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = re.escape('needle')
    grep.lines_in_files(pattern, 1, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:0\n'


def test_integrate_lines_in_files_9(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('needle noodle\ndoodle')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = 'n.ed.e'
    grep.lines_in_files(pattern, 0, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needless\nb.txt:needle noodle\n'


def test_integrate_lines_in_files_10(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('needle noodle\ndoodle')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = 'n.ed.e'
    grep.lines_in_files(pattern, 1, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:1\n'


def test_integrate_lines_in_files_11(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('lorem ipsum')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = 'n.ed.e'
    grep.lines_in_files(pattern, 0, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:needless\n'


def test_integrate_lines_in_files_12(tmp_path, monkeypatch, capsys):
    (tmp_path / 'a.txt').write_text('needless\nuseless')
    (tmp_path / 'b.txt').write_text('dolor sin amet')
    files = ['a.txt', 'b.txt']
    monkeypatch.chdir(tmp_path)
    pattern = 'n.ed.e'
    grep.lines_in_files(pattern, 1, files)
    out, err = capsys.readouterr()
    assert err == ''
    assert out == 'a.txt:1\nb.txt:0\n'
