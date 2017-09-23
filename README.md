# Async Fluentd client for Tornado 4

## Install

```
pip3 install tornado_fluent
```

## Usage

```python
import tornado_fluent as ptf

ptf.send_message(host="your.server.local",
                 port=24224, tag="foo.bar", msg={"message": "foo", "abc": 123})
```

```python
import tornado_fluent as ptf
msgs = [
        {"message": "foo", "abc": 123},
        {"message": "bar", "abc": 123},
        {"message": "baz", "abc": 123}
    ]

ptf.send_messages(host="your.server.local",
                 port=24224, tag="foo.bar", msgs=msgs)
```

```python
import tornado_fluent as ptf

ptf.send_message_with_timestamp(host="your.server.local",
                 port=24224, tag="foo.bar", msg={"message": "foo", "abc": 123}, ts=1441588984)
```

```python
import tornado_fluent as ptf
msgs = [
    [1441588984, {"message": "foo"}],
    [1441588985, {"message": "bar"}],
    [1441588986, {"message": "baz"}]
]

ptf.send_messages_with_timestamp(host="your.server.local",
                 port=24224, tag="foo.bar", msgs=msgs)
```