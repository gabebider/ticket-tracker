# Ticket Tracker by Gabe Bider
This program will use the Twilio API to text `TO_NUMBER` whenever the lowest price of a given event changes, whether it increases or decreases. It can run indeifitely or for a certain number of iterations. It will also text `TO_NUMBER` when the maximum nunber of iterations is reached or if the program fails to fetch `self.url`.

## TODO:
Update `FROM_NUMBER` to be your number from the Twilio SMS API and update `TO_NUMBER` to be the number you wish to notify.

Ensure you have files named `account_sid.txt` and `auth_token.txt` in the same directory as `tracker.py` with the only your Twilio account SID and Twilio auth token. Alternatively, you could update the code to read in the respective environment variables with the `os` library.

Finally, simply call create a `<StubHub | SeatGeek>Tracker` object and call `<StubHub | SeatGeek>Tracker.trackPrice()`. The program defaults to checking the price once a second and running indefinitely. You can also pass in a given `delay`, the time between each check, and/or a given number of iterations, `iter`.