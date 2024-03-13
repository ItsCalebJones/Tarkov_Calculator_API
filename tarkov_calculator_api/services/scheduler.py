import time

import requests

from tarkov_calculator_api.settings import settings


class TarkovItemScheduler:
    """
    A class that represents a scheduler for refreshing Tarkov item data.

    Attributes:
        url (str): The URL of the Tarkov item data API.

    Methods:
        run(): Starts the scheduler and refreshes the Tarkov item data.
    """

    def __init__(self) -> None:
        self.url = settings.hostname

    def run(self) -> None:
        """
        Starts the scheduler and refreshes the Tarkov item data at regular intervals.

        The scheduler sends a POST request to the Tarkov item data API every 10 minutes
        to refresh the data. If an error occurs during the request, the error message
        is printed to the console.

        Returns:
            None
        """
        sleep_time = 600
        while True:
            try:
                url = f"{self.url}api/refresh/"
                response = requests.post(url)
                print(f"Response: {response}")
            except requests.exceptions.RequestException as error:
                print(f"An error occurred while making the request: {error}")
            # Handle the response here
            time.sleep(sleep_time)
