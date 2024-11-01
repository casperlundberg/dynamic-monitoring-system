from typing import Dict, Any

from msys.core.generators.open_api.OOP_generator.helper_functions import \
    generate_enum_class


class ParameterModelFileGenerator:
    def __init__(self, parameter_obj: Dict[str, Any]):
        self.parameter = parameter_obj
        self.name, self.required, self.schema, self.exploded = self.parse_parameter()

        self.classname = self.name.capitalize()
        self.filename = self.name

        self.imports = None

        self.used_keywords = self.parse_schema()

        self.code_string = ""
        self.enums = []

    def parse_parameter(self):
        name = self.parameter.get("name")
        required = self.parameter.get("required")
        schema = self.parameter.get("schema")
        exploded = self.parameter.get("explode")
        return name, required, schema, exploded

    def parse_schema(self):
        keywords_in_use = {}

        relevant_keywords = [
            "type", "properties", "required", "items", "enum", "format",
            "default", "nullable", "readOnly", "writeOnly", "deprecated",
            "description", "example", "title", "multipleOf", "maximum",
            "exclusiveMaximum", "minimum", "exclusiveMinimum", "maxLength",
            "minLength", "pattern", "maxItems", "minItems", "uniqueItems",
            "maxProperties", "minProperties", "additionalProperties"
        ]

        for keyword in relevant_keywords:
            if keyword in self.schema:
                keywords_in_use[keyword] = self.schema.get(keyword)

        return keywords_in_use

    def generate_imports(self):
        self.imports = "from dataclasses import dataclass\nfrom typing import *"

    def dict_to_dataclass_attributes(self, d: Dict[str, Any], indent: int = 4,
                                     parent_name: str = "") -> str:
        attributes = ""
        indent_str = " " * indent
        for k, v in d.items():
            if isinstance(v, dict):
                if "type" in v:
                    if v["type"] == "object" and "properties" in v:
                        class_name = f"{parent_name}{k.capitalize()}"
                        attributes += f"{indent_str}{k}: {class_name}\n"
                        attributes += self.dict_to_dataclass_attributes(
                            v["properties"], indent + 4, class_name)
                    elif v["type"] == "array" and "items" in v:
                        item_type = v["items"].get("type", "Any")
                        if "enum" in v["items"]:
                            enum_name = f"{parent_name}{k.capitalize()}Enum"
                            enum_values = v["items"]["enum"]
                            self.enums.append(
                                generate_enum_class(enum_name,
                                                    enum_values))
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

    def generate_schema_class(self):
        enums_code = "\n".join(self.enums)
        attributes = self.dict_to_dataclass_attributes({"schema": self.schema},
                                                       parent_name=self.classname)
        self.code_string = f"""{self.imports}
{enums_code}

@dataclass
class {self.classname}:
    name: str
    in_: str
{attributes}
        """
