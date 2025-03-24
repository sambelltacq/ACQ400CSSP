import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil, DataUtil
from org.phoebus.framework.macros import Macros


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

macros = get_macros(widget)

uut = PVUtil.getString(pvs[0])

if macros['UUT'] != uut:
    print("NEW uut")
    widget.setPropertyValue("file", "")
    macros['UUT'] = uut
    set_macros(widget, macros)
    widget.setPropertyValue("file", "opi/components/launcher/connected.bob")