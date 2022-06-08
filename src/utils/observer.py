from abc import abstractmethod
from typing import Dict, List


class Event:
    def __init__(self, type_, payload):
        self.type_ = type_
        self.payload = payload


class Subscriber:
    """Class that wants to receive a message implements this"""

    @abstractmethod
    def handle_event(self, event: Event):
        """Subscriber handles event however he wants here"""
        pass


class Publisher:
    """Class that wants to publish messages to subscribers implements this"""

    def __init__(self):
        self.__subscribers: List[(Subscriber, Dict)] = []

    def add_subscriber(self, subscriber: Subscriber, events):
        """enable subscriber to receive messages"""
        self.__subscribers.append((subscriber, events))

    def broadcast(self, event):
        """Push message to all subscribers"""
        for subscriber, events in self.__subscribers:
            if event.type_ in events or len(events) == 0:
                subscriber.handle_event(event)
