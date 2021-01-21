## Non-Adiabatic Transitions in Quantum Molecular Dynamics
#### A project under the Supervision of Dr. Ben Goddard (School of Mathematics, University of Edinburgh) and Dr. Adam Kirrander (School of Chemistry,University of Edinburgh) 


## Authorship:
#### The repository is an attempt to replicate the repository authored by Dr. Ben Goddard, available at https://bitbucket.org/bdgoddard/qmd1dpublic/src/master/ but in Python rather than Matlab.

## Runnig scripts

#### Create a virtual environment with the packages listed in requirements.txt if you would like to avoid potential conflicts among projetcs

1. Create a virtualenv:
    ```unix
    virtualenv <project_name>
    ```
2. Activate environment:
    ```unix
    source activate <path_to_project_name>/bin/activate
    ```
3. Install packages:
    ```unix
    pip install -r <path_to_cloned_repository./requirements.txt
    ```

#### Now you are ready to run scripts from top directory

```python
python3 <file_name>.py
```

## Runnig tests

The tests/ folder contains...

## It should contain a few lines explaining the purpose of the project or library (without assuming the user knows anything about the project), the URL of the main source for the software, and some basic credit information. This file is the main entry point for readers of the code.


# TODO
planned development for the code.

Add inheritance diagram + other code structure diagrams...

np.ones((3,3), order 'F').flags - why is it faster??