#!/usr/bin/env python
"""
    data_schema_validate
    ~~~~~~~~~~~~~~~~~~~~

    blah blah blah
"""

import sys
import glob
import yaml
import pyrx

config_schema_yml = """
type: //rec
required:
  validate:
    type: //arr
    contents:
      type: //rec
      required:
        name: //str
        schema: //str
        data: //str
"""

rx = pyrx.Factory({"register_core_types": True})


def load(f):
    config = yaml.load(f.read())
    # meta-check (sanity)
    if not check(config_schema_yml, [config]):
        print "Invalid config schema  :("
        sys.exit(1)

    for test in config['validate']:
        with open(test['schema']) as f:
            schema = f.read()
            data_files = glob.glob(test['data'])
            opened = (open(d).read() for d in data_files)
            data = (yaml.load(d) for d in opened)
            yield (schema, data)


def check(schema, data):
    schema = rx.make_schema(yaml.load(schema))
    return all(schema.check(datum) for datum in data)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Validate Data blah blah")
    parser.add_argument('config', type=argparse.FileType('r'), metavar='config')
    args = parser.parse_args()
    if not all(check(schema, data) for schema, data in load(args.config)):
        print "Tests failed  :("
        sys.exit(1)
    print "Tests passed  :)"
