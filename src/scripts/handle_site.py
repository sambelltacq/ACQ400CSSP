import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil, DataUtil
from org.phoebus.framework.macros import Macros

""" Finds the site module model """

# Startup
logger = Logger.getLogger('handle_site')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()
t0 = time.time()
timeout = 2 * 1000

# Functions
def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return {key: macros.getValue(key) for key in macros.names}

def set_macros(widget, macros):
    new_macros = Macros()
    for key in macros:
        new_macros.add(key, macros[key])
    widget.setPropertyValue("macros", new_macros)

def read_pv(pvname):
    try: PV = PVUtil.createPV(pvname, timeout)
    except: return False
    return PVUtil.getVType(PV).getValue()

# Main
macros = get_macros(display)
site = PVUtil.getLong(pvs[0])
uut = PVUtil.getString(pvs[1])

model = read_pv("loc://SITE_{}_MODEL ".format(site))
if not model: model = "none"
PVUtil.writePV("loc://SITE_MODEL", model, timeout)
macros['SITE_MODEL'] = model
set_macros(display, macros)
logger.info('Current Site: {} Model: {}'.format(site, model))