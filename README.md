# Ecosystem Algorithms

## What is Ecosystem Algorithms?

Ecosystem Algorithms contains common business case implementations for Ecosystem Notebooks. It allows you to effectively use and implement multiple types of business cases, offering an opportunity to demonstrate proficient integration within your workplace.

## Requirements

* Access to the ecosystem.Ai server and runtime instances.
* [Python 3.12](https://www.python.org/downloads/): Was built using Python 3.12.

## Getting started

You can run ecosystem algorithms inside a container and then access all the libraries using Docker  commands.

```bash
docker run -d --restart unless-stopped \
   --net-alias ecosystem-algorithms --network ecosystem --name ecosystem-algorithms \
   ecosystemai/ecosystem-algorithms:latest
```

Container can be used to execute any Python program.
