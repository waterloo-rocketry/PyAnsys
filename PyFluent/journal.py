"""

This is the journal log.

Every TUI (test-user-interface) command on Fluent can be turned into a line of python code

By enabling journaling, every TUI command you type in fluent will automatically be converted and logged as
python code in this file

This is very helpful if you want to edit code or add a new feature but don't want to read/cannot understand
the pyansys and pyfluent documentations

It does however require you to know TUI commands which requires you to know what you're doing in Fluent
A handy list of TUI commands can be found here: https://www.cfdyna.com/CFDHT/FLUENT_TUI.html

To start the journal:
    1. The journal is created in the same folder as the mesh file. To keep things tidy, make sure the mesh
        is in this folder
    2.  In fluent console type:
            (api-start-python-journal "journal.py")

That's it, you do not need to edit this file or do anything else, just use the Fluent console to do whatever
your trying to achieve, and it will automatically be turned into code inside this file for you

If you end up using the journal, please refrain from committing changes to this file in git to not lose this message

"""

try:
    import ansys.fluent.core as pyfluent
    flglobals = pyfluent.setup_for_fluent(product_version="23.2.0", mode="solver", version="2d", precision="double", processor_count=1)
    globals().update(flglobals)
except Exception:
    pass
