from airflow_docker_helper.testing import test_client as get_client


class TestBranchToTasks:

    def test_one_task_id(self):
        client = get_client()
        client.branch_to_tasks('test-task')
        open_file = client._mock_branch_to_tasks_file()
        assert len(open_file.write.mock_calls) == 1
        _, args, kwargs = open_file.write.mock_calls[0]
        assert args[0] == b'["test-task"]'

    def test_many_task_ids(self):
        client = get_client()
        client.branch_to_tasks(['test-task', 'other-task'])
        open_file = client._mock_branch_to_tasks_file()
        assert len(open_file.write.mock_calls) == 1
        _, args, kwargs = open_file.write.mock_calls[0]
        assert args[0] == b'["test-task", "other-task"]'


class TestSensor:

    def test_true_outcome(self):
        client = get_client()
        client.sensor(True)
        open_file = client._mock_sensor_file()
        assert len(open_file.write.mock_calls) == 1
        _, args, kwargs = open_file.write.mock_calls[0]
        assert args[0] == b'true'

    def test_false_outcome(self):
        client = get_client()
        client.sensor(False)
        open_file = client._mock_sensor_file()
        assert len(open_file.write.mock_calls) == 1
        _, args, kwargs = open_file.write.mock_calls[0]
        assert args[0] == b'false'


class TestShortCircuit:

    def test_short_circuit(self):
        client = get_client()
        client.short_circuit()
        open_file = client._mock_short_circuit_file()
        assert len(open_file.write.mock_calls) == 1
        _, args, kwargs = open_file.write.mock_calls[0]
        assert args[0] == b'false'


class TestContext:

    def test_context(self):
        mock_context = {'foo': 'bar'}
        client = get_client(mock_context=mock_context)
        context = client.context()
        assert context == mock_context
