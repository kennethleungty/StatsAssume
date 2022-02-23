# ==========================
# Module: Logging
# Author: Kenneth Leung
# Last Modified: 30 Jan 2022
# ==========================

try:
    from loguru import logger
    logger.remove()  # Remove default 'stderr' sink (and all others, if any)
    # logger.add('logs/autoassume_check.log', mode="w")
    logger.add("logs/statsassume_check.log", rotation="10 MB", mode="w")
except ImportError:
    import logging
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("statsassume")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
