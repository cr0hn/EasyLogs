# EasyLogs - The simple, agnostic and lightweight logging dashboard

![License](https://img.shields.io/badge/License-Apache2-SUCCESS)

![Logo](https://raw.githubusercontent.com/cr0hn/easylogs/main/images/logo-250x250.jpg)

In a nutshell ``EasyLogs`` is a simple, but powerful, dashboard to visualize logs.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
- [EasyLogs - The simple, agnostic and lightweight logging dashboard](#easylogs---the-simple-agnostic-and-lightweight-logging-dashboard)

- [What is EasyLogs?](#what-is-easylogs)
  - [Why not...](#why-not)
  - [EasyLogs is for you if...](#easylogs-is-for-you-if)
- [Some screenshots](#some-screenshots)
- [Deployment](#deployment)
  - [Configuration](#configuration)
  - [Docker (standalone)](#docker-standalone)
  - [Docker (external MongoDB & Redis)](#docker-external-mongodb--redis)
  - [Docker Compose](#docker-compose)
- [How to log to EasyLogs?](#how-to-log-to-easylogs)
  - [Python](#python)
    - [Python HTTP Handler](#python-http-handler)
  - [Java (NOT IMPLEMENTED)](#java-not-implemented)
  - [Go (NOT IMPLEMENTED)](#go-not-implemented)
  - [NodeJS (NOT IMPLEMENTED)](#nodejs-not-implemented)
  - [C# (NOT IMPLEMENTED)](#c-not-implemented)
  - [Ruby (NOT IMPLEMENTED)](#ruby-not-implemented)
- [Contributing](#contributing)
  - [Adding new loggers](#adding-new-loggers)
  - [Adding new loggers + API](#adding-new-loggers--api)
- [TODO](#todo)
- [License](#license)
- [Acknowledgments](#acknowledgments)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# What is EasyLogs?

EasyLogs is a agnostic dashboard for display and filter logs. It can be used with any log source.

The main idea is to provide a simple and lightweight dashboard to visualize logs that you can use quickly.

## Why not...

There are a lot of log dashboards out there:

- Kibana
- Graylog
- Splunk
- Logstash
- ...

But most of them are very complex to configure and use. EasyLogs is a simple dashboard that can be used with any log source.

## EasyLogs is for you if...

- You want to use a simple dashboard.
- You want to visualize logs in a simple way.
- You want only a basic logs filtering.
- You want a fast deployment and lightweight dashboard.
- You don't need a complex log dashboard.
- You don't want to spend time configuring a log dashboard.
- You don't need analytics of your logs.

# Some screenshots

![Screenshot 1](https://raw.githubusercontent.com/cr0hn/easylogs/main/images/screenshot-001.png)

![Screenshot 2](https://raw.githubusercontent.com/cr0hn/easylogs/main/images/screenshot-002.png)

![Screenshot 3](https://raw.githubusercontent.com/cr0hn/easylogs/main/images/screenshot-003.png)


# Deployment

EasyLogs is composed by:

- The Web Application, aka, the Dashboard.
- MongoDB database for storing logs.
- Redis database for storing sessions.

So, you need to have both running.

## Configuration

EasyLogs is configured using environment variables. This table shows all the available configuration options:

| Variable | Description                | Default value |
| --- |----------------------------| -- |
| `REDIS_URI` | Redis Connection string | `redis://127.0.0.1:6379/0` |
| `MONGO_DB` | MongoDB database | `easylogs` |
| `MONGO_URI` | MongoDB Connection string | `mongodb://root:example@127.0.0.1:27099` |
| `ADMIN_USER` | Admin user | `admin` |
| `ADMIN_PASSWORD` | Admin Password | `adminadmin` |
| `RECEIVE_LOGS_KEY` | Key used to authenticate loggers  | `LIh982y87GgljahsadfklJHLIUG87g1u1e7f6eb2ee145571858e8e24` |
| `EMBEDED_DB` | If this variable is set, enables MongoDB and Redis embedded databases. Allowed values: TRUE|TRUE | Not set |

> NOTE: If you want to use MongoDB embedded database, you don't need to set `MONGO_URI` and `MONGO_DB` variables.

> Currently, EasyLogs only support fixed authentication. In the future, we will add support for other authentication methods.

## Docker (standalone)

Easylog has the possibility to run MongoDB and the Web Application in the same container. This is the easiest way to run EasyLogs.

```bash
> docker run -e EMBEDED_DB=1 -p 8080:8080 cr0hn/easylogs
```

> NOTE: Not recommended for production environments.

## Docker (external MongoDB & Redis)

If you want to run EasyLogs in a production environment, you should use an external MongoDB & Redis databases.

```bash
> export MONGO_URI=mongodb://...
> export REDIS_URI=redis://...
> docker run -e MONGODB_URI=$MONGODB_URI -e REDIS_URI=$REDIS_URI -p 8080:8080 cr0hn/easylogs
```

> NOTE: If you don't want to deploy and maintain a MongoDB, you can use a [MongoDB Atlas](https://www.mongodb.com/atlas/database) cloud database. It's free, simple and fast.
> NOTE: If you don't want to deploy and maintain a Redis, you can use a [Redis Labs](https://redislabs.com/) cloud database. It's free, simple and fast.

## Docker Compose

You can use the provided ``docker-compose.yaml`` file to run EasyLogs with an external MongoDB database.

```bash
> export MONGO_INITDB_ROOT_USERNAME=root
> export MONGO_INITDB_ROOT_PASSWORD=example
> docker-compose -p easy-logs up -d
```

> NOTE: If you want to expose MongoDB & Redis ports, be sure you add the ``ports:`` section in the ``docker-compose.yaml`` file.

# How to log to EasyLogs?

EasyLogs can be used with any log source.

## Python

### Python HTTP Handler

Python has a builtin [HTTP Handler log](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.HTTPHandler) that can be used to send logs to EasyLogs:

```python
"""
This file configures a logger and sent the log to a remote HTTP server.
"""

import logging
import logging.handlers

# Get new logger
logging.basicConfig()

logger = logging.getLogger('easylogs')
logger.setLevel(logging.DEBUG)

# Configure logger to send logs to EasyLogs
easy_logs_host = "http://localhost:8080"
easy_logs_path = "/loggers/python/http-handler"
easy_logs_token = "LIh982y87GgljahsadfklJHLIUG87g1u1e7f6eb2ee145571858e8e24"

# Create HTTP handler
http_handler = logging.handlers.HTTPHandler(
    easy_logs_host,
    f'{easy_logs_path}?key={easy_logs_token}',
    method='POST',
)
logger.addHandler(http_handler)

# Send logs
logger.info('This is a test log message')

try:
    1 / 0
except Exception as e:
    logger.error('Error', exc_info=e, extra={'foo': 'bar'}, stack_info=True)
    logger.exception("asdf", e)
```

## Java (NOT IMPLEMENTED)

- [Log4j HTTP Appender](https://logging.apache.org/log4j/2.x/manual/appenders.html#HttpAppender)

> Collaboration is welcome! If you want to implement a new log source, please, open an issue.

## Go (NOT IMPLEMENTED)

- [Go HTTP Handler log](https://golang.org/pkg/log/#Handler)

> Collaboration is welcome! If you want to implement a new log source, please, open an issue.

## NodeJS (NOT IMPLEMENTED)

> Collaboration is welcome! If you want to implement a new log source, please, open an issue.


## C# (NOT IMPLEMENTED)

> Collaboration is welcome! If you want to implement a new log source, please, open an issue.

## Ruby (NOT IMPLEMENTED)

> Collaboration is welcome! If you want to implement a new log source, please, open an issue.

# Contributing

You can contribute to this project in many ways:

- Reporting bugs
- Suggesting new features
- Writing or editing documentation
- **Adding new loggers** (Python, Go, NodeJS, C#, Ruby, ...)

## Adding new loggers

Thanks for your interest in contributing to EasyLogs!

If you want to add a new logger, please, follow this steps:

1. Create a new folder under ``examples`` folder with the name of the language.
2. Create a new file with the name of the logger (e.g: ``http-handler.go``)
3. Create a README.md file with the instructions to use the logger.

Have in count that I'll need to reproduce the example to test it and add a new end-point to the API. So I'll need to execute the example.

## Adding new loggers + API

If you are here, thanks! You are awesome!

If you also know Python and want to add a new end-point to the API, please, follow this steps:

1. Copy & paste the ``easy_logs/loggers/python`` package and rename it to the name of the language.
2. Adapt the code to the new language following the same structure.

# TODO

- [ ] Improve pagination for long logs
- [ ] Add more text
- [ ] Add more languages
- [ ] Improve authentication system: add API key support, multi-user...

# License

This project is licensed under the Apache License 2.0 - see the [LICENSE](https://raw.githubusercontent.com/cr0hn/easylogs/main/LICENSE) file for details.

# Acknowledgments

This dashboard is based on [SB Admin2](https://startbootstrap.com/themes/sb-admin-2/) template.
