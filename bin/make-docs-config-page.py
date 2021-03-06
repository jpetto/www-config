#!/usr/bin/env python

from envcat import get_env_vars


APPS = [
    'bedrock-dev',
    'bedrock-stage',
    'bedrock-prod',
]
_BOOLEANS = {'1': True, 'yes': True, 'true': True, 'on': True,
             '0': False, 'no': False, 'false': False, 'off': False}


def cast_boolean(value):
    """
    Helper to convert config values to boolean as ConfigParser do.
    """
    value = str(value)
    if value.lower() not in _BOOLEANS:
        raise ValueError('Not a boolean: %s' % value)

    return _BOOLEANS[value.lower()]


def get_vars_for_app(app_name):
    return get_env_vars('configs/{}.env'.format(app_name))


def vars_to_md(app_name):
    envvars = get_vars_for_app(app_name)
    lines = []
    for key, value in sorted(envvars.items()):
        output = '{key}\n: {value}\n'.format(key=key, value=value)
        try:
            if cast_boolean(value):
                output += '{: .bool-true}\n'
            else:
                output += '{: .bool-false}\n'
        except ValueError:
            pass
        lines.append(output)
    return '\n'.join(lines)


def app_section(app_name):
    output = '\n## {}\n\n'.format(app_name)
    output += vars_to_md(app_name)
    return output


def main():
    print('# Current Configurations')
    for app_name in APPS:
        print(app_section(app_name))


if __name__ == '__main__':
    main()
