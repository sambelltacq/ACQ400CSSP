import time
from java.util.logging import Logger
from  org.csstudio.display.builder.model.properties import WidgetColor

from org.csstudio.display.builder.runtime.script import ScriptUtil

""" Init XY Plot from macros """

# Startup
logger = Logger.getLogger('init_xy_plot')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()

# Functions
def list_of_channels(chanstr):
    chans = []
    for chan in chanstr.split(','):
        if '-' in chan:
            chan = list(map(int, chan.split('-')))
            chans.extend(list(range(chan[0], chan[1] + 1)))
            continue
        chans.append(int(chan))
    return chans

# Main
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

max_traces = 8
timestamp = int(time.time())

uut = widget.getEffectiveMacros().getValue('UUT')
site = widget.getEffectiveMacros().getValue('SITE')
chx = widget.getEffectiveMacros().getValue('chx')
mode = widget.getEffectiveMacros().getValue('mode')
dtype = widget.getEffectiveMacros().getValue('dtype')

#widget.propTitle().setValue("{}:{} CH{} {} {}".format(uut, site, chx, mode, dtype))

modes = {
    'LIVE': 'WF',
    'POST': 'TW',
}

dtypes = {
    'RAW': '',
    'VOLTS': ':V.VALA',
}

chans = list_of_channels(chx)

trace_pv_fmt = "{uut}:{site}:AI:{mode}:{chan:02d}{dtype}"
env = {
    'uut': uut,
    'site': site,
    'dtype': dtypes.get(dtype,''),
    'mode': modes.get(mode, 'WF'),
}

for trace_idx, chan in enumerate(chans):
    if trace_idx >= max_traces: break
    env['chan'] = chan
    trace_pv = trace_pv_fmt.format(**env)
    logger.info("CH{} Trace Pv {}".format(chan, trace_pv))
    widget.setPropertyValue("traces[{}].color".format(trace_idx), WidgetColor(*colors[trace_idx]))
    widget.setPropertyValue("traces[{}].name".format(trace_idx), trace_pv)
    widget.setPropertyValue("traces[{}].y_pv".format(trace_idx), trace_pv)

widget.setPropertyValue("y_axes[0].title", 'Volts (V)' if dtype == 'VOLTS' else 'Codes')