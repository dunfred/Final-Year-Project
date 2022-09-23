class EnumChoiceToTupleMixin():

    @classmethod
    def choices(cls):
        return [(choice, choice.value) for choice in cls]

