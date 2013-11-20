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


Sysadmin Notes
==============

Some notes from Martin von Lowis on adding new users to the website repo, 
needed for commit access to the Planet:

Here is what I know about the pydotorg repository on dinsdale; feel
free to circulate/extend.

A. Repositories:
  Data: svn+ssh://pydotorg@svn.python.org/trunk/beta.python.org
  Keys:
https://svn.python.org/systems/dinsdale/data/repos/pydotorg/sshkeys

B. Giving access:
  Data: 1. add user's ssh key to file first.last to keys repository,
           svn commit
        2. log into root@dinsdale, sudo pydotorg
        3. (cd keys; svn up)
        4. ./make_authorized_keys pydotorg www

  Keys: 1. Add admin user to /etc/apache2/svn.users
           (e.g. with htpasswd)
        2. Add admin user to group admins in
           /etc/apache2/svn.access
        3. apache2ctl graceful

C. Location of repositories:
  /data/repos/{www,systems,packages,...}

D. Building the website
  User amk has crontab entries:
  # for updating the site, to be run every minute
  /data/website-build/build/scripts/post-commit-svnup-binary
  # for updating the PEPs repository
  /data/website-build/build/scripts/pollhg
  # several other cronjobs

  website-build needs to be owned by amk

  www repository has post-commit hook, which is
  a setuid-amk binary
  /data/repos/www/hooks/update-web-wrapper

  As a consequence, each commit should result in a website
  rebuild every minute. Build logs are at

  http://www.python.org/status/


E. Deploying the site
  Life site is at /data/ftp.python.org/pub/www.python.org/

  In addition to the actual data installed by a checkout,
  many files (in particular in ftp/python) are directly
  copied into the life site, and not version-controlled.

