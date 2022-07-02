# Stubub Tracker by Gabe Bider
Update `FROM_NUMBER` to be your number from the Twilio SMS API and update `TO_NUMBER` to be the number you wish to notify.

Ensure you have files named `account_sid.txt` and `auth_token.txt` in the same directory as `tracker.py` with the only your Twilio account SID and Twilio auth token. Alternatively, you could update the code to read in the respective environment variables with the `os` library.

Finally, simple call create a `StubHubTracker` object and call `StubHubTracker.trackPrice()`. The program defaults to checking the price once and a second and running indefinitely. You can also pass in a given `delay`, the time between each check, and/or a given number of iterations, `iter`.

The program will use the Twilio API to text `TO_NUMBER` whenever the lowest price of an event changes, whether it increases or decreases. It will also text `TO_NUMBER` when the maximum nunber of iterations is reached or if the program fails to fetch `self.url`. 