import bettercli.cl as cl

selector = cl.Selector(
    options={
        "option1": "option1 description",
        "option2": "option2 description",
        "option3": "option3 description",
    },
    question="What do you want to do?",
    style={
        "SELECTED": {
            "bg-color": "red",
            "fg-color": "white",
        },
    },
)

selected = selector.run()
print(selected)