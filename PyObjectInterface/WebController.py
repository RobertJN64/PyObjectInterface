from PyObjectInterface import PyObjectInterface
from os import path
import traceback
import flask

def generate_html(poi: PyObjectInterface, font_size=2.5):
    """
    Generate HTML for the control page of a PyObjectInterface
    :param poi: PyObjectInterface
    :param font_size: font_size of largest header
    """
    buttons = ""
    for method_name, func_desc in poi.method_dict.items():
        if func_desc.builtin_err:
            buttons += f"<p>{method_name} is a builtin method and can't be accessed from WebController</p>"

        else:
            stack = poi.base_obj_name + '.' + method_name
            onclick = f'call_method("{stack}")'
            buttons += f"<button class='nice_button' onclick={onclick}>{method_name}</button>"
            for arg_name, default in zip(func_desc.args, func_desc.defaults):
                className = 'py_' + stack
                elemID = className + '|' + arg_name
                buttons += f"<span class='input_label'>{arg_name}</span>"
                if len(default) > 0 and default[0] == "'":
                    default = '"' + default[1:-1] + '"'
                buttons += f"<input id='{elemID}' class='{className}' value='{default}'>"
            if func_desc.desc is not None:
                desc = str(func_desc.desc).strip().replace('\n','<br>')
                buttons += f"<p>{desc}</p>"
        buttons += "<br>"

    attr_table = ""
    if len(poi.attribute_list) > 0:
        attr_table += "<br><table><thead><tr><th>Attribute</th><th>Value</th></thead><body>"
        for attr_name in poi.attribute_list:
            elemID = 'py_' + poi.base_obj_name + "." + attr_name
            attr_table += f"<tr><td>{attr_name}</td><td id='{elemID}'>Waiting for update...</td>"
        attr_table += "</body></table>"

    subcontent = ""
    for subobj_poi in poi.subobj_dict.values():
        subcontent += generate_html(subobj_poi, max(font_size - 0.5, 1)) + '\n'

    return (f"""
    <details open>
        <summary style="font-size: {font_size}em">{poi.base_obj_name}</summary>
        {buttons}
        {attr_table}
        {subcontent}
    </details>
    """)

def smart_arg_parse(x):
    if x == 'None':
        return None
    if x[0] == '"' or x[0] == "'":
        return x[1:-1] #strip trailing and leading quotes
    if '.' in x:
        return float(x)
    return int(x)

def create_WebController(obj, name, flask_app, recursion_depth = 5, create_private_interface=True):
    with open(path.dirname(__file__) + '/web_controller.tpl.html') as f:
        tpl = f.read()

    def _create_webroutes(poi, baseurl):
        content = generate_html(poi)

        @flask_app.route(baseurl, endpoint=baseurl + '_baseview')
        def py_control():
            return tpl.replace('{{ content }}', content)

        @flask_app.route(baseurl + '/call_method/<stack>', endpoint=baseurl + '_call_method')
        def call_method(stack):
            kwargs = {argname: smart_arg_parse(arg) for argname, arg in flask.request.args.items()}

            try:
                retval = poi.call_method(stack, kwargs)
                if retval is None:
                    return ''
                else:
                    return str(retval)
            except (Exception,):
                traces = traceback.format_exc().split('\n')
                for i in range(6):
                    traces.pop(1) #remove the webcontroller call from the trace
                trace = '\n'.join(traces)
                return "Internal Error:\n" + trace


        @flask_app.route(baseurl + '/get_attributes', endpoint=baseurl + '_get_attributes')
        def get_attributes():
            return poi.get_attributes()


    if create_private_interface:
        private_poi = PyObjectInterface(obj, name, include_private=True, recursion_depth=recursion_depth)
        _create_webroutes(private_poi, '/webcontroller/private')
    public_poi = PyObjectInterface(obj, name, include_private=False, recursion_depth=recursion_depth)
    _create_webroutes(public_poi, '/webcontroller')


