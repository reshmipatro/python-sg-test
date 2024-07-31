from jinja2 import Environment, select_autoescape
templateLoader = jinja2.FileSystemLoader( searchpath="/" )
something = ''

# sonarsource snippets
# ruleid:environment-autoescape-disabled
env = Environment() # Sensitive: New Jinja2 Environment has autoescape set to false
# ruleid:environment-autoescape-disabled
env = Environment(autoescape=False) # Sensitive:
# ok:environment-autoescape-disabled
env = Environment(autoescape=True) # Compliant
######################

def __init__(self) -> None:
    self.env = Environment(
        loader=PackageLoader('cephadm', 'templates'),
        # ok:environment-autoescape-disabled
        autoescape=select_autoescape(['html', 'xml'], default_for_string=False),
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined
    )
# ok:environment-autoescape-disabled
Environment(loader=templateLoader, load=templateLoader, autoescape=True)

# ruleid:environment-autoescape-disabled
Environment(loader=templateLoader, load=templateLoader)

# ok:environment-autoescape-disabled
templateEnv = jinja2.Environment(autoescape=True,
        loader=templateLoader )

# ruleid:environment-autoescape-disabled
Environment(loader=templateLoader, load=templateLoader, autoescape=something)

# ruleid:environment-autoescape-disabled
templateEnv = jinja2.Environment(autoescape=False, loader=templateLoader )

Environment(loader=templateLoader,
            load=templateLoader,
            # ruleid:environment-autoescape-disabled
            autoescape=False)

# ok:environment-autoescape-disabled
Environment(loader=templateLoader, autoescape=select_autoescape())

Environment(loader=templateLoader,
# ok:environment-autoescape-disabled
            autoescape=select_autoescape(['html', 'htm', 'xml']))

def fake_func():
    return 'foobar'

# ruleid:environment-autoescape-disabled
Environment(loader=templateLoader, autoescape=fake_func())
