from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import ScriptUtil

""" Action button handler """

# Startup
logger = Logger.getLogger('handle_action_button')
widget = locals()['widget']
display = widget.getTopDisplayModel()

print(widget)
print(dir(widget))

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

cmd, target, macros = get_target(widget)

if cmd == 'open':
    #open a new opi display
    macros.update(get_macros(widget)) #merge display macros
    macros.update(get_macros(display)) #merge widget macros
    opi = "opi/{}".format(target)
    logger.info("{} {} {}".format(cmd, opi, macros))
    ScriptUtil.openDisplay(display, opi, "TAB", macros)