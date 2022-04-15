from enum import Enum

class ActionTypes(Enum):
    OPEN = 1
    SELECT_ELEMENT = 2
    CLICK = 3
    SET_DATA = 4
    PAGINATION = 5
    WAIT = 6
    FOR_EACH_ELEMENT = 7
    ON_EACH_PAGE = 8
    CLOSE_TAB = 9
    MOVE_TO_NEXT_TAB = 10
