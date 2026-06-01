import sys
import json
import io
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from python.logger import get_logger, StructuredLogger, JsonFormatter
import logging


def test_get_logger():
    log = get_logger("test-app")
    assert isinstance(log, StructuredLogger)


def test_logger_name():
    log = get_logger("custom-name")
    assert log._logger.name == "custom-name"


def test_info_log_output():
    log = get_logger("test-info")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    log._logger.addHandler(handler)
    log._logger.handlers[0].setFormatter(JsonFormatter())
    log._logger.handlers = [handler]

    log.info("hello world", context={"key": "val"})
    output = stream.getvalue()
    parsed = json.loads(output)
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "hello world"
    assert parsed["context"] == {"key": "val"}


def test_error_log_with_exception():
    log = get_logger("test-exc")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    log._logger.handlers = [handler]

    try:
        1 / 0
    except ZeroDivisionError:
        log.error("division error", context={"op": "div"})

    output = stream.getvalue()
    parsed = json.loads(output)
    assert parsed["level"] == "ERROR"
    assert parsed["context"]["op"] == "div"


def test_log_format_has_timestamp():
    log = get_logger("test-ts")
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    handler.setFormatter(JsonFormatter())
    log._logger.handlers = [handler]

    log.info("test")
    parsed = json.loads(stream.getvalue())
    assert "timestamp" in parsed
    assert "logger" in parsed
    assert "module" in parsed
    assert "line" in parsed


def test_level_methods():
    log = get_logger("test-levels")
    assert callable(log.debug)
    assert callable(log.info)
    assert callable(log.warn)
    assert callable(log.error)
    assert callable(log.critical)
