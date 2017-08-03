ows-timed-release
=====================================

## Getting Started

### Installation

The installation is very straightforward, but make sure you are using at least
python 3.4. If you use a Mac, you can install it using `brew`. If you use
Windows, just ask for a remote VM that has it installed for you.

```bash
$ cd ows-timed-release
$ pyvenv env
(env) $ . env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ pip install -r requirements-dev.txt
```

### Configuration

Copy .env.shadow to .env and add the appropriate environement variables for your environment.

`cp .env.shadow .env`

Then, set your environment:
```bash
source .env
```

### Permissions

In PROD and QA environments, to accept and authorize incoming and outgoing
requests, make sure you have the right DynamoDB permissions, as highlighted
in the corresponding [tech design](https://docs.google.com/document/d/1eHoI_BddTFMi15yCaHS6KvhSSoTrMEd3WwJINIpgNpM/edit).

### Running

When all dependencies have been installed, you can run the flask application
on your local instance by running:

```bash
(env) $ python dev.py
```

or

```bash
make dev
```

By using the development server, you will have access to specific features that
are not necessarily available in production, such as the exception tracer.

### Testing

To run the tests, all you have to do is to run:

```bash
(env) $ py.test tests/ --cov timed_release --cov-report term-missing
(env) $ flake8 timed_release/ tests/
```

or

To run tests: `make test`

To lint: `make lint`

### Updating

To install new dependencies.

```bash
(env) $ pip install -r requirements.txt
(env) $ pip install -r requirements-dev.txt
```

or

```bash
make pip_dev
```
