from setuptools import setup

setup(
    name='input_mobile',
    version='0.1.3',
    install_requires=[
        'requests',
        'boto3',
        'botocore',
        'python-dotenv',
        'pymongo'
    ],
)