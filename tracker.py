import json
import requests
from bs4 import BeautifulSoup
import time
from twilio.rest import Client

# URL = "https://www.stubhub.com/outside-lands-music-festival-san-francisco-tickets-8-5-2022/event/105240066/"
URL = "https://www.stubhub.com/outside-lands-music-festival-san-francisco-tickets-8-5-2022/event/105239191/"
ACCOUNT_SID = open("account_sid.txt", "r").read()
AUTH_TOKEN = open("auth_token.txt", "r").read()
FROM_NUMBER = "+19897189196"
TO_NUMBER = "+16504557978"
client = Client(ACCOUNT_SID, AUTH_TOKEN)

class StubHubTracker:
    """
    A class used to update the client whenever the lowest price of a StubHub event changes
    
    ...

    Attributes
    --------
    url : str
        the URL of the event that is being tracked

    Methods
    --------
    getHtml()
        returns the HTML of `self.url`

    getSoup()
        returns a soup object using `self.getHTML()`

    findLowestPrice()
        returns the current lowest price from the event at `self.url`

    findTitle()
        returns the title of the event at `self.url`

    trackPrice(delay=1, iter=None)
        checks the price every `delay` seconds for `iter` iterations. If no `iter` is given, then loops indefinitely

    sendMessage(message)
        texts from `FROM_NUBMER` to `TO_NUMBER` the given `message`

    """
    def __init__(self, url) -> None:
        """
        Parameters
        -----
        url : str
            The url of the StubHub page to be tracked
        """
        assert type(url) is str
        self.url = url

    def getHTML(self):
        """
        Return the HTML of `self.url`

        Uses the requests module to fetch the url

        Raises
        ------
        Exception
            If unable to connect to url

        Return
        -------
        <class 'bytes'>
            object representing the HTML of `self.url`
        """
        try:
            data = requests.get(self.url)
        except Exception as e:
            print(f"\t*** ERROR: Could not connect to url: {self.url} ***")
            print(e)
            self.sendMessage("**ERROR**. Unable to reach the given URL. The program is terminating.")
            exit()

        return data.content

    def getSoup(self):
        """
        Return a soup object of self.url
        """
        html = self.getHTML()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    def findLowestPrice(self):
        """
        Finds the lowest price from `self.url`

        Uses a soup object to scrape the webpage and find the lowest price

        Returns
        ------
        float
            the lowest price of a StubHub event
        """
        soup = self.getSoup()
        data = json.loads(soup.find("script", id="index-data").text)
        lowestPrice = data['grid']['minPrice']
        return lowestPrice

    def findTitle(self):
        """"
        Finds the title of the event being tracked

        ...

        Returns 
        -------
        str
            title of the event
        """

        soup = self.getSoup()
        data = json.loads(soup.find("script", id="index-data").text)
        title = data['eventName']
        return title

    def trackPrice(self, delay=1, iter=None):
        """
        Tracks the price of the StubHub page

        Checks the price every `delay` seconds and prints the price to console.
        Runs indefinitely unless an `iter` is given in which case it runs for `iter` times

        Paramters
        ---------
        delay : float | int
            the amount of seconds to wait in between checks
        iter : float | int (optional)
            the amount of times to check the price before terminating

        Returns
        ------
        None

        """
        assert type(delay) is float or type(delay) is int
        # init lowest price
        lowestPrice = self.findLowestPrice()
        # send initial price to client
        self.sendMessage(f"The initial lowest price for {self.findTitle()} is ${lowestPrice}. Find the event here: {self.url}")
        num_checks = 0
        # case when a certain number of iterations is given
        if iter is not None:
            assert type(iter) is float or type(iter) is int
            count = 0
            while count < iter:
                updatedPrice = self.findLowestPrice()
                print(f"The lowest price is {lowestPrice} and the newest fetched price is {updatedPrice}. This is check #{num_checks}")
                if updatedPrice != lowestPrice:
                    self.sendMessage(f"The new lowest price for {self.findTitle()} is ${updatedPrice}. Find the event here: {self.url}")
                    lowestPrice = updatedPrice
                count += 1
                num_checks += 1
                time.sleep(delay)
            self.sendMessage(f"The maximum number of iterations has been reached. The last checked price was ${updatedPrice}")
        # case when no iteration limit is given
        else:
            while True:
                updatedPrice = self.findLowestPrice()
                print(f"The lowest price is {lowestPrice} and the newest fetched price is {updatedPrice}. This is check #{num_checks}")
                if updatedPrice != lowestPrice:
                    self.sendMessage(f"The new lowest price for {self.findTitle()} is ${updatedPrice}. Find the event here: {self.url}")
                    lowestPrice = updatedPrice
                num_checks += 1
                time.sleep(delay)

    def sendMessage(self, message):
        """
        Sends a SMS from `FROM_NUMBER` to `TO_NUMBER` with body `message`

        Uses the Twilio API to send a text message with a given `message`

        Paramters
        ---------
        message : str
            the body of the text message

        Returns 
        -------
        None

        """
        client.messages \
            .create(
                    body=message,
                    from_=FROM_NUMBER,
                    to=TO_NUMBER
                )
        time.sleep(1)
        # griffin
        # client.messages \
        #     .create(
        #             body=message,
        #             from_=FROM_NUMBER,
        #             to="+18478309990"
        #         )
        # time.sleep(1)
        # # mika
        message = client.messages \
            .create(
                    body=message,
                    from_=FROM_NUMBER,
                    to="+16502081201"
                )
                

if __name__ == "__main__":
    tracker = StubHubTracker(URL)
    tracker.trackPrice(10)