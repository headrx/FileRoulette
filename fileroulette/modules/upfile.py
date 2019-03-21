"""UploadFiles.io data source module."""

from bs4 import BeautifulSoup
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

    def check_output(self, content):
        """Check the content of the page to extract useful information."""
        # Avoid files that are inaccessible or missing.
        if "Sorry it's gone..." in content or "Premium Access Only" in content:
            return False
        # Attempt to extract the file name and size from the data.
        try:
            soup = BeautifulSoup(content, "lxml")
            a, b = self._split_after(content, '<div class="details">')
            a, b = self._split_after(b, "<h3>")
            file_name, b = self._split_before(b, "</h3>")
            details_div = soup.find("div", class_="details")
            file_size = re.search("Size:(.*)", str(details_div.p)).group(0)
        except Exception as e:
            raise
        # Determine if the file exists.
        if file_name is not "None" and "" not in [file_name, file_size]:
            # If so, return its information.
            return_dict = {"File Name": file_name, "File Size": file_size}
            return return_dict
        # If this isn't a file, return False.
        return False
