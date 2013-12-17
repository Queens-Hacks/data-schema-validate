#!/usr/bin/env python
"""
    data_schema_validate
    ~~~~~~~~~~~~~~~~~~~~

    blah blah blah
"""

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


class ConfigError(ValueError):
    """An invalid configuration was provided"""
    def __init__(self, trace):
        self.trace = trace

    def __str__(self):
        return '\n'.join(self.trace[:-1])


def check_config(config):
    config_schema = yaml.load(config_schema_yml)
    schema = rx.make_schema(config_schema, trace=True)
    if not schema.check(config):
        return schema.trace


def load_data_files(filepathdef):
    file_list = glob.glob(filepathdef)
    for filename in file_list:
        with open(filename) as data_file:
            data = yaml.load(data_file)
        yield filename, data


def validate(config):
    config_trace = check_config(config)
    if config_trace is not None:
        raise ConfigError(config_trace)

    errors = 0

    for test in config['validate']:
        print('Validating data for {} against {}'.format(
              test['name'], test['schema']))

        with open(test['schema']) as schema_file:
            schema_def = yaml.load(schema_file)
        schema = rx.make_schema(schema_def, trace=True)

        for filename, data in load_data_files(test['data']):
            print('  - testing {}'.format(filename))
            if not schema.check(data):
                trace = schema.trace[:4]
                print('   x  {}'.format(
                      '\n   x  '.join(trace)))
                errors += 1

    return errors


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Validate data with schemas')
    parser.add_argument('config', metavar='config',
                        type=argparse.FileType('r'))
    args = parser.parse_args()
    config = yaml.load(args.config)

    try:
        errors = validate(config)
    except ConfigError:
        raise SystemExit('ERROR: invalid configuration')

    if errors > 0:
        raise SystemExit('FAILED (errors={})'.format(errors))

    print('\nTests passed  :)')
