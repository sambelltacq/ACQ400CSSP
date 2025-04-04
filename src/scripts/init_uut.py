import time
from java.util.logging import Logger
from org.phoebus.framework.macros import Macros
from org.csstudio.display.builder.runtime.script import PVUtil

""" Init uut  """

# Startup
t0 = time.time()
logger = Logger.getLogger('init_uut')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()
timeout = 2 * 1000

# Functions
class DotDict(dict):
    __delattr__ = dict.__delitem__
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__

def get_macros(widget):
    macros = widget.getEffectiveMacros()
    return DotDict({key: macros.getValue(key) for key in macros.names})

def set_macros(widget, macros):
    new_macros = Macros()
    for key in macros:
        new_macros.add(key, str(macros[key]))
    widget.setPropertyValue("macros", new_macros)

def read_pv(pvname):
    try: PV = PVUtil.createPV(pvname, timeout)
    except: return False
    return PVUtil.getVType(PV).getValue()

def get_model(uutname):
    try:
        uut_model = read_pv("{}:0:MODEL".format(uutname))
        if uut_model:
            for model in model_def:
                if uut_model.startswith(model):
                    return model
    except: pass
    return None

model_def = {
    'acq1001': {
        'sites': 1,
    },
    'acq1002': {
        'sites': 2,
    },
    'acq1102': {
        'sites': 2,
    },
    'acq2106': {
        'sites': 6,
    },
    'acq2206': {
        'sites': 6,
    },
    'z7io'   : {
        'sites': 2,
    },
}


# Main
def main():
    macros = get_macros(widget)
    uutname = macros.UUT
    if uutname == "none": return
    logger.info("Init {}".format(uutname))

    model = get_model(macros.UUT)

    sites = {}
    if model:
        macros.MODEL = get_model(macros.UUT)
        sitelist = read_pv("{}:SITELIST".format(macros.UUT))
        sites = {int(k): v for k, v in (site.split('=') for site in sitelist.split(',', 1)[1].split(','))}
        site_str = ','.join(map(str, sites.keys()))
        #PVUtil.writePV('loc://SITES', site_str, timeout) # Unneeded?
        macros.SITES = site_str

    for site in range(1, 6 + 1):
        site_key = "SITE_{}_MODEL".format(site)
        site_model = "none"
        if site in sites:
            site_model = read_pv("{}:{}:PART_NUM".format(macros.UUT, site))
        macros[site_key] = site_model

    set_macros(widget, macros)
    widget.setPropertyValue("file", "")
    widget.setPropertyValue("file", macros.FILE)

main()