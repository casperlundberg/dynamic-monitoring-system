from src.core.generators.openAPI.parser.misc_parser import *
from src.core.generators.openAPI.models.misc import Tag, License, Contact, \
    Info, ExternalDocs
import unittest


class TestMiscParser(unittest.TestCase):
    def test_parse_info(self):
        info = {
            "title": "Swagger Petstore - OpenAPI 3.0",
            "description": "This is a sample Pet Store Server based on the OpenAPI 3.0 specification.  You can find out more about\nSwagger at [https://swagger.io](https://swagger.io). In the third iteration of the pet store, we've switched to the design first approach!\nYou can now help us improve the API whether it's by making changes to the definition itself or to the code.\nThat way, with time, we can improve the API in general, and expose some of the new features in OAS3.\n\n_If you're looking for the Swagger 2.0/OAS 2.0 version of Petstore, then click [here](https://editor.swagger.io/?url=https://petstore.swagger.io/v2/swagger.yaml). Alternatively, you can load via the `Edit > Load Petstore OAS 2.0` menu option!_\n\nSome useful links:\n- [The Pet Store repository](https://github.com/swagger-api/swagger-petstore)\n- [The source API definition for the Pet Store](https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml)",
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
