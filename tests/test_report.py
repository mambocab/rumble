from simpletimeit import report


def test_title_empty_group_name():
    a = 'a=10, "foo"'
    assert report._title_from_group_and_args('', a) == 'args: {}'.format(a)
