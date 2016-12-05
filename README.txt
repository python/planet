Maintaining Planet Python (planetpython.org):

* Requests come in to the github issues (https://github.com/python/planet/issues) 
  or planet mailing list (planet at python.org):

  https://mail.python.org/mailman/listinfo/planet
  
* Check the feed for validity using the services: http://feedvalidator.org/ or https://validator.w3.org/feed/ or http://www.rssboard.org/rss-validator/

* Check the feed for: Python-specific contents (often we
  have to ask for a Python specific feed), and English-language
  content (ask for an English-language feed).

* Add the feed URL to a text config file (config/config.ini)::

      [http://example.org/feed/url/]
      name = Author/Group/Project Name

  Sort the config file::

      cd config
      python sort-ini.py

  Commit the config file to the repo.

The Planet code is under the code/ directory. See code/README.pydotorg
for details.
