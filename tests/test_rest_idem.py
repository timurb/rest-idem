import mock

from rest_idem import IdempotentRest


def test_diff_state():
    current = {'foo': 'bar',
               'baz': 'qux1',
               'hey': 'yo'}
    desired = {'foo': 'bar',
               'baz': 'qux',
               'bah': 'boom'}

    missing, extra = IdempotentRest.diff_state(current, desired)

    print missing, extra

    assert missing == {'baz': 'qux', 'bah': 'boom'}
    assert extra == {'baz': 'qux1', 'hey': 'yo'}


def test_delete():
    endpoint = mock.Mock()

    rest = IdempotentRest(endpoint)

    rest.delete({"foo": "bar", "baz": "qux"})

    endpoint.delete.assert_any_call({"foo": "bar"})
    endpoint.delete.assert_any_call({"baz": "qux"})


def test_post():
    endpoint = mock.Mock()

    rest = IdempotentRest(endpoint)

    rest.post({"foo": "bar", "baz": "qux"})

    endpoint.post.assert_any_call({"foo": "bar"})
    endpoint.post.assert_any_call({"baz": "qux"})


def test_match():
    endpoint = mock.Mock()
    endpoint.get.return_value = {'foo': 'bar',
                                 'baz': 'qux1',
                                 'hey': 'yo'}

    desired = {'foo': 'bar',
               'baz': 'qux',
               'bah': 'boom'}

    rest = IdempotentRest(endpoint)
    missing, extra = rest.match(desired)

    assert missing == {'baz': 'qux', 'bah': 'boom'}
    assert extra == {'baz': 'qux1', 'hey': 'yo'}


def test_update():
    endpoint = mock.Mock()
    endpoint.get.return_value = {'foo': 'bar',
                                 'baz': 'qux1',
                                 'hey': 'yo'}

    desired = {'foo': 'bar',
               'baz': 'qux',
               'bah': 'boom'}

    rest = IdempotentRest(endpoint)
    missing, extra = rest.update(desired)

    assert missing == {'baz': 'qux', 'bah': 'boom'}
    assert extra == {'baz': 'qux1', 'hey': 'yo'}

    endpoint.delete.assert_any_call({"hey": "yo"})
    endpoint.delete.assert_any_call({"baz": "qux1"})
    endpoint.post.assert_any_call({"bah": "boom"})
    endpoint.post.assert_any_call({"baz": "qux"})
