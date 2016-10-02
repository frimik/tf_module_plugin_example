# tf_module_plugin_example
Terraform module plugin concept for external data integration

## Usage

```
mkvirtualenv tf  # or regular virtualenv, have it your way
pip install -r requirements.txt
invoke py.requirements --modulepath=modules
invoke data --modulepath=modules
```

## Real-life usage

If you have created or are using modules which uses the plugin concept:

```
mkvirtualenv tf
pip install -r requirements.txt
terraform get
invoke py.requirements
invoke data
terraform plan
```

## Concept explained

* Each module provides a plugin method: `collect_data()`.
* For each downloaded module, go through all found plugins and call `collect_data()`. Currently, method allows no input.
* Plugin method is responsible for *populating*/*updating* the variables in the Terraform module.
* Each module gets checked for diffs and notifies operator if data differs (git diff is hardcoded right now).

## TODO

* Maintain configuration in yaml or json in your "master" Terraform files which map input data => plugins - make `collect_data()` take arguments?
