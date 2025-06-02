#!/usr/bin/env python3

import argparse
import os
import platform
import glob
import re
import logging
from subprocess import run, Popen, DEVNULL

"""Starts ACQ400CSSP"""
logging.basicConfig(level=logging.INFO)

def init_globals(args):
    if not args.uuts:
        print("[ACQ400CSSP]")
        args.uuts = input("Enter UUT hostnames: ").split()

    if not isinstance(args.uuts, list): args.uuts = [args.uuts]

    ID=             gen_ID(args)
    ROOT_DIR=       os.path.dirname(os.path.abspath(__file__))
    OS_NAME=        platform.system().lower()
    ENV=            os.environ.copy()

    WORKSPACE=      f"{ROOT_DIR}/workspaces/{ID}"
    JAVA_BIN=       None #"java"
    PHOEBUS_JAR=    None #f"{ROOT_DIR}/product-4.7.3/product-4.7.3.jar"
    CSSP_CONF=      f"{ROOT_DIR}/CSSP.conf"

    SETTINGS_BASE=  f"{ROOT_DIR}/src/settings_base.ini"
    WORKSPACE=      f"{ROOT_DIR}/workspaces/{ID}"
    LOGGING=        f"{ROOT_DIR}/src/logging.properties"
    SETTINGS=       f"{WORKSPACE}/settings.ini"
    MEMENTO=        f"{WORKSPACE}/memento"
    LAUNCHER=       f"{ROOT_DIR}/src/acq400_launcher.bob"
    LAUNCHER_MULTI= f"{ROOT_DIR}/src/acq400_launcher_multi.bob"

    PREFS=          f"{ROOT_DIR}/workspace.prefs"
    UUT_PREFS=      f"{ROOT_DIR}/{ID}_workspace.prefs"

    JAVA_ARGS=      f"-Dphoebus.user={WORKSPACE} -Dphoebus.folder.name.preference= "
    TARGET=         ""

    if args.debug: logging.getLogger().setLevel(logging.DEBUG)
    globals().update(locals())

def run_main(args):
    init_globals(args)
    globals().update(read_conf())
    check_system()

    init_memento(args)
    update_pref()
    
    CMD = os.path.normpath(f'"{JAVA_BIN}" {JAVA_ARGS} -jar {PHOEBUS_JAR} -settings {SETTINGS} -logging {LOGGING} {TARGET}')

    if args.debug:
        run(CMD, shell=True, env=ENV, text=True)
        print('END')
        print("CMD", CMD)
        #print(globals())
        input()
        return

    Popen(CMD, shell=True, stdout=DEVNULL, stderr=DEVNULL, start_new_session=True, env=ENV)

def read_conf():
    conf = {}
    if os.path.exists(CSSP_CONF):
        with open(CSSP_CONF, 'r') as fp:
            for line in fp.readlines():
                try:
                    key, value = line.split('=', maxsplit=1)
                    logging.debug(f"CSSP.conf got {key}={repr(value)}")
                    conf[key.strip()] = value.strip()
                except: pass
    return conf

def write_conf(key, value):
    conf = read_conf()
    conf[key] = value
    with open(CSSP_CONF, 'w+') as fp:
        for key, value in conf.items():
            fp.write(f"{key}={value}\n")


def check_system():
    global JAVA_BIN, PHOEBUS_JAR

    if not JAVA_BIN:
        JAVA_BIN = locate_java_bin()
        write_conf("JAVA_BIN", JAVA_BIN)
    
    if not PHOEBUS_JAR: 
        PHOEBUS_JAR = locate_phoebus()
        write_conf("PHOEBUS_JAR", PHOEBUS_JAR)

    print(f"JAVA_BIN = {JAVA_BIN}")
    print(f"PHOEBUS_JAR = {PHOEBUS_JAR}")

def locate_java_bin():
    """Finds the Java bin with the correct version"""
    cmd = {'windows': 'where', 'linux': 'whereis'}
    separator = {'windows': '\n', 'linux': ' '}
    java_bin = "java"
    if check_version(java_bin): return java_bin
    response, code = run_cmd(f"{cmd[OS_NAME]} java")
    for java_bin in response.split(separator[OS_NAME]):
        if check_version(java_bin): return java_bin
    logging.critical('Cannot find valid java version set manually in CSSP.conf')
    exit(1)

