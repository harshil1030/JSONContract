import json

def to_pascal(name):
    return ''.join(x.capitalize() for x in name.split('_'))

def detect_type(v):
    if isinstance(v, str): return "str"
    if isinstance(v, bool): return "boolean"
    if isinstance(v, int): return "int"
    if isinstance(v, float): return "real"
    if isinstance(v, list): return "List"
    if isinstance(v, dict): return "class"
    return "str"

def generate_class(name, data, classes):
    class_name = to_pascal(name) + "Contract"
    fields = []
    members = []

    for key, value in data.items():
        detected = detect_type(value)

        if detected == "class":
            generate_class(key, value, classes)
            type_name = to_pascal(key) + "Contract"

        elif detected == "List":
            if value and isinstance(value[0], dict):
                generate_class(key, value[0], classes)
                type_name = f"List /* of {to_pascal(key)}Contract */"
            else:
                type_name = "List"

        else:
            type_name = detected

        fields.append(f"    {type_name} {key};")

        members.append(f"""
    [DataMemberAttribute]
    public {type_name} parm{to_pascal(key)}({type_name} _{key} = {key})
    {{
        {key} = _{key};
        return {key};
    }}""")

    # Add line separator after class
    class_content = f"""
[DataContractAttribute]
class {class_name}
{{
{chr(10).join(fields)}

{chr(10).join(members)}
}}
------------------------------------------------------------------------
"""

    classes.append(class_content)
    return class_name

def convert(json_str):
    data = json.loads(json_str)
    classes = []
    generate_class("Root", data, classes)
    return "\n".join(classes)
