from airflow_docker_helper.testing import test_host as get_host_client
from airflow_docker_helper.compat import mock


class TestBranchToTasks:

    def test_one_task_id(self):
        client = get_host_client(task_ids=['foo'])
        tmp_dir = 'META_DIR'
        task_ids = client.branch_task_ids(tmp_dir)
        assert task_ids == ['foo']

    def test_many_task_ids(self):
        client = get_host_client(task_ids=['foo', 'bar'])
        tmp_dir = 'META_DIR'
        task_ids = client.branch_task_ids(tmp_dir)
        assert task_ids == ['foo', 'bar']

    def test_no_task_ids(self):
        client = get_host_client()
        tmp_dir = 'META_DIR'
        task_ids = client.branch_task_ids(tmp_dir)
        assert task_ids == []


class TestSensor:

    def test_true_outcome(self):
        client = get_host_client(sensor=True)
        tmp_dir = 'META_DIR'
        sensor_outcome = client.sensor_outcome(tmp_dir)
        assert sensor_outcome is True

    def test_false_outcome(self):
        client = get_host_client(sensor=False)
        tmp_dir = 'META_DIR'
        sensor_outcome = client.sensor_outcome(tmp_dir)
        assert sensor_outcome is False

    def test_no_outcome(self):
        client = get_host_client()
        tmp_dir = 'META_DIR'
        sensor_outcome = client.sensor_outcome(tmp_dir)
        assert sensor_outcome is False


class TestShortCircuit:

    def test_short_circuit(self):
        client = get_host_client(short_circuit=False)
        tmp_dir = 'META_DIR'
        short_circuit_outcome = client.short_circuit_outcome(tmp_dir)
        assert short_circuit_outcome is False

    def test_no_short_circuit(self):
        client = get_host_client()
        tmp_dir = 'META_DIR'
        short_circuit_outcome = client.short_circuit_outcome(tmp_dir)
        assert short_circuit_outcome is True


class TestWriteContext:

    def test_context(self):
        client = get_host_client()
        test_context = {'foo': 'bar'}
        tmp_dir = 'META_DIR'
        with mock.patch('airflow_docker_helper.serialize_context', return_value=test_context):
            client.write_context(test_context, tmp_dir)
            open_file = client._mock_context_file()
            assert len(open_file.write.mock_calls) == 1
            _, args, kwargs = open_file.write.mock_calls[0]
            assert args[0] == b'{"foo": "bar"}'


def get_test_context():
    import datetime

    execution_date = datetime.datetime.now()
    prev_execution_date = execution_date + datetime.timedelta(days=-1)
    next_execution_date = execution_date + datetime.timedelta(days=1)

    return {
        "dag": "a dag",
        "ds": "2019-02-22",
        "next_ds": "2019-02-22",
        "next_ds_nodash": "20190222",
        "prev_ds": "2019-02-22",
        "prev_ds_nodash": "20190222",
        "ds_nodash": "20190222",
        "ts": "2019-02-22T05:56:17.977197+00:00",
        "ts_nodash": "20190222T055617",
        "ts_nodash_with_tz": "20190222T055617.977197+0000",
        "yesterday_ds": "2019-02-21",
        "yesterday_ds_nodash": "20190221",
        "tomorrow_ds": "2019-02-23",
        "tomorrow_ds_nodash": "20190223",
        "END_DATE": "2019-02-22",
        "end_date": "2019-02-22",
        "dag_run": "a dag run",
        "run_id": "manual__2019-02-22T05:56:17.977197+00:00",
        "execution_date": execution_date,
        "prev_execution_date": prev_execution_date,
        "next_execution_date": next_execution_date,
        "latest_date": "2019-02-22",
        "macros": "blah",
        "params": {},
        "tables": "None",
        "task": "task sensor",
        "task_instance": "a task instance ",
        "ti": "a task instance",
        "task_instance_key_str": "adag__task-name__20190222",
        "conf": "blah",
        "test_mode": False,
        "var": {
            "value": "None",
            "json": "None"
        },
        "inlets": [],
        "outlets": []
    }
