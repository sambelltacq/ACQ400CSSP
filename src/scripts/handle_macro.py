import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil, DataUtil
from org.phoebus.framework.macros import Macros

""" On pv change update macro """

# Startup
logger = Logger.getLogger('handle_macro')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()
t0 = time.time()

# Functions
def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return {key: macros.getValue(key) for key in macros.names}

def set_macros(widget, macros):
    new_macros = Macros()
    for key in macros:
        new_macros.add(key, str(macros[key]))
    widget.setPropertyValue("macros", new_macros)

# Main
macros = get_macros(display)
for pv in pvs:
    key = pv.name.replace('loc://', '').split('_WD')[0]
    value = PVUtil.getString(pv)
    if value == macros.get(key): continue
    macros[key] = str(value)
    logger.info("Updated {} macro to {}".format(key, value))

set_macros(display, macros)