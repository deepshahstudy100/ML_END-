from setuptools import find_packages,setup 
""" from this we can find all the packages in our ml project directories """
from typing import List 

HYPEN_E_DOT = '-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function return the list of requirements
    '''
    requirements =[]
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()  #  in the file of requirements.txt :  each one by one line reads but at the end '/n' get added , so for removing this : for loop . 
        requirements = [req.strip() for req in requirements]
        # to remove the -e . , we would like to remove from this 

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


# this file shared the imformation about the project 
setup(
    name='ml project',
    version='0.0.1',
    author='deep',
    author_email='deep.shah.study100@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"), # here we import all the libery from the requirements.txt file 
    )