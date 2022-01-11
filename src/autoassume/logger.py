# ==========================
# Module: Logs
# Author: Kenneth Leung
# Last Modified: 31 Dec 2021
# ==========================

try:
    from loguru import logger
    
except ImportError:
    import logging
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger = logging.getLogger("pyassume")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)