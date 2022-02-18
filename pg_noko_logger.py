#----------------------------------------------------------------------------
# Created By  : JFM
# Created Date: 2020-01-26
# version ='1.0'
# Logger
# ---------------------------------------------------------------------------
""" Super simple stdout logging """
import sys
import config

#
# If you need a more complex suite of logging, then use python
# log libraries.  This is galatically simple.   We call this routine from
# everywhere else in the code -- you can add calls if you need more logging.
# The config.sys variable log_message will display the passed data to stdout
# if true -- otherwse it will ignore it
#
#
# We pass three variables for identification:
#
#   level -- set your own levels - i.e. INFO, WARNING, ERROR, ETC
#   module -- we usually pass in the library.method that is calling the log
#   message -- a message string containing anything that you want logged
#
def log(level, module, message_string):
    if config.log_message:
        print("TYPE:",level, "MODULE:",module, "MESSAGE:", message_string)
    else:
        return