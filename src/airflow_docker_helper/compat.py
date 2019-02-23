try:
    import unittest.mock as mock
except ImportError:
    import mock

try:
    import builtins

    BUILT_IN_MOCK_STRING = "builtins"
except ImportError:
    import __builtin__

    BUILT_IN_MOCK_STRING = "__builtin__"
