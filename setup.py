from setuptools import find_packages, setup


def parse_requirements(filename):
    with open(filename) as f:
        lineiter = (line.strip() for line in f)
        return [
            line.replace(' \\', '').strip()
            for line in lineiter
            if (
                line and
                not line.startswith("#") and
                not line.startswith("-e") and
                not line.startswith("--")
            )
        ]


setup(
    name='airflow-docker-helper',
    version='0.1.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    extras_require={
        'testing': parse_requirements('deps/testing-requirements.in'),
        'docs': parse_requirements('deps/docs-requirements.in'),
        'linting': parse_requirements('deps/linting-requirements.in'),
    },
    entry_points={
        'console_scripts': [
            'airflow-docker-helper=airflow_docker_helper.__main__:main',
        ]
    }
)
