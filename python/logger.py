import logging
import json
import sys
from datetime import datetime, timezone
from typing import Any, Optional


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "level": record.levelname,
            "message": record.getMessage(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
        }
        if hasattr(record, "context") and record.context:
            log_entry["context"] = record.context
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
            }
        return json.dumps(log_entry)


class StructuredLogger:
    def __init__(self, name: str = "app", level: int = logging.INFO):
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(JsonFormatter())
            self._logger.addHandler(handler)

    def _log(self, level: int, msg: str, context: Optional[dict] = None) -> None:
        extra = {"context": context} if context else {}
        self._logger.log(level, msg, extra=extra)

    def info(self, msg: str, context: Optional[dict] = None) -> None:
        self._log(logging.INFO, msg, context)

    def warn(self, msg: str, context: Optional[dict] = None) -> None:
        self._log(logging.WARNING, msg, context)

    def error(self, msg: str, context: Optional[dict] = None) -> None:
        self._log(logging.ERROR, msg, context)

    def debug(self, msg: str, context: Optional[dict] = None) -> None:
        self._log(logging.DEBUG, msg, context)

    def critical(self, msg: str, context: Optional[dict] = None) -> None:
        self._log(logging.CRITICAL, msg, context)


def get_logger(name: str = "app", level: int = logging.INFO) -> StructuredLogger:
    return StructuredLogger(name, level)
