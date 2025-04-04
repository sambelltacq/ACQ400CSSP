import time
from java.util.logging import Logger
from org.phoebus.framework.macros import Macros
from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil

""" Detect boot and reload display """

# Startup
t0 = time.time()
logger = Logger.getLogger('handle_boot')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()
timeout = 2 * 1000

# Functions

class DotDict(dict):
    __delattr__ = dict.__delitem__
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return DotDict({key: macros.getValue(key) for key in macros.names})

# Main
ioc_val = PVUtil.getLong(pvs[0])

if ioc_val == 0:
    logger.info("Booting is detected")
    display.setUserData("booting", True)

if ioc_val == 1 and display.getUserData("booting"):
    logger.info("Booting complete reloading")
    macros = get_macros(display)
    ScriptUtil.openDisplay(display, macros.LAUNCHER, "REPLACE", macros)
