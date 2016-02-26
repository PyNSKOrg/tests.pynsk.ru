class TestAppError(Exception):
    def __str__(self):
        return "Error in test application"


class OpenGameAlreadyExists(TestAppError):
    def __str__(self):
        return "Player already has open game."


class TestIsNotAvailable(TestAppError):
    def __init__(self, available_time=None):
        self.available_time = available_time

    def __str__(self):
        return "Test is not available."


