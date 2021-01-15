<p align="center"><a href="https://www.verygoodsecurity.com/"><img src="https://vgs-public-image-storage.s3-us-west-2.amazonaws.com/vgs_zero_hero.png" width="512" alt="VGS Logo"></a></p>
<p align="center"><a href="https://www.verygoodsecurity.com/"><img src="https://vgs-public-image-storage.s3-us-west-2.amazonaws.com/vgs_satellite_sputnik.png" width="512" alt="VGS Logo"></a></p>
<p align="center"><b>@vgs/vgs-satellite</b><br/>VGS Offline integration/debugging application.</p>
<p align="center">
<a href="https://circleci.com/gh/verygoodsecurity/vgs-satellite/tree/master"><img src="https://circleci.com/gh/verygoodsecurity/vgs-satellite/tree/master.svg?style=svg" alt="circleci-test"></a>
</p>


<!-- toc -->
* [Description](#description)
* [How to start application](#how-to-start-application)
    * [Using the source code](#using-the-source-code)
    * [Using the Docker image](#using-the-docker-image)
    * [Using the Electron app](#using-the-electron-app)
* [Developer notes](#developer-notes)
    * [Python dependencies](#python-dependencies)
    * [Running tests](#running-tests)
    * [DB management](#db-management)
    * [Docker](#docker)
    * [Electron](#electron)
    * [Release process](#release-process)
<!-- tocstop -->

## Description

VGS Satellite is an application that can ease your integration with Very Good Security to achieve [Zero Data security](https://www.verygoodsecurity.com/#data-security-platform)

VGS Satellite provides:

    - Demo VGS Vault capabilities
    - Redact/reveal functionality
    - HTTP request/response payload transformer
    - Route configuration generator according to specific request
    - Route configuration editor
    - Logging
    - Man-in-the-middle proxy functionality (request intercept/replay/edit/etc)

This  application gives you an ability to run requests with your service and transform them into suitable VGS route configuration
without any need to sign up.

VGS Satellite's core depends on [mitmproxy](https://github.com/mitmproxy/mitmproxy/).
**mitmproxy** or man-in-the-middle proxy is an interactive intercepting proxy with ton of build-in functionalities and protocol support.
VGS Satellite is provided as a Open Source product under Apache License v2.0

## How to start application

### Using the source code

_Note: If you are not interested in contributing to VGS Satellite and don't need the latest (not released) changes please consider using the [Docker image](#using-the-docker-image) or the [Electron app](#using-the-electron-app)._

Assuming you have the right versions of Python (`3.8.*`), npm (`6.14.*`) and node (`14.15.*`):
```bash
> git clone git@github.com:verygoodsecurity/vgs-satellite.git && cd vgs-satellite
vgs-satellite> npm ci
vgs-satellite> npm run start
```

After the app is up and running you can visit `localhost:1234` to start configuring your routes.

Example request to the reverse proxy:
```bash
curl http://localhost:9098/post -H "Content-type: application/json" -d '{"foo": "bar"}'
```

Example request to the forward proxy:
```bash
curl https://httpbin.org/post -k -x localhost:9099 -H "Content-type: application/json" -d '{"foo": "bar"}'
```

#### The core app

The core of the VGS Satellite is a Python app providing 3 services:

1. Reverse proxy - use it for your inbound traffic
2. Forward proxy - use it for your outbound traffic
3. Management API which is used for routes configuration and request/response examination

The Python app can be run separately as:
```bash
vgs-satellite> python app.py
```

The core app can be configured via command line arguments, environment variables or a YAML config file. You can always get available configuration parameters invoking the app with `--help` option:
```bash
vgs-satellite> python app.py --help
Usage: app.py [OPTIONS]

Options:
  --debug                         [env:SATELLITE_DEBUG] (default:False) Debug
                                  mode.

  --web-server-port INTEGER       [env:SATELLITE_API_PORT] (default:8089) API
                                  port.

  --reverse-proxy-port INTEGER    [env:SATELLITE_REVERSE_PROXY_PORT] (default:
                                  9098) Reverse proxy port.

  --forward-proxy-port INTEGER    [env:SATELLITE_FORWARD_PROXY_PORT]
                                  (default:9099) Forward proxy port.

  --config-path FILE              [env:SATELLITE_CONFIG_PATH]
                                  (default:$HOME/.vgs-satellite/config.yml)
                                  Path to the config YAML file.

  --db-path FILE                  [env:SATELLITE_DB_PATH] (default:$HOME/.vgs-
                                  satellite/db.sqlite) Path to the DB file.

  --log-path FILE                 [env:SATELLITE_LOG_PATH] (default:None) Path
                                  to a log file.

  --silent                        [env:SATELLITE_SILENT] (default:False) Do
                                  not log into stdout.

  --volatile-aliases-ttl INTEGER  [env:VOLATILE_ALIASES_TTL] (default:3600)
                                  TTL for volatile aliases in seconds.

  --routes-path FILE              [env:SATELLITE_ROUTES_PATH] (default:None)
                                  Path to a routes config YAML file. If
                                  provided all the current  routes present in
                                  Satellite DB will be deleted.

  --help                          Show this message and exit.
```

Command line arguments take precedence over environment variables. Environment variables take precedence over the config file.

Upon the first launch VGS Satellite directory is created. By default the directory is `$HOME/.vgs-satellite` which can be changed via environment variable `SATELLITE_DIR`. By default VGS Satellite directory is used to store the DB file (where your routes are persisted) and is a default location where the app will search for the config file. Both of these paths (DB and config) can be changed via corresponding config parameters.

#### UI

VGS Satellite UI is a SPA served separately via node server (except when using the [Electron app](#electron-app)).

You can run the UI separately (assuming the core app is already started) as:
```bash
vgs-satellite> npm run serve
```

_Caveat: Although you can change the API port, UI will still try to use the default value (8089). We will fix this eventually but currently it is what it is._

### Using the Docker image
Pull the image
```bash
docker pull verygood/satellite
```

Start a container
```bash
docker run --rm -v $HOME/.vgs-satellite/:/data -p 8089:8089 -p 9098:9098 -p 9099:9099 -p 1234:1234 verygood/satellite
```

Using `docker-compose`:
```bash
vgs-satellite> docker-compose up
```

_Note: You can use any directory you like to mount `/data` volume - just make sure the directory exists before you start a container._

### Using the Electron app
VGS Satellite is available as an Electron app (for Linux and Mac). You can find the latest release versions of the app on the GitHub [releases page](https://github.com/verygoodsecurity/vgs-satellite/releases).

## Developer notes

### Python dependencies
Do not add Python dependencies directly to `requirements.txt`. Instead add them to `requirements.in` and run:
```bash
vgs-satellite> make pin_requirements
```

If you want to upgrade Python dependencies run:
```bash
vgs-satellite> make upgrade_requirements
```

### Running tests
Unit tests for the core app can be run as:
```bash
vgs-satellite> make test
```

Before submitting a PR it is worth to run
```bash
vgs-satellite> make check
```
The above command
1. Runs the linter app over Python source code (we use flake8).
2. Runs Python unit tests.
3. Builds the Python distribution (used for the Electron app).
4. Tests the Python distribution built in the previous step.

UI tests can be run as:
```bash
vgs-satellite> npm run test
```
The above command
1. Starts both the core and UI apps.
2. Runs Cypress tests.

### DB management
Routes configuration is stored in a SQLite DB. For DB migrations management we use [Alembic](https://alembic.sqlalchemy.org). Migrations are applied to the DB automatically when the core app is started.

To generate a new migration run:
```bash
vgs-satellite> PYTHONPATH=. alembic revision --autogenerate -m "Describe your changes here."
```

There is a good chance that migration generated for your model changes will not work as is due to SQLite limited nature. Usually Alembic [batch operations](https://alembic.sqlalchemy.org/en/latest/batch.html) help in such situations.

### Docker
The docker image can be built locally by running:
```bash
vgs-satellite> make docker_image
```

Publishing of the image is done via:
```bash
vgs-satellite> make docker_publish
```

### Electron
In order to ship the core as part of the Electron app we "freeze" it with [PyInstaller](https://github.com/pyinstaller/pyinstaller). To build the Python distribution run:
```bash
vgs-satellite> make dist
```

Usually PyInstaller does a good job guessing what should be included in the final distribution but sometimes some guidance is needed (see `dist` Make-target for details). It's always a good idea to test the distribution before pushing your changes:
```bash
vgs-satellite> make test_dist
```

The Electron app can be build locally by running:
```bash
vgs-satellite> npm run electron:build
```
On Mac the build process includes signing/notarizing steps which can be disabled by setting `CSC_IDENTITY_AUTO_DISCOVERY` environment variable to `false`.
```bash
vgs-satellite> CSC_IDENTITY_AUTO_DISCOVERY=false npm run electron:build
```

### Release process
Make sure `package.json` has the right `version` set - the version you're going to release. To initiate the release process run:
```
vgs-satellite> npm run release
```
This pushes a GIT-tag named after the version and triggers the release CI-job. If everything went well a draft GH-release is created and a new Docker image is pushed. Finally you can add/review release notes and publish the GH release.
