import time
from java.util.logging import Logger
from org.phoebus.framework.macros import Macros
from org.csstudio.display.builder.runtime.script import PVUtil

""" Init macros and local pvs """

# Startup
t0 = time.time()
logger = Logger.getLogger('init_main')
widget = locals()['widget']
pvs = locals()['pvs']
display = widget.getTopDisplayModel()
timeout = 1

# Functions
def get_pv_value(pvname):
    timeout = 1000
    try: PV = PVUtil.createPV(pvname, timeout)
    except:
        return False
    return PVUtil.getVType(PV).getValue()

def get_model(uutname):
    uut_model = get_pv_value("{}:0:MODEL".format(uutname))
    if uut_model:
        for model in model_def:
            if uut_model.startswith(model):
                return model
    return None

def set_local(pvname, value, pv=True):
    display.getEffectiveMacros().add(pvname, str(value))
    if pv:
        PVUtil.writePV('loc://{}'.format(pvname), str(value), timeout)

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
logger.info("Start")
uutname = PVUtil.getString(pvs[0]).lower()
model = get_model(uutname)

if model:
    time.sleep(0.1)
    set_local('UUT', uutname, pv=False)
    set_local('MODEL', model)

    nsites = model_def[model]['sites']
    set_local('NSITES', nsites)

    sites = {}
    sitelist = get_pv_value("{}:SITELIST".format(uutname))

    if sitelist:
        sites = {int(k): v for k, v in (site.split('=') for site in sitelist.split(',', 1)[1].split(','))}
        set_local('SITES', ','.join(map(str, sites.keys())))

    for site in range(1, 6 + 1):
        pvname = "SITE_{}_MODEL".format(site)
        value = "none"
        if site in sites:
            value = sites[site]
        display.getEffectiveMacros().add(pvname, str(value))

logger.info("Complete {:0.2f}s".format(time.time() - t0))
