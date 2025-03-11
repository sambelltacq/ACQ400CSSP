from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil, ScriptUtil

""" Ident all site DCs """

# Startup
logger = Logger.getLogger('ident_dc')
widget = locals()['widget']
display = widget.getTopDisplayModel()
timeout = 1000

# Functions
def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return {key: macros.getValue(key) for key in macros.names}

# Main
nchan = PVUtil.getLong(ScriptUtil.getPrimaryPV(widget))
macros = get_macros(display)

amount = 0
pvname = "{UUT}:{SITE}:AO:SLOW_SET:CH:{chan}"
for chan in range(1, nchan + 1):
    amount += 0.125
    macros['chan'] = chan
    PVUtil.writePV(pvname.format(**macros), amount, timeout)