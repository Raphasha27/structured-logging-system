from logger import get_logger

log = get_logger("example")

log.info("Application started", context={"env": "production", "version": "1.0.0"})
log.warn("High memory usage detected", context={"memory_mb": 2048})
log.error("Database connection failed", context={"host": "postgres://db.internal"})

try:
    1 / 0
except ZeroDivisionError:
    log.error("Division by zero", context={"operation": "calculate_ratio"})
