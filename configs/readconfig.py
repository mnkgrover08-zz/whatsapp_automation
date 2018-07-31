import os, sys
import ConfigParser

ENV_CONFIG = {
    'dev': 'dev',
    'prod': 'prod',
    'staging': 'staging'
}

#ENV = os.getenv('ENV', 'prod')

ENV=os.environ["ENV"]

print ENV

def load_env_configuration(env):
    if not env:
        print('Please define the ENV')
        sys.exit(1)
    config = ConfigParser.RawConfigParser()
    config.read((os.path.join(os.getcwd(), 'configs/%s.cfg' % ENV_CONFIG[env])))
    return config

global configp

configp = load_env_configuration(ENV)