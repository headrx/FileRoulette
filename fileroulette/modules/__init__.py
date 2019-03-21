"""FileRoulette Module Library.

This library defines the BaseModule template, from which new data source
modules can be derived. To learn more about making a new data source module,
see the demo.py module.
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

# The following dictionary contains dicts of HTTP status codes that would
# signal some kind of problem with our request. If any of these codes should
# warrant a rejection of the URL without user notification, move them to the
# "rejected" dict.
STATUS_CODES = {
    "rejected": {400: "Bad Request", 404: "Not Found", 410: "Gone"},
    "forbidden": {401: "Unauthorized", 403: "Forbidden"},
    "unexpected": {
        405: "Method Not Allowed",
        406: "Not Acceptable",
        418: "I'm a Teapot!",
        420: "Enhance Your Calm",
    },
    "error": {
        408: "Request Timeout",
        421: "Misdirected Request",
        423: "Locked",
        429: "Too Many Requests",
        496: "SSL Certificate Required",
        500: "Internal Server Error",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        509: "Bandwidth Limit Exceeded",
    },
    "cloudflare": {
        520: "Unknown Error (Cloudflare)",
        521: "Website is Down (Cloudflare)",
        522: "Connection Timed Out (Cloudflare)",
        523: "Origin is Unreachable (Cloudflare)",
        524: "A Timeout Occurred (Cloudflare)",
        525: "SSL Handshake Failed (Cloudflare)",
        527: "Railgun Error (Cloudflare)",
        530: "Origin DNS Error (Cloudflare)",
    },
}


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

    def _get_page_content(self, session, url):
        """Retrieve the HTML content for the specified URL.

        Parameters
        ----------
        session
            The session with which we will retrieve the URL.
        url
            The URL we will be retrieving.

        Returns
        -------
        content or False
            This function returns False if the content could not be loaded,
            otherwise it will return the text content of the retrieved page.

        """
        # Retrieve the page's header.
        (header, url) = self._get_page_header(session, url)
        if header.status_code == 200:
            # The request was a success. Return the text of the site.
            return session.get(url).content.decode()
        # Check for alternate status codes.
        if header.status_code in STATUS_CODES["rejected"]:
            # The URL is invalid or unavailable.
            return False
        for _, codes in STATUS_CODES.items():
            # There's an unexpected status code.
            if header.status_code in codes.keys():
                # Print out the status code information.
                print(
                    "{}: {} ({})".format(
                        header.status_code, codes[header.status_code], url
                    )
                )
                return False
        # We've encountered an unknown status code.
        print("{}: Unknown ({})".format(header.status_code, url))
        return False

    @staticmethod
    def _get_page_header(session, url):
        """Retrieve the HTTP header for the specified URL.

        Parameters
        ----------
        session
            The session with which we will retrieve the URL.
        url
            The URL we will be retrieving.

        Returns
        -------
        header
            The HTTP result header returned from the target site.
        url
            The URL of the page. If the header redirects to another URL, it
            will return the target URL. Otherwise, it will return the original.

        """
        header = session.head(url)
        if header.is_redirect:
            # If we're being redirected, grab the headers for the target URL.
            url = header.headers["Location"]
            header = session.head(url)
        return (header, url)

    def _new_url(self):
        """Generate a new random URL.

        Returns
        -------
        str
            A randomly-generated URL which follows the specified constraints.

        """
        return urlgen(self.base_url, self.allowed_chars, self.key_length)

    def check_output(self, content):
        """Check the content of the page to extract useful information.

        This function needs to be defined in each individual module, as this is
        the method which determines if the page contains data we wish to save,
        such as a live file or useful text.

        Parameters
        ----------
        content : str
            The content returned by the server, typically text or HTML.

        Returns
        -------
        dict or False
            If the content is useful, return a dict containing the useful info
            (such as file names and sizes). This information will be either
            printed to the screen or saved in a file, depending on the user's
            preference. If there is no good data, return False to continue
            scanning.

        """
        pass

    def run(self):
        """Start the module's main loop."""
        print("Running {} module...".format(self.name))
