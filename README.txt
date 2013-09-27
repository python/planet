Maintaining Planet Python (planet.python.org):

* Requests come in to the planet mailing list (planet@python.org):

  https://mail.python.org/mailman/listinfo/planet

* The feed must be checked (and usually we have to ask for a Python
  specific feed, and sometimes an English-language feed).

  Note: https feeds currently don't seem to work.

* The feed url is added to a text config file (config/config.ini),
  sorted (with ``cd config ; python sort-ini.py``) and committed to
  the website repo.

The Planet code is under the code/ directory. See code/README.pydotorg
for details.
