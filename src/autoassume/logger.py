# ==========================
# Module: Logging
# Author: Kenneth Leung
# Last Modified: 12 Jan 2022
# ==========================

try:
    from loguru import logger
    logger.remove()  # Remove default 'stderr' sink (and all others, if any)
    # logger.add('logs/autoassume_check.log', mode="w")
    logger.add("logs/my_log_file.log", rotation="10 MB", mode="w")
except ImportError:
    import logging
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("autoassume")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
