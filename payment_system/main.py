# Use strategy Pattern to implement payment methods
# Use chain of responsiblity to split payments

from abc import ABC, abstractmethod
from typing import List, TypedDict


class PaymentMethod(ABC):
    """Abstract class for payment strategy"""

    @abstractmethod
    def pay(self, amount):
        """Abstract method for payment"""

    def refund(self, amount):
        """Abstract method for refund"""


class CreditCardPayment(PaymentMethod):
    """Concrete class for credit card payment"""

    def __init__(self, card_number, cvv, expiration_date):
        """Constructor for credit card payment"""
        self.card_number = card_number
        self.cvv = cvv
        self.expiration_date = expiration_date

    def pay(self, amount):
        """Pay with credit card"""
        # do some stuff with the credit card info
        print(f"Pay {amount} with credit card")

    def refund(self, amount):
        """Refund with credit card"""
        # do some stuff with the credit card info
        print(f"Refund {amount} with credit card")


class PayPalPayment(PaymentMethod):
    """Concrete class for paypal payment"""

    def __init__(self, email, password):
        """Constructor for paypal payment"""
        # don't know how paypay works, don't care, for now
        self.email = email
        self.password = password

    def pay(self, amount):
        """Pay with paypal"""
        print(f"Pay {amount} with paypal")

    def refund(self, amount):
        """Refund with paypal"""
        print(f"Refund {amount} with paypal")


# What if one payment method's succeeds and others don't?
# Should the pay methods be called in parallel or in series?

class ChosenStrategy(TypedDict):
    """Type for chosen strategy"""
    method: PaymentMethod
    amount: int


class PaymentsHandler:
    """Class for handling payments"""

    def __init__(self, methods: List[ChosenStrategy]):
        """
        Constructor for payment chain

        Args:
            amount (int): amount to pay
            methods (list): list of payment methods
        """
        self.methods = methods

    @property
    def total_amount(self):
        """Total amount to pay"""
        return sum(method["amount"] for method in self.methods)

    def pay(self):
        """Pay with all payment methods"""
        for method in self.methods:
            try:
                method["method"].pay(method["amount"])
            except Exception:
                print(f"Error: {Exception}")
                print(f"Refund {method['amount']} to {method['method']}")
                method["method"].refund(method["amount"])
                raise


if __name__ == "__main__":
    # create payment methods
    credit_card = ChosenStrategy(
        amount=100,
        method=CreditCardPayment("1234 5678 9012 3456", "123", "12/24")
    )
    paypal = ChosenStrategy(
        amount=100,
        method=PayPalPayment("johndoe@gmail.com", "john123")

    )
    
    payment_handler = PaymentsHandler([credit_card, paypal])
    payment_handler.pay()


    # What's next? Parallalize the payments. No user's gonna wait for 30 seconds for all methods to finish
