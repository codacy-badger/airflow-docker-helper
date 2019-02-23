import airflow_docker_helper
from airflow_docker_helper.compat import mock
import os


def test_branch_operator_file_path():
    test_dir = 'foo'
    branch_operator_file_path = airflow_docker_helper._get_branch_operator_file_path(test_dir)
    assert test_dir in branch_operator_file_path
    assert branch_operator_file_path == os.path.join(
        test_dir,
        airflow_docker_helper.BRANCH_OPERATOR_FILENAME
    )


def test_short_circuit_file_path():
    test_dir = 'foo'
    short_circuit_file_path = airflow_docker_helper._get_short_circuit_operator_file_path(test_dir)
    assert test_dir in short_circuit_file_path
    assert short_circuit_file_path == os.path.join(
        test_dir,
        airflow_docker_helper.SHORT_CIRCUIT_OPERATOR_FILENAME
    )


def test_sensor_file_path():
    test_dir = 'foo'
    sensor_file_path = airflow_docker_helper._get_sensor_file_path(test_dir)
    assert test_dir in sensor_file_path
    assert sensor_file_path == os.path.join(
        test_dir,
        airflow_docker_helper.SENSOR_OPERATOR_FILENAME
    )


def test_context_file_path():
    test_dir = 'foo'
    context_file_path = airflow_docker_helper._get_context_file_path(test_dir)
    assert test_dir in context_file_path
    assert context_file_path == os.path.join(test_dir, airflow_docker_helper.CONTEXT_FILENAME)


def test_host_meta_path():
    tmp_dir = 'SOME_DIR'
    host_meta_path = airflow_docker_helper.get_host_meta_path(tmp_dir)
    assert tmp_dir in host_meta_path
    assert host_meta_path == os.path.join(tmp_dir, airflow_docker_helper.META_PATH_DIR)


def test_container_meta_path_from_env():
    with mock.patch.dict(os.environ, {'AIRFLOW_TMP_DIR': 'SOME_DIR'}):
        container_meta_path = airflow_docker_helper._get_container_meta_path()

    assert 'SOME_DIR' in container_meta_path
    assert container_meta_path == os.path.join('SOME_DIR', airflow_docker_helper.META_PATH_DIR)
