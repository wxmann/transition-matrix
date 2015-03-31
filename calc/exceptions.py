__author__ = 'tangz'
class InvalidTransitionStateError(Exception):
    pass

class InvalidTransitionMatrixError(Exception):
    pass

class InvalidProbabilityError(InvalidTransitionMatrixError):
    pass

class UnnormalizedProbabilitiesError(InvalidProbabilityError):
    pass

class InconsistentStatesError(InvalidTransitionStateError):
    pass