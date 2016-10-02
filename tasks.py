#! /usr/bin/env python
from invoke import task, Collection
from yapsy.PluginManager import PluginManager
import os

from glob import glob

import logging
import coloredlogs
coloredlogs.install()
logging.basicConfig(level=logging.INFO)

# some needed variables
workdir = os.path.dirname(__file__)


@task
def get(ctx):
    ctx.run("terraform get")


@task
def plan(ctx):
    ctx.run("terraform plan")


@task(help={'modulepath': "Path to modules (.terraform/modules)"})
def data(ctx, modulepath=".terraform/modules"):
    """Run all module's collect_data() plugin methods"""
    # TODO this may not be the proper path
    places = glob(os.path.join(workdir, modulepath, "*/plugins"))
    manager = PluginManager(directories_list=places)
    manager.collectPlugins()

    for plugin in manager.getAllPlugins():
        # TODO Use plugin categories or check for method existence before
        # calling the methods
        logging.info("Running %s.collect_data(): (from %s)",
                     plugin.name, plugin.path)
        plugin.plugin_object.collect_data()
        # TODO "Change detection" should be in a plugin method, modules may not
        # always be git repos.
        tf_modulepath = os.path.abspath(os.path.join(plugin.path, "../.."))
        tf_module_basename = os.path.abspath(os.path.realpath(tf_modulepath))
        args = [
            "git -C",
            tf_modulepath,
            "diff --quiet --ignore-submodules --"
        ]
        runresult = ctx.run(" ".join(args), echo=False, warn=True)
        if runresult.exited == 1:
            logging.warning("There are uncommited changes in Module %s",
                            tf_module_basename)


@task(help={'modulepath': "Path to modules (.terraform/modules)"})
def requirements(ctx, modulepath=".terraform/modules"):
    """Install all recursive python requirements"""
    requirements = glob(os.path.join(
        workdir,
        modulepath, "*/requirements.txt"))
    for reqTxt in requirements:
        ctx.run(" ".join([
            "pip install -r",
            reqTxt
        ]))


# The default task namespace
ns = Collection()
ns.add_task(get)
ns.add_task(plan)
ns.add_task(data)
py = Collection("py")
py.add_task(requirements, 'requirements')
ns.add_collection(py)
