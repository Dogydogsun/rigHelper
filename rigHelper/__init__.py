import importlib
import fnmatch
import os

dirname = os.path.dirname(__file__)

packagePathRaw = os.path.dirname(dirname)
packagePath = packagePathRaw.replace("\\", "/")

#Reload scripts by recursively looking through package path. Code courtesy of Greg Hendrix, found at: https://www.tdhendrix.com/blog/reload-python-files-in-maya

def list_files_with_extension(path, file_extension):
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, '*{}'.format(file_extension)):
            yield os.path.join(root, filename)


def reload_python_files():
    python_files = list_files_with_extension(packagePath, '.py')
    python_files = [py_file.replace('\\', '/') for py_file in python_files]

    exclude_packages = ['sandbox', 'third_party']
    exclude_paths = [os.path.join(packagePath, package) for package in exclude_packages]
    exclude_paths = [path.replace('\\', '/') for path in exclude_paths]

    for py_file in python_files:
        if '__init__.py' in py_file or any(x in py_file for x in exclude_paths):
            continue

        package = py_file.split('/')[-2]
        if 'Scripts' in package:
            continue

        script = py_file.split('/')[-1].split('.')[0]
        package_full_path = '.'.join(py_file.split(packagePath)[1][1:].split('/')[:-1])

        module = importlib.import_module('{}.{}'.format(package_full_path, script), package=None)
        importlib.reload(module)
        print("Reloaded '{}'".format(py_file))


reload_python_files()

import rigHelper.rigHelperUI

rigHelper.rigHelperUI.RigHelperUI()
