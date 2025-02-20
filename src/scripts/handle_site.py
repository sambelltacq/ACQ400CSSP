from java.util.logging import Logger
from org.phoebus.framework.macros import Macros
from org.csstudio.display.builder.runtime.script import PVUtil

""" Init macros and local pvs """

# Startup
logger = Logger.getLogger('handle_site')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()

#Main
site = PVUtil.getString(pvs[0])
display.getEffectiveMacros().add("SITE", str(site))
logger.info("SITE set {}".format(site))