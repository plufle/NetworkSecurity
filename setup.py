'''
The setup.py file is used to install the dependencies of the project. 
'''

from setuptools import setup,find_packages
from typing import List

def get_requirements(file_path:str) -> List[str]:
    """
    This function will return the list of requirements
    """
    requirements_list:List[str] = []
    try:
        with open(file_path,'r') as file_obj:
            requirements = file_obj.readlines()
            for req in requirements:
                req = req.strip()
                if req and req != "-e .":
                    requirements_list.append(req)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File {file_path} not found: {e}")
    return requirements_list

setup(
    name='Network Security',
    version='0.0.1',
    author='Plufle',
    author_email='[EMAIL_ADDRESS]',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)
