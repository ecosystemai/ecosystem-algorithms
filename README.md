# Ecosystem Algorithms

## What is Ecosystem Algorithms?

Ecosystem Algorithms is for the business user and resides within Ecosystem Notebooks. It allows you to effectively use and implement multiple types of business cases, offering an opportunity to demonstrate proficient integration within your workplace.

## Requirements

* To use any of these algorithms, [Ecosystem Notebooks](https://github.com/ecosystemai/ecosystem-notebooks) you must first install Ecosystem Notebooks
* Access to an Ecosystem API server is required
* Jupyter Notebook
* [Python3](https://www.python.org/downloads/): The notebooks were built using python 3.6, but most Python 3 versions will work

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

This will open up a default web browser to the Jupyter Notebook landing page from which you can open up one of the desired Ecosystem Notebooks. It is from within the Ecosystem Notebooks that you can use the Ecosystem Algorithms.

![Jupyter Landing Page](https://github.com/ecosystemai/ecosystem-algorithms/blob/master/docs/images/jupyter_landing_page.png "Jupyter Landing Page")

## How does Ecosystem Algorithms work

It is from within a chosen notebook that the Ecosystem Algorithms can be used.  This coding environment, from which you can edit and run live code, is the interface which utilises the algorithms for business case uses. For easy navigation within any of the notebooks, you can use the table of contents which will be situated on the left.

In order for the API endpoints to properly function, you will need to login. Depending on which notebooks you have chosen to use, logging in could require a URL endpoint. Or a username, password and URL combination, which will generate an authentication token. This token will activate the API, then you can begin using Ecosystem Notebooks, and subsequently implementing your business algorithms.

![Login](https://github.com/ecosystemai/ecosystem-algorithms/blob/master/docs/images/login.png "Login")

Ecosystem Algorithms contains a myriad of business cases for you to play around with. You can either work within the Ecosystem environment, or implement it within you own chosen infrastructure.
