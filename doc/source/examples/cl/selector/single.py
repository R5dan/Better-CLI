import bettercli.cl as cl

selector = cl.SingleSelector(
    options={
        "option1": "option1 description",
        "option2": "option2 description",
        "option3": "option3 description",
    },
    question="What do you want to do?",
)

selected = selector.run()
print(selected)