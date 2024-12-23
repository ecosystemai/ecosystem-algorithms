from setuptools import setup
from pathlib import Path

setup(
    name='ecosystem-notebooks',
    version='0.1.25',
    description='Ecosystem Notebooks is a wrapper for the Ecosystem API servers.',
    long_description=Path("README.rst").read_text(encoding="utf-8"),
    url='https://github.com/ecosystemai/ecosystem-notebooks',
    author='EcosystemAi',
    author_email='jay@ecosystem.ai',
    license='MIT',
    packages=['runtime', 'runtime.apis', 'runtime.endpoints', 'runtime.utils', 'prediction', 'prediction.apis', 'prediction.endpoints', 'prediction.utils'],
    # packages=['runtime', 'prediction', 'notebook_server'],
    # install_requires=['numpy',
				# 	'plotly',
				# 	'matplotlib',
				# 	'pymongo',
				# 	'gunicorn',
				# 	'python-dateutil',
				# 	'Flask',
				# 	'Flask-Compress',
				# 	'Flask-Cors',
				# 	'Flask-RESTful',
				# 	'flask-restplus',
				# 	'flask-restx',
				# 	'Flask-Session',
				# 	'jupyterhub-nativeauthenticator',
				# 	'psycopg2-binary',
				# 	'seaborn',
				# 	'requests',
				# 	'pandas',
				# 	'Werkzeug',
				# 	'prophet',
				# 	'networkx',
				# 	'torch>=1.11.0',
				# 	'transformers',
				# 	'accelerate>=0.20.1',
				# 	'ipywidgets==7.7.5',
				# 	'sentence-transformers',
				# 	'scikit-learn',
				# 	'statsmodels',
				# 	'h2o==3.42.0.2',
				# 	'nltk',
				# 	'wordcloud',
				# 	'shapely',
				# 	'faker',
				# 	'sdv',
				# 	'agentpy',
				# 	'langchain',
				# 	'openai',
				# 	'bs4',
				# 	'tiktoken',
				# 	'gpt4all',
				# 	'chromadb',
				# 	'jq',
				# 	'nest_asyncio',
				# 	'pypdf',
				# 	'chardet',
				# 	'statistics',
				# 	'datetime',
    #                   ],
    install_requires=[
					'requests',
					'pymongo'
                      ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Framework :: Jupyter :: JupyterLab'
    ],
)

