"""Demo data source module.

This module is designed to demonstrate the layout of a data source module. It
includes only the most basic features that are required of a module, without
any additional fluff.

This module is non-functional and is not intended for actual use, but rather to
demonstrate how a data source module can be constructed.

Useful Functions
----------------
The following functions are defined in the fileroulette.libs.__init__.py file
to make it easier for you to write new modules.

self._new_url()
    Creates a new randomly-generated URL as defined by the three variables set
    in the __init__ function:
        * self.base_url
        * self.allowed_chars
        * self.key_length

"""

from fileroulette.modules import BaseModule

# Set the module name based on this file's name.
MODULE_NAME = __name__.split(".")[-1]


class Module(BaseModule):
    """Define the demo data source module.

    Note: The name of a data source Module class must always be 'Module.' This
    allows the module_loader to automatically load each module.
    """

    # A description of this particular module.
    description = "a demonstration data source"

    def __init__(self):
        """Initialize the demo data source module."""
        # Initialize the BaseModule with the module name.
        super(Module, self).__init__(MODULE_NAME)
        # Set the base url for random generation. The random key will replace
        # the brackets {} in the string.
        self.base_url = "https://example.site/files/{}"
        # Set the character types allowed in the key. This can include digits,
        # upper-case and/or lower-case letters, which will enable digits,
        # upper-case and/or lower-case letters in the randomly-generated key.
        # For example, this allowed_chars variable enables all three:
        self.allowed_chars = "aA1"
        # Set the randomly-generated key length.
        self.key_length = 5
