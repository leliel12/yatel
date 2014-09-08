CHANGELOG
=========

0.3.5
-----

- the ``test`` command now support the parameter ``--filefast``
- Create an infraestructure for testing various database engines by setting the
  enviroment variable ``YATEL_TEST_DBS``.
- Now the only way to create ``db.YatelNetwork`` instances are with
  uri connection string to database according to the RFC 1738 spec.
- Now if you want t create in memory database the uri is ``sqlite:///``
- Removed ``list`` command
- added this changelog.
