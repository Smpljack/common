# -*- encoding: utf-8 -*-
import os
import yaml
import jinja2

def render_page(env, template, filename, parameters):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(filename, "w") as output_file:
        output_file.write(env.get_template(template).render(**parameters))

def _main():
    import sys
    import narval_ii.metadata as metadata
    basepath = os.path.abspath(os.path.dirname(__file__))
    template_folder = os.path.join(basepath, "templates")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_folder))
    out_folder = sys.argv[1]
    print("generating to:", out_folder)
    render_page(env,
                "flights.html",
                os.path.join(out_folder, "flights.html"),
                {"flights": metadata.load_flights()})

if __name__ == '__main__':
    _main()
