'''
    Program Name: TradeMe.py
    Version: 1.0
    Author: Matthew Hartstonge | Mykro Enterprises New Zealand Limited
    Date Written: 23/02/2014
    Modified: 28/02/2014
    Description:
        Provides a way to calculate the TradeMe listing price based on the price
        wanted for a general item listing

    ----------------------------------------------------------------------------
    Version 1.0
    + Correctly calculates fees and the price to list them at for all fee
      brackets including PayPal

    ----------------------------------------------------------------------------
    Version 0.1
    + Enables finding the listing price for a general item on TradeMe
    + Enables finding the listing price for an item on PayPal Merchant fees
    - Fees for TradeMe mid/high listing price not calculating correctly

'''


class CalcFee(object):

    def __init__(self, price_wanted):
        # TradeMe Default Fees
        # Base success fee
        self.min_fee = 0.50

        # Up to $200 | 7.9% of sale price (50c minimum)
        self.low_range = 200
        self.low_fee = 0.079

        # $200 - $1500 | $15.80 + 4.9% of sale price over $200
        self.mid_range = 1500
        self.mid_base_charge = 15.80
        self.mid_fee = 0.049

        # Over $1500 | $79.50 + 1.9% of sale price over $1500 (max fee = $149)
        self.high_base_charge = 79.50
        self.high_fee = 0.019
        self.max_fee = 149

        # PayNow fee
        self.pay_now_fee = 0.0195

        # PayPal Merchant Fee
        self.base_web_fee = 0.45
        self.web_fee = 0.0345

        self.fee_charged = ''
        self.price_wanted = price_wanted
        self.trademe_list_price = 0.0
        self.paynow_list_price = 0.0
        self.web_list_price = 0.0
        self.success_fee = 0.0
        self.paynow_success_fee = 0.0
        self.total_success_fees = 0.0



    def calc_base_fee(self):
        '''
            Calculates the list price based on price wanted + base fee
            Base Fee being the minimum success fee you have to pay TradeMe
        '''

        self.trademe_list_price = self.price_wanted + self.min_fee
        self.success_fee = self.min_fee
        self.paynow_list_price = self.trademe_list_price / (1 - self.pay_now_fee)


    def calc_low_fee(self):
        '''
            Calculates the list price based on price wanted - fees on lowest
            TradeMe fee bracket
        '''

        self.trademe_list_price = self.price_wanted / (1 - self.low_fee)
        self.success_fee = self.trademe_list_price * self.low_fee

        if self.success_fee <= self.min_fee:
            self.trademe_list_price = (self.trademe_list_price - self.success_fee) + self.min_fee
            self.success_fee = self.min_fee


    def calc_mid_fee(self):
        '''
            Calculates the list price based on price wanted - fees on lowest
            TradeMe fee bracket
        '''
        # List price is 4.9% charged on top of $200 with a base fee of $15.80

        # Work out price including base fee
        self.trademe_list_price = self.price_wanted + self.mid_base_charge
        # Add success fee on top of price
        self.trademe_list_price = self.low_range + ((self.trademe_list_price - self.low_range) / (1 - self.mid_fee))
        self.success_fee = self.mid_base_charge + ((self.trademe_list_price - self.low_range) * self.mid_fee)


    def calc_high_fee(self):
        '''
            Calculates the list price based on price wanted - fees on lowest
            TradeMe fee bracket
        '''
        # Over $1500 | $79.50 + 1.9% of sale price over $1500 (max fee = $149)

        # Work out price including base fee
        self.trademe_list_price = self.price_wanted + self.high_base_charge
        # Add success fee on top of price
        self.trademe_list_price = self.mid_range + ((self.trademe_list_price - self.mid_range) / (1 - self.high_fee))
        self.success_fee = self.high_base_charge + ((self.trademe_list_price - self.high_base_charge) * self.high_fee)

        # If the success fee works out to be greater than high_base_charge
        # ($149), minus the success fee and then add the high_base_charge ($149)
        if self.success_fee >= self.max_fee:
            self.trademe_list_price = (self.trademe_list_price - self.success_fee) + self.max_fee
            self.success_fee = self.max_fee


    def calc_web_fee(self):
        '''
            Calculates a liting price based on PayPal Merchant Fees
        '''
        # work out the Web list price based on PayPal Merchant Fees
        self.web_list_price = (self.price_wanted / (1 - self.web_fee)) + self.base_web_fee


    def calc_paynow_fee(self):
        '''
            Calculates the fee PayNow charges on top of the sale
        '''
        # Work out the Listing price if including PayNow
        self.paynow_list_price = self.trademe_list_price / (1 - self.pay_now_fee)
        self.paynow_success_fee = self.paynow_list_price - self.trademe_list_price


    def calc_total_success_fees(self):
        '''
            Total Fee = Success Fee + PayNow Fee
        '''
        self.total_success_fees = self.success_fee + self.paynow_success_fee

    def calculate_general_fee(self):
        '''
            Decides which bracket the fee will be based on price wanted
        '''


        if self.price_wanted < (self.low_range * (1 - self.low_fee)):
            self.calc_low_fee()
            self.fee_charged = 'Low Fee'

        elif self.price_wanted < (self.mid_range * (1 - self.mid_fee)):
            self.calc_mid_fee()
            self.fee_charged = 'Medium fee'

        else:
            self.calc_high_fee()
            self.fee_charged = 'High fee'

        self.calc_paynow_fee()
        self.calc_total_success_fees()
        self.calc_web_fee()

trademe = CalcFee(float(input('Please enter the price wanted for a general item on TradeMe: $')))
trademe.calculate_general_fee()

print("You will be put on the '{}' structure".format(trademe.fee_charged))
print('TradeMe List Price: {0:>20.2f}'.format(trademe.trademe_list_price))
print('PayNow List Price: {0:>21.2f}'.format(trademe.paynow_list_price))
print('Web List Price: {0:>24.2f}'.format(trademe.web_list_price))
print('TradeMe Success Fee: {0:>19.2f}'.format(trademe.success_fee))
print('TradeMe PayNow Fee: {0:>20.2f}'.format(trademe.paynow_success_fee))
print('TradeMe Total Fees: {0:>20.2f}'.format(trademe.total_success_fees))
