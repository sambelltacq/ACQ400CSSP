import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil, DataUtil
from org.phoebus.framework.macros import Macros

""" Update Macro when changed """

# Startup
logger = Logger.getLogger('handle_macro')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()
t0 = time.time()

def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return {key: macros.getValue(key) for key in macros.names}

def set_macros(widget, macros):
    new_macros = Macros()
    for key in macros:
        new_macros.add(key, macros[key])
    widget.setPropertyValue("macros", new_macros)

# Main
macros = get_macros(display)

for pv in pvs:
    pvname = pv.getName().split('://')[-1]
    pvvalue = PVUtil.getString(pv)
    macros[pvname] = str(pvvalue)
    logger.info("Updated {} macro to {}".format(pvname, pvvalue))

set_macros(widget, macros)