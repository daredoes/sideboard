from __future__ import unicode_literals
import sys
import importlib
from glob import glob
from os.path import join, isdir, basename

from sideboard.config import config

plugins = {}

def _discover_plugins():
    ordered = list(reversed(config['priority_plugins']))
    print("priority_plugins: " + str(ordered))
    plugin_dirs = [d for d in glob(join(config['plugins_dir'], '*')) if isdir(d) and not basename(d).startswith('_')]

    # glob() results are not ordered, so we sort here to ensure consistency on multiple platforms
    plugin_dirs = sorted(plugin_dirs, key=lambda d: basename(d))

    print("plugin_dirs: " + str(plugin_dirs))
    sorted_plugin_ordering = sorted(plugin_dirs, reverse=True, key=lambda d: (ordered.index(basename(d)) if basename(d) in ordered else -1))

    sorted_plugin_names = [basename(p) for p in sorted_plugin_ordering]
    print("would load plugins in the following order:" + str(sorted_plugin_names))

    for plugin_path in sorted_plugin_ordering:
        sys.path.append(plugin_path)
        plugin_name = basename(plugin_path).replace('-', '_')
        print("LOADING PLUGIN: " + plugin_name)
        plugins[plugin_name] = importlib.import_module(plugin_name)
