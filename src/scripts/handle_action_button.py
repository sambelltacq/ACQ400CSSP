import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import ScriptUtil

""" Action button handler """

# Startup
logger = Logger.getLogger('handle_action_button')
widget = locals()['widget']
display = widget.getTopDisplayModel()

#Functions
def get_macros(widget):
    macros = widget.getEffectiveMacros()
    extracted = {}
    for key in macros.names:
        extracted[key] = macros.getValue(key)
    return extracted

def get_target(widget, propname="tooltip"):
    prop = widget.getPropertyValue(propname).split(' ')
    if len(prop) > 2:
        prop[2] = dict(kv.split('=') for kv in prop[2].split('/'))
    else:
        prop.append({})
    return prop[0], prop[1], prop[2]


macros = {}
macros.update(get_macros(widget))
macros.update(get_macros(display))

# Combine macros from display, widget and button
cmd, target, button_macros = get_target(widget)
macros.update(button_macros)
macros['timestamp'] = str(int(time.time()))

logger.info('Pressed button {} {}'.format(cmd, target))

if cmd == 'open':
    ScriptUtil.openDisplay(display, target, "TAB", macros)