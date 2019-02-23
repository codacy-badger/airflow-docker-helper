import json

from . import client, host
from .compat import BUILT_IN_MOCK_STRING, mock


def test_client(mock_context=None):
    if mock_context is None:
        mock_context = {}

    class _client:
        _mock_context = mock_context

        _mock_context_file = mock.Mock()
        _mock_short_circuit_file = mock.Mock()
        _mock_branch_to_tasks_file = mock.Mock()
        _mock_sensor_file = mock.Mock()

        @classmethod
        def short_circuit(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILT_IN_MOCK_STRING),
                mock.mock_open(cls._mock_short_circuit_file),
            ):
                return client.short_circuit(*args, **kwargs)

        @classmethod
        def branch_to_tasks(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILT_IN_MOCK_STRING),
                mock.mock_open(cls._mock_branch_to_tasks_file),
            ):
                return client.branch_to_tasks(*args, **kwargs)

        @classmethod
        def sensor(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILT_IN_MOCK_STRING),
                mock.mock_open(cls._mock_sensor_file),
            ):
                return client.sensor(*args, **kwargs)

        @classmethod
        def context(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILT_IN_MOCK_STRING),
                mock.mock_open(
                    cls._mock_context_file,
                    read_data=json.dumps(cls._mock_context).encode("utf-8"),
                ),
            ):
                return client.context(*args, **kwargs)

    return _client


def test_host(task_ids=None, sensor=None, short_circuit=None):
    class _host:
        _task_ids = task_ids
        _sensor = sensor
        _short_circuit = short_circuit

        _mock_context_file = mock.Mock()
        _mock_sensor_file = mock.Mock()
        _mock_short_circuit_file = mock.Mock()
        _mock_branch_file = mock.Mock()

        @classmethod
        def branch_task_ids(cls, *args, **kwargs):
            if cls._task_ids is not None:
                with mock.patch(
                    "{}.open".format(BUILT_IN_MOCK_STRING),
                    mock.mock_open(
                        cls._mock_branch_file,
                        read_data=json.dumps(cls._task_ids).encode("utf-8"),
                    ),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.branch_task_ids(*args, **kwargs)
            else:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.branch_task_ids(*args, **kwargs)

        @classmethod
        def short_circuit_outcome(cls, *args, **kwargs):
            if cls._short_circuit is None:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.short_circuit_outcome(*args, **kwargs)
            else:
                with mock.patch(
                    "{}.open".format(BUILT_IN_MOCK_STRING),
                    mock.mock_open(
                        cls._mock_short_circuit_file,
                        read_data=json.dumps(cls._short_circuit).encode("utf-8"),
                    ),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.short_circuit_outcome(*args, **kwargs)

        @classmethod
        def sensor_outcome(cls, *args, **kwargs):
            if cls._sensor is None:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.sensor_outcome(*args, **kwargs)
            else:
                with mock.patch(
                    "{}.open".format(BUILT_IN_MOCK_STRING),
                    mock.mock_open(
                        cls._mock_sensor_file,
                        read_data=json.dumps(cls._sensor).encode("utf-8"),
                    ),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.sensor_outcome(*args, **kwargs)

        @classmethod
        def write_context(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILT_IN_MOCK_STRING),
                mock.mock_open(cls._mock_context_file),
            ):
                return host.write_context(*args, **kwargs)

        @staticmethod
        def make_meta_dir(*args, **kwargs):
            return host.make_meta_dir(*args, **kwargs)

    return _host
