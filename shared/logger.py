from loguru import logger as _logger


class AsyncLogger:
    async def debug(self, message: str) -> None:
        _logger.debug(message, enqueue=True)
        await _logger.complete()

    async def info(self, message: str) -> None:
        _logger.info(message, enqueue=True)
        await _logger.complete()

    async def warning(self, message: str) -> None:
        _logger.warning(message, enqueue=True)
        await _logger.complete()

    async def error(self, message: str) -> None:
        _logger.error(message, enqueue=True)
        await _logger.complete()

    async def critical(self, message: str) -> None:
        _logger.critical(message, enqueue=True)
        await _logger.complete()


logger = AsyncLogger()
