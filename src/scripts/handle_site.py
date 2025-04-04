import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil, DataUtil
from org.phoebus.framework.macros import Macros

""" Updates the current site """

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

macros = get_macros(widget)

site_val = PVUtil.getLong(pvs[0])
model = pvs[1]

model_val = macros['SITE_{}_MODEL'.format(site_val)]
model.setValue(model_val)
logger.info('Current Site: {} Model: {}'.format(site_val, model_val))