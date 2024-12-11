tools = [
    {
        "name": "add_two_integers",
        "description": "A simple tool that adds two integers.",
        "input_schema": {
            "type": "object",
            "properties": {
                "integer1": {
                    "type": "integer",
                    "description": "The first integer to add.",
                },
                "integer2": {
                    "type": "integer",
                    "description": "The second integer to add.",
                },
            },
            "required": ["integer1", "integer2"],
        },
    }
]
