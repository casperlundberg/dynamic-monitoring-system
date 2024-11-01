from typing import List, Dict, Any


def generate_enum_class(name: str, values: List[str]) -> str:
    enum_values = ", ".join([f'"{val}"' for val in values])
    return f"{name} = Literal[{enum_values}]"


def dict_to_dataclass_attributes(d: Dict[str, Any], indent: int = 4,
                                 parent_name: str = "") -> str:
    attributes = ""
    indent_str = " " * indent
    for k, v in d.items():
        if isinstance(v, dict):
            if "type" in v:
                if v["type"] == "object" and "properties" in v:
                    class_name = f"{parent_name}{k.capitalize()}"
                    attributes += f"{indent_str}{k}: {class_name}\n"
                    attributes += dict_to_dataclass_attributes(v["properties"],
                                                               indent + 4,
                                                               class_name)
                elif v["type"] == "array" and "items" in v:
                    item_type = v["items"].get("type", "Any")
                    if "enum" in v["items"]:
                        enum_name = f"{parent_name}{k.capitalize()}Enum"
                        enum_values = v["items"]["enum"]
                        attributes += f"{indent_str}{k}: List[{enum_name}]\n"
                    else:
                        attributes += f"{indent_str}{k}: List[{item_type.capitalize()}]\n"
                else:
                    attributes += f"{indent_str}{k}: {v['type'].capitalize()}\n"
            else:
                attributes += f"{indent_str}{k}: Any\n"
        else:
            attributes += f"{indent_str}{k}: {type(v).__name__}\n"
    return attributes
