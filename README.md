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
