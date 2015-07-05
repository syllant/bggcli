=====================================================
bggcli - Command Line Interface for BoardGameGeek.com
=====================================================

.. image:: https://travis-ci.org/syllant/bggcli.svg?branch=master
    :target: https://travis-ci.org/syllant/bggcli


.. image:: https://coveralls.io/repos/syllant/bggcli/badge.svg?branch=master
  :target: https://coveralls.io/r/syllant/bggcli?branch=master

Introduction
============


``bggcli`` is a Command Line Interface providing automation for tedious tasks on
`BoardGameGeek <http://www .boardgamegeek.com>`__ (aka BGG). It relies on the Web UI and not on the
`official API <https://www.boardgamegeek.com/wiki/page/BGG_XML_API2>`__ which doesn't offer all features available.

Only 3 operations are implemented at this time:

* bulk import/update for your game collection from a CSV file
* bulk delete from a CSV file
* bulk export as a CSV file, WITH version information (game's version is missing in the default export)

Warning:

   * Use it at your own risks, you may damage your game collection by doing mistakes! Ensure you have a backup of you
     collection first!
   * This tool is not supported by BoardGameGeek, this is an independent development
   * Be respectful regarding BGG web site: this kind of automated tools can impact performance when used
     "aggressively" (plenty of requests per second). Provided features are intended to be used for
     one-shot needs. Also they rely on a real web browser, and should conform with their
     `Terms of Services <https://www.boardgamegeek.com/terms>`__


Installation
============
Python 2.7 is required.

::

    pip install bggcli

Usage
=====
You'll need **Firefox** to be installed; Firefox will be automatically controlled by ``bggcli`` to perform operations
(through Selenium library).

Type ``bggcli`` to get the full help about available commands.

Here is an example to export a collection from an account *account1* and import it to another account *account2*::

    $ bggcli -l mylogin1 -p mypassword1 collection-export mycollection.csv
    $ bggcli -l mylogin2 -p mypassword2 collection-import mycollection.csv

Update a collection
-------------------
Here are some use cases this operation could be used for:

* Create a new account on BGG and transfer your collection: export the collection from the old account first, then use
  **bggcli** to import it
* Make a bulk update for all or some of your games: export the collection from your account first, modify details in
  the CSV file (using a text editor, OpenOffice, MS Excel, or whatever) and use ``bggcli`` to import the file

Export should be done with this tool to be complete. You can also do a manual export online, but you won't have
information about the version of each game.

Example:::

    $ bggcli -l mylogin -p mypassword collection-import mycollection.csv

Notes:

   * Column names are those exported by BGG. Any column not recognized will just be ignored
   * When a game already exists in your collection, game is updated with provided CSV values only, other fields are not
     impacted. You could only update one field for all your game.
   * Games are identified by their internal ID, named ``objectid`` in CSV file (name used by BGG). Having the
     ``objectname`` field (name of the game) is also recommended for logging.


Remove games from a collection
------------------------------
Goal is to remove from your collection all games identified in the CSV file you will provide as input.

Example:::

    $ bggcli -l mylogin -p mypassword collection-delete mycollection.csv

Notes:

  * Only the ``objectid`` column will be used for this operation: this is the internal ID managed by BGG. All other
    columns will just be ignored.

Export a collection
-------------------
Will create a CSV file with all your games, as you will do with the UI.

Example:::

    $ bggcli -l mylogin -p mypassword collection-export mycollection.csv

Notes:

  * Only the ``objectid`` column will be used for this operation: this is the internal ID managed by BGG. All other
    columns will just be ignored.


Limitations
===========

* Only *Firefox* is supported. This tools relies on Selenium to control browser, and only Firefox is supported
  out of the box by Selenium (i.e. without additional requirements). Support of additional browsers could be introduced,
  but I'm not sure it's worth it.
* Performance: Selenium+Firefox association is not the fastest way to automate operations, but it's
  probably the best regarding stability (no Javascript emulation, Firefox does the work) and simplicity (no need to
  install anything else), which is the most important in the current context. On my laptop, I see the import taking
  1 min for 5 games.
* Some fields related to the game's version are not exported by BGG: the ``barcode`` and the `language``. Note
  although this only applies to custom version you define yourself, which should be quite rare.


Ideas for future versions
=========================

Here are some ideas of additional tasks that could be implemented:

* Generic import for collections, based on game names and not on the BGG internal identifier. A confirmation would be
  required for each ambiguous name to choose among matching games provided by BGG
* Update/Delete for plays
* Update/Delete for forum subscriptions

Links
=====

* *BoardGameGeek*: http://www.boardgamegeek.com
* *Officiel XML API 2*: https://www.boardgamegeek.com/wiki/page/BGG_XML_API2
* *boardgamegeek - A Python API for boardgamegeek.com*: https://github.com/lcosmin/boardgamegeek

Final note
==========

Does it really deserve such a development? Probably not, but my second goal was to discover the Python ecosystem!