# diet-bot
A telegram bot that tracks your diet

## How To run tests
1. Install virtualenv using: `pip install virtualenv`
1. Create a virtualenv in source folder: `virtualenv .`
1. Activate virtualenv by: `source bin/activate`
1. Install diet-bot as package: `pip install -e .`
1. Install `nosegae` for running tests with google datastore: `pip install nosegae`
1. Run tests (it should discover all of them): `nosetests --with-gae -d`
1. Leave virtualenv by: `deactivate`
