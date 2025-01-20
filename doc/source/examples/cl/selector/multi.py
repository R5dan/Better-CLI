import bettercli.cl as cl

selector = cl.Selector(
    options={
        "option1": "option1 description",
        "option2": "option2 description",
        "option3": "option3 description",
    },
    question="What do you want to do?",
)

@selector.validator()
def validator(options):
    if len(options) == 1:
        return "You must select at least two options"
    return True

selected = selector.run()
print(selected)