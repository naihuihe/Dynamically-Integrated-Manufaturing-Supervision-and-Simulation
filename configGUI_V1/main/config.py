import os, inspect, sys
from configGUI_V1 import PROJECT_BASE_DIR

def import_modules(pkg_dir):

    pkg_full_dir = os.path.join(PROJECT_BASE_DIR, os.path.relpath(pkg_dir))
    pkg_path = pkg_dir if os.sep not in os.path.relpath(pkg_dir) else os.path.relpath(pkg_dir).replace(os.sep, '.')

    for dir in os.listdir(pkg_full_dir):
        if '_' not in dir:
            module_path = pkg_path + '.'+ inspect.getmodulename(dir)
            __import__(module_path)

def get_agent_mapper(pkg_dir):
    '''
    :param pkg_dir: the full directory path of the package relative to the project base folder (not include base folder name)
    :return: dict {agent.__class__.__name__, agent obj}
    '''
    pkg_full_dir = os.path.join(PROJECT_BASE_DIR, os.path.relpath(pkg_dir))
    pkg_path = pkg_dir if os.sep not in os.path.relpath(pkg_dir) else os.path.relpath(pkg_dir).replace(os.sep, '.')

    mapper = {}
    for dir in os.listdir(pkg_full_dir):
        if '_' not in dir:
            module_path = pkg_path + '.'+ inspect.getmodulename(dir)
            __import__(module_path)
            is_class_member = lambda member: inspect.isclass(member) and member.__module__ == module_path and not inspect.isabstract(member)
            for name, obj in inspect.getmembers(sys.modules[module_path], is_class_member):
                mapper[name] = obj

    return mapper

AGENT_MAPPER = get_agent_mapper('agent_models')
BITMAP = PROJECT_BASE_DIR + os.sep + 'figs' + os.sep+ 'Corot.ico'



if __name__=='__main__':
    get_agent_mapper('agent_models')
