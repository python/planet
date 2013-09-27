Maintaining Planet Python (planet.python.org):

* Requests come in to the planet mailing list (planet@python.org):

  https://mail.python.org/mailman/listinfo/planet

* Check the feed for: validity, Python-specific contents (often we
  have to ask for a Python specific feed), and English-language
  content (ask for an English-language feed).

  Note: https feeds currently don't seem to work.

* Add the feed URL to a text config file (config/config.ini)::

      [http://example.org/feed/url/]
      name = Author/Group/Project Name

  Sort the config file::

      cd config
      python sort-ini.py

  Commit the config file to the website repo. Prefix commit messages
  with "(Planet Python) ".

The Planet code is under the code/ directory. See code/README.pydotorg
for details.
