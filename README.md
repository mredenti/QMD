## Non-Adiabatic Transitions in Quantum Molecular Dynamics
## Table of contents
* [Introduction](#introduction)
* [Installation](#installation)
* [Contacts](#contacts)
* [Acknowledgements](#acknowledgements)

## Introduction
QMD is a library for quantum molecular dynamics on multiple electronic energy levels in one dimension. As of this moment, it supports a Strang-Splitting scheme to compute reference solutions, an algorithm for computing non-adiabatic transitions that requires only one level Born-Oppenheimer dynamics (https://epubs.siam.org/doi/abs/10.1137/100802347) and a surface hopping algorithm. The library is designed for proof of concepts ideas for low dimensional systems. 

## Installation

Create a virtual environment with the packages listed in requirements.txt if you would like to avoid potential conflicts among projetcs

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

Now you are ready to run scripts from top directory

```python
python3 <file_name>.py
```

## Contacts
If you have any questions or you would like to collaborate, feel free to contact:
  * Mr. Michael Redenti (M.Redenti@sms.ed.ac.uk)
  
## Acknowledgements
The development of QMD was made possible with the support of the following organization:
| Logo | Name | URL |
|:----:|:----:|:---:|
|![mifms](doc/maxwell-logo.png) | Maxwell Institute For Mathematical Sciences | https://www.maxwell.ac.uk/graduate-school/|


