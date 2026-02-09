import logging
import logging.handlers
import os
from pathlib import Path


def setup_logging():
    """Configure logging to write to both stdout and rotating files."""
    
    # Create logs directory if it doesn't exist
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Get log level from environment or default to INFO
    log_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(simple_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler for all logs (rotating)
    all_logs_handler = logging.handlers.RotatingFileHandler(
        filename=logs_dir / "service_alpha.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    all_logs_handler.setLevel(log_level)
    all_logs_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(all_logs_handler)
    
    # File handler for error logs only (rotating)
    error_logs_handler = logging.handlers.RotatingFileHandler(
        filename=logs_dir / "service_alpha_error.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding='utf-8'
    )
    error_logs_handler.setLevel(logging.ERROR)
    error_logs_handler.setFormatter(detailed_formatter)
    root_logger.addHandler(error_logs_handler)
    
    # File handler for parser runs (rotating)
    parser_logs_handler = logging.handlers.RotatingFileHandler(
        filename=logs_dir / "parser_runs.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10,
        encoding='utf-8'
    )
    parser_logs_handler.setLevel(logging.INFO)
    parser_logs_handler.setFormatter(detailed_formatter)
    
    # Create a separate logger for parser runs
    parser_logger = logging.getLogger("parser")
    parser_logger.setLevel(logging.INFO)
    parser_logger.addHandler(parser_logs_handler)
    parser_logger.propagate = False  # Don't propagate to root logger
    
    # Set specific loggers to appropriate levels
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)
    
    logging.info(f"Logging configured with level: {log_level_name}")
    logging.info(f"Log files will be written to: {logs_dir.absolute()}")