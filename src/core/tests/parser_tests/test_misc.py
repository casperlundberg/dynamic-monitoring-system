from src.core.generators.open_api.parser.misc_parser import *
from src.core.generators.open_api.models.misc import Tag, License, Contact, \
    Info, ExternalDocs
import unittest


class TestMiscParser(unittest.TestCase):
    def test_parse_info(self):
        info = {
            "title": "Swagger Petstore - OpenAPI 3.0",
            "description": "This is a sample Pet Store Server based on the OpenAPI 3.0 specification.",
            "termsOfService": "http://swagger.io/terms/",
            "contact": {
                "email": "apiteam@swagger.io"
            },
            "license": {
                "name": "Apache 2.0",
                "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
            },
            "version": "1.0.11"
        }
        assert parse_info(info) == Info(**info)

    def test_parse_external_docs(self):
        external_docs = {
            "description": "Find out more about Swagger",
            "url": "http://swagger.io"
        }
        assert parse_external_docs(external_docs) == ExternalDocs(
            **external_docs)

    def test_parse_contact(self):
        contact = {
            "name": "API Support",
            "email": "apiteam@swagger.io"
        }
        assert parse_contact(contact) == Contact(**contact)

    def test_parse_license(self):
        _license = {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
        assert parse_license(_license) == License(**_license)

    def test_parse_tags(self):
        tags = [
            {
                "name": "pet",
                "description": "Everything about your Pets",
                "externalDocs": {
                    "description": "Find out more",
                    "url": "http://swagger.io"
                }
            },
            {
                "name": "store",
                "description": "Access to Petstore orders",
                "externalDocs": {
                    "description": "Find out more about our store",
                    "url": "http://swagger.io"
                }
            },
            {
                "name": "user",
                "description": "Operations about user"
            }
        ]
        assert parse_tags(tags) == [Tag(**tag) for tag in tags]
