import unittest
from datetime import datetime

from quickbooks.objects.account import Account
from quickbooks.objects.bill import Bill
from quickbooks.objects.billpayment import BillPayment, BillPaymentLine, CheckPayment
from quickbooks.objects.vendor import Vendor


class BillPaymentTest(unittest.TestCase):
    def setUp(self):

        self.account_number = datetime.now().strftime('%d%H%M')
        self.name = "Test Account {0}".format(self.account_number)

    def test_create(self):
        bill_payment = BillPayment()

        bill_payment.PayType = "Check"
        bill_payment.TotalAmt = 200
        bill_payment.PrivateNote = "Private Note"

        vendor = Vendor.all(max_results=1)[0]
        bill_payment.VendorRef = vendor.to_ref()

        bill_payment.CheckPayment = CheckPayment()
        account = Account.where("AccountSubType = 'Checking'")[0]
        bill_payment.CheckPayment.BankAccountRef = account.to_ref()

        ap_account = Account.where("AccountSubType = 'AccountsPayable'")[0]
        bill_payment.APAccountRef = ap_account.to_ref()

        bill = Bill.all(max_results=1)[0]

        line = BillPaymentLine()
        line.LinkedTxn.append(bill.to_linked_txn())
        line.Amount = 200

        bill_payment.Line.append(line)
        bill_payment.save()

        query_bill_payment = BillPayment.get(bill_payment.Id)

        self.assertEquals(query_bill_payment.PayType, "Check")
        self.assertEquals(query_bill_payment.TotalAmt, 200.0)
        self.assertEquals(query_bill_payment.PrivateNote,"Private Note")

        self.assertEquals(len(query_bill_payment.Line), 1)
        self.assertEquals(query_bill_payment.Line[0].Amount, 200.0)
