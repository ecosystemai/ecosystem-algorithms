# Ecosystem Algorithms

## What is Ecosystem Algorithms?

Ecosystem Algorithms business layer on top of Ecosystem Notebooks, demonstrating how to effectively use and impletment different business cases.

## Requirements

To use any of these algorithms [Ecosystem Notebooks](https://github.com/ecosystemai/ecosystem-algorithms) need to be installed.
Jupyter Notebook
Python3

## Getting started

To get going with Ecosystem Algorithms, start by installing Jupyter Notebook.

**Note:** if Ecosystem Notebooks is already installed then all the required software will available.

This can be done by running the configure_jupyter.sh shell script, in addition recommended styling options can be added by running the configure_jupyter_styling.sh shell script, but is not required.

To install the relevant python code add the parent directory(ecosystem-notebooks) to the PYTHONPATH environment variable. 

Once Jupyter is installed run the command:
```bash
jupyter notebook
```
in the directory containing the algorithm notebooks designated by the .ipynb extention.

This will open up a default web browser to the Jupyter Notebook landing page from which you can open up the required notebook.

## How does Ecosystem Algorithms work

The opened notebook is a live computing environment, allowing code to be edited and run in place. 
To navigate the notebook, use the table of contents on the left to easily find any section.

Logging on is required before any of the api endpoints will function. Depending on the algorithm notebook this will either be a username, password and url endpoint combination or just an url endpoint. This will generate an authentication token that all api calls required to function.

![Login1](https://github.com/ecosystemai/ecosystem-algorithms/blob/master/docs/images/login1.png "Login1")
![Login2](https://github.com/ecosystemai/ecosystem-algorithms/blob/master/docs/images/login1.png "Login2")