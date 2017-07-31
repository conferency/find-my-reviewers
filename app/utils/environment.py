import os


def load_env(filename):
    env_dict = {}
    if os.path.exists(filename):
        for line in open(filename):
            var = line.strip().split('=')
            if len(var) == 2:
                env_dict[var[0]] = var[1]
        print('Imported configuration in ' + filename)
    return env_dict