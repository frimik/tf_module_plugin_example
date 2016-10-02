#! /usr/bin/env python
from invoke import task
from yapsy.PluginManager import PluginManager
import os

import logging
logging.basicConfig(level=logging.INFO)


@task(default=True)
def collect_data(ctx):
    places = [os.path.join(os.path.dirname(__file__), "plugins")]
    manager = PluginManager(directories_list=places)
    manager.collectPlugins()

    for plugin in manager.getAllPlugins():
        logging.info("Running %s.collect_data: (from %s)",
                     plugin.name, plugin.path)
        plugin.plugin_object.collect_data()
