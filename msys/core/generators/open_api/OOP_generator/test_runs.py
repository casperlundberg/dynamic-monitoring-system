from msys.core.generators.open_api.OOP_generator.path_model_file_generator import \
    PathModelFileGenerator

path_obj = {
    "/v1/forecast": {
        "servers": [
            {"url": "https://api.open-meteo.com"}
        ],
        "get": {
            "tags": ["Weather Forecast APIs"],
            "summary": "7 day weather forecast for coordinates",
            "description": "7 day weather variables in hourly and daily resolution for given WGS84 latitude and longitude coordinates. Available worldwide.",
            "parameters": [
                {
                    "name": "hourly",
                    "in": "query",
                    "explode": False,
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "temperature_2m", "relative_humidity_2m",
                                "dew_point_2m", "apparent_temperature",
                                "pressure_msl", "cloud_cover",
                                "cloud_cover_low", "cloud_cover_mid",
                                "cloud_cover_high",
                                "wind_speed_10m", "wind_speed_80m",
                                "wind_speed_120m", "wind_speed_180m",
                                "wind_direction_10m", "wind_direction_80m",
                                "wind_direction_120m", "wind_direction_180m",
                                "wind_gusts_10m", "shortwave_radiation",
                                "direct_radiation", "direct_normal_irradiance",
                                "diffuse_radiation", "vapour_pressure_deficit",
                                "evapotranspiration", "precipitation",
                                "weather_code", "snow_height",
                                "freezing_level_height",
                                "soil_temperature_0cm",
                                "soil_temperature_6cm",
                                "soil_temperature_18cm",
                                "soil_temperature_54cm",
                                "soil_moisture_0_1cm", "soil_moisture_1_3cm",
                                "soil_moisture_3_9cm", "soil_moisture_9_27cm",
                                "soil_moisture_27_81cm"
                            ]
                        }
                    }
                },
                {
                    "name": "daily",
                    "in": "query",
                    "schema": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": [
                                "temperature_2m_max", "temperature_2m_min",
                                "apparent_temperature_max",
                                "apparent_temperature_min",
                                "precipitation_sum", "precipitation_hours",
                                "weather_code",
                                "sunrise", "sunset", "wind_speed_10m_max",
                                "wind_gusts_10m_max",
                                "wind_direction_10m_dominant",
                                "shortwave_radiation_sum", "uv_index_max",
                                "uv_index_clear_sky_max",
                                "et0_fao_evapotranspiration"
                            ]
                        }
                    }
                },
                {
                    "name": "latitude",
                    "in": "query",
                    "required": True,
                    "description": "WGS84 coordinate",
                    "schema": {
                        "type": "number",
                        "format": "float"
                    }
                },
                {
                    "name": "longitude",
                    "in": "query",
                    "required": True,
                    "description": "WGS84 coordinate",
                    "schema": {
                        "type": "number",
                        "format": "float"
                    }
                },
                {
                    "name": "current_weather",
                    "in": "query",
                    "schema": {
                        "type": "boolean"
                    }
                },
                {
                    "name": "temperature_unit",
                    "in": "query",
                    "schema": {
                        "type": "string",
                        "default": "celsius",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                {
                    "name": "wind_speed_unit",
                    "in": "query",
                    "schema": {
                        "type": "string",
                        "default": "kmh",
                        "enum": ["kmh", "ms", "mph", "kn"]
                    }
                },
                {
                    "name": "timeformat",
                    "in": "query",
                    "description": "If format `unixtime` is selected, all time values are returned in UNIX epoch time in seconds. Please not that all time is then in GMT+0! For daily values with unix timestamp, please apply `utc_offset_seconds` again to get the correct date.",
                    "schema": {
                        "type": "string",
                        "default": "iso8601",
                        "enum": ["iso8601", "unixtime"]
                    }
                },
                {
                    "name": "timezone",
                    "in": "query",
                    "description": "If `timezone` is set, all timestamps are returned as local-time and data is returned starting at 0:00 local-time. Any time zone name from the [time zone database](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) is supported.",
                    "schema": {
                        "type": "string"
                    }
                },
                {
                    "name": "past_days",
                    "in": "query",
                    "description": "If `past_days` is set, yesterdays or the day before yesterdays data are also returned.",
                    "schema": {
                        "type": "integer",
                        "enum": [1, 2]
                    }
                }
            ],
            "responses": {
                "200": {
                    "description": "OK",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "latitude": {
                                        "type": "number",
                                        "example": 52.52,
                                        "description": "WGS84 of the center of the weather grid-cell which was used to generate this forecast. This coordinate might be up to 5 km away."
                                    },
                                    "longitude": {
                                        "type": "number",
                                        "example": 13.419,
                                        "description": "WGS84 of the center of the weather grid-cell which was used to generate this forecast. This coordinate might be up to 5 km away."
                                    },
                                    "elevation": {
                                        "type": "number",
                                        "example": 44.812,
                                        "description": "The elevation in meters of the selected weather grid-cell. In mountain terrain it might differ from the location you would expect."
                                    },
                                    "generationtime_ms": {
                                        "type": "number",
                                        "example": 2.2119,
                                        "description": "Generation time of the weather forecast in milli seconds. This is mainly used for performance monitoring and improvements."
                                    },
                                    "utc_offset_seconds": {
                                        "type": "integer",
                                        "example": 3600,
                                        "description": "Applied timezone offset from the &timezone= parameter."
                                    },
                                    "hourly": {
                                        "type": "HourlyResponse",
                                        "description": "For each selected weather variable, data will be returned as a floating point array. Additionally a `time` array will be returned with ISO8601 timestamps."
                                    },
                                    "hourly_units": {
                                        "type": "object",
                                        "additionalProperties": {
                                            "type": "string"
                                        },
                                        "description": "For each selected weather variable, the unit will be listed here."
                                    },
                                    "daily": {
                                        "type": "DailyResponse",
                                        "description": "For each selected daily weather variable, data will be returned as a floating point array. Additionally a `time` array will be returned with ISO8601 timestamps."
                                    },
                                    "daily_units": {
                                        "type": "object",
                                        "additionalProperties": {
                                            "type": "string"
                                        },
                                        "description": "For each selected daily weather variable, the unit will be listed here."
                                    },
                                    "current_weather": {
                                        "type": "CurrentWeather",
                                        "description": "Current weather conditions with the attributes: time, temperature, wind_speed, wind_direction and weather_code"
                                    }
                                }
                            }
                        }
                    }
                },
                "400": {
                    "description": "Bad Request",
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "error": {
                                        "type": "boolean",
                                        "description": "Always set true for errors"
                                    },
                                    "reason": {
                                        "type": "string",
                                        "description": "Description of the error",
                                        "example": "Latitude must be in range of -90 to 90°. Given: 300"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

path_gen = PathModelFileGenerator(path_obj)
path_gen.generate_imports()
path_gen.generate_path_class()
print(path_gen.code_string)
