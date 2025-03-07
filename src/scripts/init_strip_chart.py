import time
from java.util.logging import Logger
from org.csstudio.display.builder.runtime.script import PVUtil

""" Init Strip Plot from macros """

# Startup
logger = Logger.getLogger('init_xy_plot')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()


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
    except:
        return False
    return PVUtil.getVType(PV).getValue()

# Main
max_traces = 4
macros = get_macros(display)

uut = macros.UUT
site = int(macros.SITE)
nsites = int(macros.NSITES)
chans = list_of_channels(macros.pchans)
chanmap = {site: chans}
pvbase = "=elementAt({UUT}:0:SLOWMON:MEAN, {chan})"

"""
site = 0-6  : Map channels to specific site
site = -1   : Map channels to uut
"""

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
    print(site)
    macros.site = site
    for chan in chanmap[site]:
        if current >= max_traces: break
        macros.chan = chan
        trace_pv = pvbase.format(**macros)
        print(current, trace_pv)
        widget.setPropertyValue("traces[{}].name".format(current), trace_pv)
        widget.setPropertyValue("traces[{}].y_pv".format(current), trace_pv)
        current += 1

