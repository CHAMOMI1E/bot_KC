from jinja2 import Environment, FileSystemLoader

template_env = Environment(loader=FileSystemLoader('app/templates'), autoescape=True)
