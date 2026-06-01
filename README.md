# Structured Logging System

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-261230?style=for-the-badge)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?style=for-the-badge&logo=pre-commit)](https://pre-commit.com/)

A lightweight Python structured logging library that outputs JSON-formatted log entries to stdout. Designed for cloud-native applications, containerized environments, and log aggregation systems (ELK, Loki, Datadog, etc.).

---

## Features

- **JSON Output** — Every log entry is a valid JSON object, parseable by any log shipper
- **Structured Context** — Attach arbitrary key-value context to any log message
- **Exception Serialization** — Automatically captures exception type and message in log entries
- **Level Support** — `debug`, `info`, `warn`, `error`, `critical` with standard Python logging levels
- **Zero Dependencies** — Uses only the Python standard library (`logging`, `json`, `sys`)
- **Simple API** — Single `get_logger()` factory function with familiar interface

## Installation

```bash
# Clone the repository
git clone https://github.com/Raphasha27/structured-logging-system.git
cd structured-logging-system

# Install with pip
pip install -e .
```

## Quick Start

```python
from python.logger import get_logger

log = get_logger("myapp")

log.info("Application started", context={"env": "production", "version": "2.1.0"})
log.warn("High memory usage", context={"memory_mb": 2048})
log.error("Failed to connect", context={"host": "db.example.com"})
```

Output:

```json
{"level": "INFO", "message": "Application started", "timestamp": "2026-06-01T12:00:00+00:00", "logger": "myapp", "module": "example", "line": 5, "context": {"env": "production", "version": "2.1.0"}}
{"level": "WARNING", "message": "High memory usage", "timestamp": "2026-06-01T12:00:00+00:00", "logger": "myapp", "module": "example", "line": 6, "context": {"memory_mb": 2048}}
{"level": "ERROR", "message": "Failed to connect", "timestamp": "2026-06-01T12:00:00+00:00", "logger": "myapp", "module": "example", "line": 7, "context": {"host": "db.example.com"}}
```

## API Reference

### `get_logger(name: str = "app", level: int = logging.INFO) -> StructuredLogger`

Creates a new structured logger instance.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | `str` | `"app"` | Logger name (appears in JSON output) |
| `level` | `int` | `logging.INFO` | Minimum log level |

### `StructuredLogger`

| Method | Signature | Description |
|--------|-----------|-------------|
| `debug` | `(msg: str, context: Optional[dict] = None)` | Log at DEBUG level |
| `info` | `(msg: str, context: Optional[dict] = None)` | Log at INFO level |
| `warn` | `(msg: str, context: Optional[dict] = None)` | Log at WARNING level |
| `error` | `(msg: str, context: Optional[dict] = None)` | Log at ERROR level |
| `critical` | `(msg: str, context: Optional[dict] = None)` | Log at CRITICAL level |

All methods accept an optional `context` dict for structured metadata.

### JSON Log Format

```json
{
  "level": "INFO",
  "message": "Human-readable message",
  "timestamp": "2026-06-01T12:00:00+00:00",
  "logger": "app",
  "module": "my_module",
  "line": 42,
  "context": { "key": "value" },
  "exception": {
    "type": "ValueError",
    "message": "invalid literal for int()"
  }
}
```

The `exception` field is only present when logging from an exception handler.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check python/
ruff format python/ --check
```

## Integration Examples

**Logstash / Filebeat**: Ship the stdout JSON directly — no parsing configuration needed.

**Docker**: The logger writes to stdout, so container logs are automatically structured.

```dockerfile
CMD ["python", "-m", "myapp"]
# docker logs will show JSON
```

## License

MIT License. See [LICENSE](LICENSE) for details.

---

© 2026 **Kirov Dynamics Technology** | Built by **Koketso Raphasha (Raphasha27)**
