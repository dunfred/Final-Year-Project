class EnumChoiceToTupleMixin():

    @classmethod
    def choices(cls):
        # print([(choice.name, choice.value,) for choice in cls])
        return [(choice.name, choice.value,) for choice in cls]

