import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil
from  org.csstudio.display.builder.model.properties import WidgetColor

""" Init Strip Plot from macros """

# Startup
logger = Logger.getLogger('init traces')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()

colors = (
    (21, 21, 196), # Blue
    (242, 26, 26), # Red
    (33, 179, 33), # Green
    (0, 0, 0), # Black
    (128, 0, 255), # Purple
    (255, 170, 0), # Orange
    (255, 0, 240), #Magenta
    (243, 132, 132), #Coral
)

# Functions

class DotDict(dict):
    __delattr__ = dict.__delitem__
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return DotDict({key: macros.getValue(key) for key in macros.names})

def list_of_channels(chanstr):
    result = []
    for part in chanstr.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            result.extend(range(start, end + 1))
            continue
        result.append(int(part))
    return result

def read_pv(pvname):
    timeout = 1000
    try: PV = PVUtil.createPV(pvname, timeout)
    except: return False
    return PVUtil.getVType(PV).getValue()



# Main
"""
Macro Args

UUT         Target uut
SITE        Target site 0-6: to Module -1: to UUT
NSITES      Total sites
strip_chans channels to plot ie 1,2,3,4-8
pv_fmt      Trace pv format ie "=elementAt({UUT}:0:SLOWMON:MEAN, {chan} - 1)"
name_fmt    Trace name format ie "{UUT}:{SITE}:{chan}
max_traces  Max traces to allow 1-8
"""

macros = get_macros(widget)

uut = macros.UUT
site = int(macros.SITE)
nsites = int(macros.NSITES)
pv_fmt = macros.pv_fmt
name_fmt = macros.name_fmt
max_traces = int(macros.max_traces)

chans = list_of_channels(macros.pchans)
chanmap = {site: chans}

if site < 0:
    current = 0
    chanmap = {}
    for site_idx in range(1, nsites + 1):
        if not len(chans) > 0: break
        nchan_pv = "{}:{}:NCHAN".format(uut, site_idx)
        nchan = current + read_pv(nchan_pv)
        chanmap[site_idx] = []
        while len(chans) > 0:
            if chans[0] > nchan: break
            chanmap[site_idx].append(chans.pop(0) - current)
        current = nchan

current = 0
for site in chanmap:
    macros.site = site
    for chan in chanmap[site]:
        if current >= max_traces: break
        macros.site = site
        macros.chan = chan
        trace_pv = pv_fmt.format(**macros)
        trace_name = name_fmt.format(**macros)
        trace_color = WidgetColor(*colors[current])

        logger.info("CH{} PV {} Trace {} Name {}".format(chan, trace_pv, current, trace_name))
        widget.setPropertyValue("traces[{}].color".format(current), trace_color)
        widget.setPropertyValue("traces[{}].name".format(current), trace_name)
        widget.setPropertyValue("traces[{}].y_pv".format(current), trace_pv)

        current += 1

