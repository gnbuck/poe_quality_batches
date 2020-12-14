class ExceptionHandler(Exception):
    """Base exception handler class."""

    def __init__(self):
        super().__init__(self)
        self.message = "NonImplementedError: Unknown error happened"

    def __str__(self):
        return self.message


class BadObjectType(ExceptionHandler):
    """Malformated object type exception handler class."""

    def __init__(self, obj_types, obj):
        self.obj_types = obj_types
        self.obj = obj
        self.enum = [item["name"] for item in self.obj_types.values()]
        self.message = (
            f"BadObjectTypeError: Object '{self.obj}' is not one of {self.enum}"
        )

    def __str__(self):
        return self.message


class BadInput(ExceptionHandler):
    """Wrong input variables exception handler class."""

    def __init__(self, *vars):
        self.vars = vars
        self.message = (
            f"InputExceptionError: Following variables are missing: {self.vars}"
        )

    def __str__(self):
        return self.message
