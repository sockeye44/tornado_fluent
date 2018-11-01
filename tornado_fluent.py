import msgpack
import random
import base64
import logging
import datetime
import time

from tornado import gen
from tornado.ioloop import IOLoop
from tornado.tcpclient import TCPClient

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 24224
READ_TIMEOUT_SEC = 2
CONN_TIMEOUT_SEC = 2
RETRY_COUNT = 2
RESP_MAX_SIZE = 64 * 1024

rd = random.Random()
logger = logging.getLogger('tornado_fluent')


def __gen_id():
    bits = rd.getrandbits(128)
    return base64.b64encode(bits.to_bytes(16, "big"))


@gen.coroutine
def read_callback(_data, request_id):
    try:
        data = msgpack.unpackb(_data)
    except Exception as e:
        logger.exception("bad response: " + str(_data))
        return False

    if data.get(b'ack') == request_id:
        return True
    else:
        logger.error('ack != request id: {}, {}'.format(data.get(b'ack'), request_id))
        return False


@gen.coroutine
def __send_messages(tag, msgs, host, port, conn_timeout_sec, read_timeout_sec):
    stream = yield gen.with_timeout(datetime.timedelta(seconds=conn_timeout_sec), TCPClient().connect(host, port))
    try:
        request_id = __gen_id()
        stream.write(msgpack.packb([
            tag,
            msgs,
            {"chunk": request_id}
        ]))
        data = yield gen.with_timeout(datetime.timedelta(seconds=read_timeout_sec), stream.read_bytes(RESP_MAX_SIZE, partial=True))
        ok = yield read_callback(data, request_id)
        return ok
    finally:
        stream.close()


@gen.coroutine
def send_messages_with_timestamp(tag, msgs, host=DEFAULT_HOST, port=DEFAULT_PORT, retry_count=RETRY_COUNT, conn_timeout_sec=CONN_TIMEOUT_SEC, read_timeout_sec=READ_TIMEOUT_SEC):
    # tag = "your.tag"
    # msgs = [
    #     [1441588984, {"message": "foo"}],
    #     [1441588985, {"message": "bar"}],
    #     [1441588986, {"message": "baz"}]
    # ]
    try:
        res = yield __send_messages(tag, msgs, host, port, conn_timeout_sec, read_timeout_sec)
    except Exception as e:
        logger.exception("error!")
        if retry_count > 0:
            logger.error("retrying...")
            res = yield send_messages_with_timestamp(tag, msgs, host, port, retry_count - 1, conn_timeout_sec, read_timeout_sec)
        else:
            logger.error("no retries left")
            return False
    return res


@gen.coroutine
def send_messages(tag, msgs, host=DEFAULT_HOST, port=DEFAULT_PORT, retry_count=RETRY_COUNT, conn_timeout_sec=CONN_TIMEOUT_SEC, read_timeout_sec=READ_TIMEOUT_SEC):
    # tag = "your.tag"
    # msgs = [
    #     {"message": "foo"},
    #     {"message": "bar"},
    #     {"message": "baz"}
    # ]
    _msgs = []
    for msg in msgs:
        _msg = [int(time.time()), msg]
        _msgs.append(_msg)

    res = yield send_messages_with_timestamp(tag, _msgs, host, port, retry_count, conn_timeout_sec, read_timeout_sec)
    return res


@gen.coroutine
def send_message_with_timestamp(tag, msg, ts, host=DEFAULT_HOST, port=DEFAULT_PORT, retry_count=RETRY_COUNT, conn_timeout_sec=CONN_TIMEOUT_SEC, read_timeout_sec=READ_TIMEOUT_SEC):
    # tag = "your.tag"
    # msg = {"message": "foo"}
    # ts = 1441588984
    _msgs = [[ts, msg]]
    res = yield send_messages_with_timestamp(tag, _msgs, host, port, retry_count, conn_timeout_sec, read_timeout_sec)
    return res


@gen.coroutine
def send_message(tag, msg, host=DEFAULT_HOST, port=DEFAULT_PORT, retry_count=RETRY_COUNT, conn_timeout_sec=CONN_TIMEOUT_SEC, read_timeout_sec=READ_TIMEOUT_SEC):
    # tag = "your.tag"
    # msg = {"message": "foo"}
    _msgs = [[int(time.time()), msg]]
    res = yield send_messages_with_timestamp(tag, _msgs, host, port, retry_count, conn_timeout_sec, read_timeout_sec)
    return res
