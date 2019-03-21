"""UploadFiles.io data source module."""

from fileroulette.modules import BaseModule

# Set the module name based on this file's name.
MODULE_NAME = __name__.split(".")[-1]


class Module(BaseModule):
    """Define the UploadFiles.io data source module."""

    # A description of this particular module.
    description = "find files on uploadfiles.io"

    def __init__(self):
        """Initialize the UploadFiles.io data source module."""
        # Initialize the BaseModule with the module name.
        super(Module, self).__init__(MODULE_NAME)
        # Set the base url for random generation.
        self.base_url = "https://uploadfiles.io/{}"
        # Set the character types allowed in the key.
        self.allowed_chars = "a1"
        # Set the randomly-generated key length.
        self.key_length = 5
