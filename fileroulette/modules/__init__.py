"""FileRoulette Module Library.

This library defines the BaseModule template, from which new data source
modules can be derived.

Contents
--------
__init__.py
    Contains the module foundation, from which all other modules are derived.
demo.py
    A demonstration module that exists to show, simply, how a data source
    module can be constructed. (This module is non-functional.)
"""

import random
import requests

from fileroulette.libs import urlgen

# Just to prevent some SSL errors. This may not be necessary.
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += (
#     ":ECDHE-ECDSA-AES128-GCM-SHA256"
# )

# A list of user agents, in case we wish to pick at random.
AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
    "like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like "
    "Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like "
    "Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14931",
    "Chrome (AppleWebKit/537.1; Chrome50.0; Windows NT 6.3) "
    "AppleWebKit/537.36 (KHTML like Gecko) Chrome/51.0.2704.79 Safari/537.36 "
    "Edge/14.14393",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML like "
    "Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.9200",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML like "
    "Gecko) Chrome/46.0.2486.0 Safari/537.36 Edge/13.10586",
    "Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) Gecko/20100101 Firefox/64.0",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.10; rv:62.0) Gecko/20100101 "
    "Firefox/62.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:10.0) Gecko/20100101 "
    "Firefox/62.0",
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, "
    "like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ "
    "(KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, "
    "like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) "
    "AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
]
# Default to the Tor Browser user agent.
DEF_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0"

# ---[ BASE MODULE DEFINITION ]--- #


class BaseModule:
    """Define the core structures common to all data source modules."""

    # The allowed_chars defines what kinds of characters can be used in the
    # randomly-generated key.
    allowed_chars = str()
    # The base_url defines the URL used by urlgen to create random URLs.
    base_url = str()
    # The key_length defines how long the randomly-generated key should be.
    key_length = int()
    # Decide whether to use a randomized user agent for every request.
    random_agent = False

    def __init__(self, module_name):
        """Initialize the module.

        Parameters
        ----------
        module_name : str
            The name of the module that derived from this BaseModule class.

        """
        self.name = module_name
        print("Initializing {} module...".format(self.name))

    def _create_new_session(self):
        """Create a new requests session.

        Returns
        -------
        session
            A new instance of requests.sessions.Session with the qualities
            specified by the user's requirements.

        """
        session = requests.Session()
        if self.random_agent:
            # Choose a random agent from the AGENTS list.
            session.headers.update({"User-Agent": random.choice(AGENTS)})
        else:
            # Default to the Tor Browser user agent.
            session.headers.update({"User-Agent": DEF_AGENT})
        return session

    def _new_url(self) -> str:
        """Generate a new random URL.

        Returns
        -------
        str
            A randomly-generated URL which follows the specified constraints.

        """
        return urlgen(self.base_url, self.allowed_chars, self.key_length)

    def run(self):
        """Start the module's main loop."""
        print("Running {} module...".format(self.name))
