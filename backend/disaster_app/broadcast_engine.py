from threading import Thread
from datetime import datetime


class DisasterAlert:

    def __init__(self, disaster, location):

        self.disaster = disaster
        self.location = location
        self.time = datetime.now()

    def message(self):

        return (
            f"🚨 {self.disaster} Alert "
            f"for {self.location} "
            f"at {self.time.strftime('%d-%m-%Y %H:%M')}"
        )


class BroadcastEngine:

    @staticmethod
    def send(alert):

        print("Broadcast Started...")

        print(alert.message())

        print("SMS Sent")

        print("Email Sent")

        print("Notification Sent")

        print("Broadcast Completed")


def start_broadcast(disaster, location):

    alert = DisasterAlert(disaster, location)

    thread = Thread(
        target=BroadcastEngine.send,
        args=(alert,)
    )

    thread.start()