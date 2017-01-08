from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('mypkg', 'templates'))
template = env.get_template('base.html')
print template.render({'title':'fuck'})