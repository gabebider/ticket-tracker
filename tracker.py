import json
from pprint import pprint
from tokenize import String
import requests
from bs4 import BeautifulSoup
import time
from twilio.rest import Client

URL = "https://www.stubhub.com/outside-lands-music-festival-san-francisco-tickets-8-5-2022/event/105240066/"
ACCOUNT_SID = open("account_sid.txt", "r").read()
AUTH_TOKEN = open("auth_token.txt", "r").read()
FROM_NUMBER = "+19897189196"
TO_NUMBER = "+16504557978"
client = Client(ACCOUNT_SID, AUTH_TOKEN)

class StubHubTracker:
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
        Return the HTML of self.url

        Uses the requests module to fetch the url
        """
        data = requests.get(self.url)
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
        Finds the lowest price from self.url

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
        soup = self.getSoup()
        title = soup.title.text
        return title[0 : title.find(" - ")]

    def trackPrice(self, delay, iter=None):
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
        lowestPrice = self.findLowestPrice()
        if iter is not None:
            assert type(iter) is float or type(iter) is int
            count = 0
            while count < iter:
                updatedPrice = self.findLowestPrice()
                if updatedPrice != lowestPrice:
                    self.sendMessage(f"The new lowest price is ${updatedPrice}")
                    lowestPrice = updatedPrice
                count += 1
                time.sleep(delay)
        else:
            while True:
                updatedPrice = self.findLowestPrice()
                if updatedPrice != lowestPrice:
                    self.sendMessage(f"The new lowest price for {self.findTitle()} is ${updatedPrice}")
                    lowestPrice = updatedPrice
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
        message = client.messages \
            .create(
                    body=message,
                    from_=FROM_NUMBER,
                    to=TO_NUMBER
                )
                

if __name__ == "__main__":
    tracker = StubHubTracker(URL)
    tracker.trackPrice(0.5)