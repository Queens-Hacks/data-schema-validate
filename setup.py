from setuptools import setup

setup(name='rx-data-validate',
      version='0.0.2',
      author='Philip Schleihauf',
      author_email='uniphil@gmail.com',
      license='MIT',
      description='Validate Qcumber Data',
      long_description=open('readme.md').read(),
      py_modules=['data_schema_validate'],
      scripts=['data_schema_validate.py'],
      install_requires=['pyrx', 'pyyaml'])
