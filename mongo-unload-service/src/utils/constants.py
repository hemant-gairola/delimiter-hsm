#
# Copyright (c) 2023 by Delphix. All rights reserved.
#

CONFIG_FILE_PATH = "src/config/default_config.ini"

# logging constants
ROTATION_CONDITION = 10485760  # 10MB
BACKUP_COUNT = 20
TRACE = 8
FORMATTER = "%(asctime)s — %(name)s — %(lineno)s — %(levelname)s — %(message)s"
DATEFORMAT = "%Y-%m-%d %H:%M:%S %Z"
