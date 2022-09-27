from enum import Enum
from counsellor.mixin import EnumChoiceToTupleMixin

class UserType(EnumChoiceToTupleMixin, Enum):
    STUDENT     = "student"
    NON_STUDENT = "non_student"
    STAFF       = "staff"
    NON_STAFF   = "non_staff"
    
class Gender(EnumChoiceToTupleMixin, Enum):
    MALE    = 'male'
    FEMALE  = 'female'
    UNKNOWN = 'unknown'

    
class MaritalStatus(EnumChoiceToTupleMixin, Enum):
    MARRIED   = 'married'
    SINGLE    = 'single'
    SEPARATED = 'separated'
    DIVORCED  = 'divorced'
    WIDOWED   = 'widowed'
    WIDOWER   = 'widower'


class Religion(EnumChoiceToTupleMixin, Enum):
    CHRISTIAN    = 'christian'
    MUSLIM       = 'muslim'
    TRADITIONAL  = 'traditional'
    OTHER        = 'other'


class Level(EnumChoiceToTupleMixin, Enum):
    YEAR_100    = 100
    YEAR_200    = 200
    YEAR_300    = 300
    YEAR_400    = 400
    YEAR_500    = 500
    YEAR_600    = 600
    YEAR_700    = 700
    YEAR_800    = 800

class StringBoolChoices(EnumChoiceToTupleMixin, Enum):
    YES = "yes"
    NO  = "no"

class Honorifics(EnumChoiceToTupleMixin, Enum):
    MR      = "Mr"
    MRS     = "Mrs"
    MISS    = "Miss"
    MS      = "Ms"
    DR      = "Dr"


