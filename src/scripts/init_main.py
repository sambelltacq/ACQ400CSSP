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

# Functions
def get_macros(widget):
	macros = widget.getPropertyValue("macros")
	extracted = {}
	for key in macros.getNames():
		extracted[key] = macros.getValue(key)
	return extracted

def set_macros(widget, new_macros):
    macros = Macros()
    for key in new_macros:
        macros.add(key, str(new_macros[key]))
    widget.setPropertyValue("macros", macros)
    return macros

def get_pv_value(pvname):
    timeout = 1000
    try: PV = PVUtil.createPV(pvname, timeout)
    except:
        return False
    return PVUtil.getVType(PV).getValue()

def create_string_pv(name, value):
    timeout = 2
    dtype="VString"
    pvname = 'loc://{}<{}>("")'.format(name, dtype)
    pv = PVUtil.createPV(pvname, timeout)
    pv.write(value)
    logger.info("Create {} {}".format(pvname, value))
    return pv

def create_long_pv(name, value):
    timeout = 2
    dtype="VLong"
    pvname = 'loc://{}<{}>(0)'.format(name, dtype)
    pv = PVUtil.createPV(pvname, timeout)
    pv.write(value)
    logger.info("Create {} {}".format(pvname, value))
    return pv

def get_model(uutname):
    for model in models:
        if uutname.startswith(model):
            return model
    return None

models = {
    'acq1001': {
        'sites': 1,
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

#pv0 + 1 >= $(NUM)

# Main
logger.info("Start")
uutname = PVUtil.getString(pvs[0]).lower()
model = get_model(uutname)

if model:
    macros = get_macros(display)
    macros['UUT'] = uutname
    
    macros['MODEL'] = model
    create_string_pv('MODEL', model)

    nsites = models[model]['sites']
    macros['NSITES'] = nsites
    create_long_pv('NSITES', nsites)

    sites = {}
    sitelist = get_pv_value("{}:SITELIST".format(uutname))

    if sitelist:
        _, sites = sitelist.split(',', 1)
        sites = {int(k): v for k, v in (site.split('=') for site in sites.split(','))}

    for site in range(1, nsites + 1):
        sitemacro = "SITE_{}".format(site)
        sitemodel = sites[site] if site in sites else None
        macros[sitemacro] = sitemodel
    
    print(macros)
    set_macros(widget, macros)

logger.info("Complete {:0.2f}s".format(time.time() - t0))