def check_version(path, min_version=17):
    """Checks java bin version"""
    cmd = f'"{path}" --version'
    logging.debug(f"Checking java {path}")
    response, code = run_cmd(cmd)
    if code != 0: return False
    match = re.search(r'(\d+)\.([\db_-]*)\.([\db_-]*)', response)
    logging.debug(f"version {match.group(0)}")
    if int(match.group(1)) >= min_version: return True
    return False

def locate_phoebus():
    global PHOEBUS_JAR
    if PHOEBUS_JAR and os.path.exists(PHOEBUS_JAR): return PHOEBUS_JAR
    search_glob = os.path.join(ROOT_DIR, 'p*', 'p*.jar')
    matches = glob.glob(search_glob)
    if len(matches) != 0:
        PHOEBUS_JAR = matches[0]
        return PHOEBUS_JAR
    logging.critical('Cannot find phoebus jar set manually in CSSP.conf')
    exit(1)

def gen_ID(args):
    uuts = sorted(args.uuts)
    prefix = '' if len(uuts) == 1 else 'multi_'
    uuts = '_'.join(uuts)
    return f"{prefix}{uuts}"

def init_memento(args):
    global MEMENTO, WORKSPACE, JAVA_ARGS, TARGET, SETTINGS
    if os.path.exists(MEMENTO):
        print(f"Using existing workspace {WORKSPACE}")
        TARGET = f"-layout {MEMENTO}"
        return
    new_lines = []
    macros_pref = "org.csstudio.display.builder.model/macros={macros}\n"
    new_lines.append(macros_pref.format(macros=gen_macros_pref(args.uuts, args.debug)))
    if len(args.uuts) > 1: new_lines.append("org.phoebus.ui/home_display=src/acq400_launcher_multi.bob")
    print(f"Creating new workspace {WORKSPACE}")
    os.makedirs(WORKSPACE, exist_ok=True)
    with open(SETTINGS_BASE, 'r') as base_fp:
        with open(SETTINGS, 'w') as new_fp:
            lines = base_fp.readlines()
            lines.extend(new_lines)
            new_fp.writelines(lines)
    resource = LAUNCHER
    if len(args.uuts) > 1: resource = LAUNCHER_MULTI
    TARGET=f"-resource {resource} -layout null"
    
def gen_macros_pref(uuts, debug):
    macros="<UUT>{uut}</UUT>".format(uut=uuts[0])
    if len(uuts) > 1:
        macros=""
        for idx, uut in enumerate(uuts):
            idx += 1
            macros += f"<UUT{idx}>{uut}</UUT{idx}>"
    macros += f"<DEBUG>{debug}</DEBUG>"
    return macros

def update_pref():
    global PREFS, UUT_PREFS, SETTINGS
    """Updates the phoebus preference ini"""

    if os.path.exists(UUT_PREFS): pref_file = UUT_PREFS
    elif os.path.exists(PREFS): pref_file = PREFS
    else: return
    
    with open(pref_file) as f:
        prefs = {pref.split('=')[0]: pref.split('=')[1] for pref in f.readlines() if pref.find('=') != -1}

    with open(SETTINGS, 'r+') as fp:
        lines = fp.readlines()
        changed_lines = 0
        for idx, line in enumerate(lines):
            for pref, value in prefs.copy().items():
                if line.startswith(pref):
                    new_line = f"{pref}={value}"
                    del prefs[pref]
                    if line != new_line:
                        lines[idx] = new_line
                        changed_lines += 1

        for pref, value in prefs.items():
            new_line = f"{pref}={value}"
            lines.append(new_line)
            changed_lines += 1

        if changed_lines > 0:
            fp.seek(0)
            fp.writelines(lines)
            fp.truncate()

def run_cmd(cmd):
    result = run(cmd, shell=True, capture_output=True, text=True)
    response = result.stdout if result.stdout else result.stderr
    return response, result.returncode

def get_parser():
    parser = argparse.ArgumentParser(description='Start script for ACQ400CSSP')
    parser.add_argument('--debug', action='store_true', help="enable debug")
    parser.add_argument('uuts', nargs='*', help="uut hostnames")
    return parser

if __name__ == '__main__':
    run_main(get_parser().parse_args())
