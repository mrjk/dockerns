import os
import sys
import re
import json
import yaml
from functools import reduce
from datetime import datetime

QUIET = False
PROCESS = "dockerdns"


def log(msg, *args):
    global QUIET
    if not QUIET:
        now = datetime.now().isoformat()
        line = "%s [%s] %s\n" % (now, PROCESS, msg % args)
        sys.stderr.write(line)
        sys.stderr.flush()


def get(d, *keys):
    empty = {}
    return reduce(lambda d, k: d.get(k, empty), keys, d) or None


def splitrecord(rec):
    m = re.match(
        "([a-zA-Z0-9_-]*|\*):((?:[12]?[0-9]{1,2}\.){3}(?:[12]?[0-9]{1,2}){1}$)", rec
    )
    if not m:
        log("--record has invalid format, expects: `--record <host>:<ip>`")
        sys.exit(1)
    else:
        return (m.group(1), m.group(2))


def contains(txt, *subs):
    return any(s in txt for s in subs)


# TODO: add tests
def from_yaml(string):
    "Transform YAML string to python dict"
    return yaml.safe_load(string)


# TODO: add tests
def to_yaml(obj, headers=False):
    "Transform obj to YAML"
    return yaml.safe_dump(obj)


# TODO: add tests
def to_json(obj, nice=True):
    "Transform JSON string to python dict"
    if nice:
        return json.dumps(obj, indent=2)
    return json.dumps(obj)


# TODO: add tests
def from_json(string):
    "Transform JSON string to python dict"
    return json.loads(string)


# TODO: add tests
def to_dict(obj):
    """Transform JSON obj/string to python dict

    Useful to transofmr nested dicts as well"""
    if not isinstance(obj, str):
        obj = json.dumps(obj)
    return json.loads(obj)


def read_file(file):
    "Read file content"
    with open(file, encoding="utf-8") as _file:
        return "".join(_file.readlines())


def write_file(file, content):
    "Write content to file"

    file_folder = os.path.dirname(file)
    if not os.path.exists(file_folder):
        os.makedirs(file_folder)

    with open(file, "w", encoding="utf-8") as _file:
        _file.write(content)
