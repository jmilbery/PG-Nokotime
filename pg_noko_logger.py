#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Logger
# ---------------------------------------------------------------------------

import sys
import config

def log(level, module, message_string):
    if config.log_message:
        print("TYPE:",level, "MODULE:",module, "MESSAGE:", message_string)
    else:
        return