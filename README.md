# Ecosystem Algorithms

## What is Ecosystem Algorithms?

Ecosystem Algorithms contains common business case implementations for Ecosystem Notebooks. It allows you to effectively use and implement multiple types of business cases, offering an opportunity to demonstrate proficient integration within your workplace.

## Requirements

* To use any of these algorithms [Ecosystem Notebooks](https://github.com/ecosystemai/ecosystem-notebooks) need to be installed
* Access to an Ecosystem API server
* [Jupyter Notebook](https://jupyter.org/)
* [Python 3](https://www.python.org/downloads/): Was built using Python 3.6, but most Python 3 versions will work.

## Getting started

To begin using Ecosystem Algorithms,  you need to first install Jupyter Notebook.

**Note:** If Ecosystem Notebooks is already installed, then all the required software should already be in place.

This can be done by running the configure_jupyter.sh shell script. 
In addition, recommended styling options can be added by running the configure_jupyter_styling.sh shell script. While this is not required, you are welcome to play around with it to personalise the Ecosystem workbench style.

To install the relevant python code, add the parent directory (ecosystem-notebooks) to the PYTHONPATH environment variable.

Once Jupyter is installed, enter the directory containing the notebooks. At the designated .ipynb extension, run the command:
```bash
jupyter notebook
```

This will open up a default web browser to the Jupyter Notebook landing page from which you can open up one of the desired notebooks. It is from within these notebooks that you can access the Ecosystem Algorithms.

![Jupyter Landing Page](https://github.com/ecosystemai/ecosystem-algorithms/blob/master/docs/images/jupyter_landing_page.png "Jupyter Landing Page")

## How does Ecosystem Algorithms work

From within a chosen notebook, Ecosystem Algorithms can be used. This coding environment, from which you can edit and run live code, provides the interface with which to utilise the algorithms for business use cases. For easy navigation within any of the notebooks, you can use the table of contents which will be situated on the left.

In order for the API endpoints to properly function, you will need to login. Depending on which notebooks you have chosen to use, logging in could require a URL endpoint. Or a username, password and URL combination, which will generate an authentication token. This token must be passed along to the API, then you can begin using Ecosystem Algorithms, and subsequently implementing your business algorithms.

![Login](https://github.com/ecosystemai/ecosystem-algorithms/blob/master/docs/images/login.png "Login")

Ecosystem Algorithms contains a myriad of business cases for you to play around with. From building and training models to offer recommendations, you can either work within the Ecosystem environment, or implement it within your own chosen infrastructure.
