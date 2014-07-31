# Flask-JSONAPI

JSON API-compliant view generators for Flask

# Installation

Clone repository and run `python setup.py install` until this reaches version 0.1.

# Usage

To use this, make sure your models already have the `JSONAPIMixin` from SQLAlchemy-JSONAPI added.  Then add the following code to your application:

```py
from flask.ext.jsonapi import FlaskJSONAPI, SQLAlchemyEndpoint

# Add the extension to your application.  You can also call init_app later
# much like most other extensions for Flask.
api = FlaskJSONAPI(app)

# Now add an endpoint for each model.
api.add_endpoint(SQLAlchemyEndpoint(User, db.session), urlprefix='/api')
```

In this example, the endpoint will be accessible at `/api/users`.
