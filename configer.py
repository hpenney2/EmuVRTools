from configmanager import Config

schema = {
    "evrconfig": {
        "cuecreator": {
            "presets": []
        },

        "evrdir": None
    }
}

config = Config(schema=schema, load_sources=["EVRToolsConfig.json"], auto_load=True)


def save():
    config.json.dump("EVRToolsConfig.json")
