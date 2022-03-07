# ==========================
# Module: Logging
# Author: Kenneth Leung
# Last Modified: 07 Mar 2022
# ==========================

import logging
logging.basicConfig(filename='logs/statsassume.log',
                    filemode='w+',
                    force=True,
                    level=logging.INFO
                    )

logger = logging.getLogger()

# from loguru import logger
# logger.remove()  # Remove default 'stderr' sink (and all others, if any)
# # logger.add('logs/statsassume_check.log', mode="w")
# logger.add("logs/statsassume_check.log", rotation="10 MB", mode="w")
