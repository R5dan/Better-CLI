import bettercli.cl as cl

spinner = cl.Spinner(
    style={
        "states": [
            {"symbol": "⠋", "wait": 0.1, "message":{"message": "Hello, world!", "fg-color": cl.ANSIColors.green}},
            {"symbol": "⠙", "wait": 0.1, "fg-color": cl.ANSIColors.green},
            {"symbol": "⠹", "wait": 0.1, "bg-color": cl.ANSIColors.red},
            {"symbol": "⠸", "wait": 0.1},
            {"symbol": "⠼", "wait": 0.1},
            {"symbol": "⠴", "wait": 0.1},
            {"symbol": "⠦", "wait": 0.1},
            {"symbol": "⠧", "wait": 0.1},
            {"symbol": "⠇", "wait": 0.1},
        ],
        "wait": 0.1,
        "bg-color": cl.ANSIColors.red,
        "fg-color": cl.ANSIColors.white,
    }
)