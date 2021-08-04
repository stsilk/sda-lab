from jinja2 import Template, Environment, FileSystemLoader
import yaml

yml = {}
with open("Variables/Fusion-Router.yml") as f:
    try:
        yml = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        print(exc)
environment = Environment(loader=FileSystemLoader("Templates/"))
template = environment.get_template("Fusion-Router.j2")
with open("Configs/fusion-router.cfg", 'w+') as f:
    f.write(template.render(yml).replace('\n\n', '\n'))


