import unittest
from packages.flatten_prop_schema.flatten_prop import flatten_properties


class TestFlattenProperties(unittest.TestCase):
    def test_non_nested_properties(self):
        properties = {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "is_active": {"type": "boolean"}
        }
        expected = [
            ("name", "TEXT"),
            ("age", "INTEGER"),
            ("is_active", "BOOLEAN")
        ]
        result = flatten_properties(properties)
        self.assertEqual(result, expected)

    def test_nested_properties(self):
        properties = {
            "user": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                }
            },
            "is_active": {"type": "boolean"}
        }
        expected = [
            ("user_name", "TEXT"),
            ("user_age", "INTEGER"),
            ("is_active", "BOOLEAN")
        ]
        result = flatten_properties(properties)
        self.assertEqual(result, expected)

    def test_deeply_nested_properties(self):
        properties = {
            "user": {
                "type": "object",
                "properties": {
                    "profile": {
                        "type": "object",
                        "properties": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"}
                        }
                    },
                    "age": {"type": "integer"}
                }
            },
            "is_active": {"type": "boolean"}
        }
        expected = [
            ("user_profile_first_name", "TEXT"),
            ("user_profile_last_name", "TEXT"),
            ("user_age", "INTEGER"),
            ("is_active", "BOOLEAN")
        ]
        result = flatten_properties(properties)
        self.assertEqual(result, expected)

    def test_properties_with_formats(self):
        properties = {
            "created_at": {"type": "string", "format": "date-time"},
            "price": {"type": "number"}
        }
        expected = [
            ("created_at", "TIMESTAMPTZ"),
            ("price", "DOUBLE PRECISION")
        ]
        result = flatten_properties(properties)
        self.assertEqual(result, expected)

    def test_heavily_nested_properties(self):
        properties = {
            "deviceconfiguration": {
                "type": "object",
                "properties": {
                    "network": {
                        "type": "object",
                        "properties": {
                            "ip": {"type": "string", "format": "ipv4"},
                            "mac": {"type": "string"}
                        }
                    },
                    "thresholds": {
                        "type": "object",
                        "properties": {
                            "temperature": {"type": "number"},
                            "pressure": {"type": "number"}
                        }
                    },
                    "maintenanceschedule": {
                        "type": "object",
                        "properties": {
                            "nextCheck": {"type": "string",
                                          "format": "date-time"},
                            "lastCheck": {"type": "string",
                                          "format": "date-time"}
                        }
                    }
                }
            }
        }
        expected = [
            ("deviceconfiguration_network_ip", "TEXT"),
            ("deviceconfiguration_network_mac", "TEXT"),
            ("deviceconfiguration_thresholds_temperature", "DOUBLE PRECISION"),
            ("deviceconfiguration_thresholds_pressure", "DOUBLE PRECISION"),
            ("deviceconfiguration_maintenanceschedule_nextcheck",
             "TIMESTAMPTZ"),
            (
                "deviceconfiguration_maintenanceschedule_lastcheck",
                "TIMESTAMPTZ")
        ]
        result = flatten_properties(properties)
        self.assertEqual(result, expected)

    def test_empty_properties(self):
        properties = {}
        expected = []
        result = flatten_properties(properties)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
