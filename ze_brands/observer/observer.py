from abc import ABC, abstractmethod
from typing import List

from apps.customuser.models import MyUser
from apps.product.models import Product
from utils.constans import BODY_EMAIL, SUBJECT_EMAIL
from utils.send_email import send_email


class Subject(ABC):
    """
    The Subject interface declares a set of methods for managing subscribers.
    """

    @abstractmethod
    def notify(self) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    _product: Product = None

    _observers: List[MyUser] = MyUser.objects.filter()

    def notify(self) -> None:
        """
        Notify each subscriber of a change in the subject.

        This method sends an email notification to each observer in the list of
        subscribers with the subject and body defined by the constants `SUBJECT_EMAIL`
        and `BODY_EMAIL`, respectively. The email is sent using the `send_email`
        function, which must be implemented elsewhere in the code.

        Raises:
            Exception: If there is an error while sending the email to any of the
                subscribers.

        """

        try:
            body = f"{BODY_EMAIL} - {str(self._product.price)}"
            for observer in self._observers:
                send_email(observer.email, body, SUBJECT_EMAIL)
        except Exception as exp:
            print(exp)

    def change_product(self, product: Product) -> None:
        self._product = product
        self.notify()
