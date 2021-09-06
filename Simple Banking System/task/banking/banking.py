# Write your code here
import random
import sqlite3


class BankSystem:
    run = 1
    db = {}
    balance = 0
    con = sqlite3.connect('card.s3db')
    cur = con.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS card '
                '(id INTEGER PRIMARY KEY , number TEXT, pin TEXT,'
                ' balance INTEGER DEFAULT 0)')

    def create_account(self):
        bin_num = str(400000)
        acc_id = str((random.randint(100000000, 999999999)))
        card_number = bin_num + acc_id
        check_sum = self.luhn(card_number)
        card_number = int(card_number + check_sum)
        pin = ''
        for i in range(4):
            if i == 0:
                k = str(random.randint(1, 9))
            else:
                k = str(random.randint(0, 9))
            pin += k
        pin = int(pin)
        self.db[card_number] = pin
        self.cur.execute('insert  into card (number, pin) values (?, ?)', (str(card_number), pin))
        self.con.commit()
        print("You card number:\n{}\n"
              "Your card PIN:\n{}".format(card_number, pin))

    def auth(self, card_num, pin_num):
        try:
            if self.db[card_num] == pin_num:
                print('You have successfully logged in!')
                count = 1
                while count != 0:
                    action = input("1. Balance\n2. Add income\n"
                                   "3. Do transfer\n4. Close account\n"
                                   "5. Log out\n0. Exit")
                    if action == '1':
                        self.cur.execute('select balance from card'
                                         ' where number = {}'.format(card_num))
                        print('Balance: {}'.format(self.cur.fetchone()))
                    elif action == '2':
                        add = int(input("Enter income:\n"))
                        self.balance += add
                        self.cur.execute('update card '
                                         'set balance = {} where number = {}'.format(self.balance, card_num))
                        self.con.commit()
                        print('Income was added!')
                    elif action == '3':
                        to_card = input("Transfer\nEnter card number:")
                        if to_card != card_num:
                            if self.luhn_auth(to_card):
                                info = self.cur.execute('SELECT * FROM card WHERE number=?', (to_card, ))
                                if info.fetchone() is not None:
                                    transfer = int(input('Enter how much money you want to transfer:'))
                                    self.cur.execute('select balance from card'
                                                     ' where number = {}'.format(card_num))
                                    balance_1 = self.cur.fetchone()
                                    if transfer <= balance_1[0]:
                                        self.cur.execute('update card '
                                                         'set balance = balance+{} where number = {}'.format(transfer, to_card))
                                        self.cur.execute('update card '
                                                         'set balance = balance-{} where number = {}'.format(transfer,
                                                                                                             card_num))
                                        self.con.commit()
                                        print('Success')
                                    else:
                                        print('Not enough money')
                                else:
                                    print('Such a card does not exist.')
                            else:
                                print('Probably you made a mistake in the card number. Please try again!')
                        else:
                            print("You can't transfer money to the same account!")
                    elif action == '4':
                        self.cur.execute('delete from card where number = {}'.format(card_num))
                        print('The account has been closed!')
                        self.con.commit()
                    elif action == '5':
                        count = 0
                        pass
                    elif action == '0':
                        count = 0
                        self.run = 0
            else:
                print('Wrong card number or PIN!')
        except KeyError:
            print('Wrong card number or PIN!')

    def running(self):
        while self.run != 0:
            action = input('1. Create an account\n2. Log into account\n0. Exit')
            if action == '1':
                self.create_account()
            elif action == '2':
                card_num = int(input('Enter your card number:'))
                pin_num = int(input('Enter your PIN:'))
                self.auth(card_num, pin_num)
            elif action == '0':
                self.run = 0
                self.con.close()

    @staticmethod
    def luhn(card):
        card = str(card)
        f = ''
        summ = 0
        checksum = 0
        for i in range(1, len(card) + 1):
            if i % 2 != 0:
                buf = int(card[i - 1]) * 2
                if buf > 9:
                    buf -= 9
                f += str(buf)
            else:
                f += card[i - 1]

        for k in f:
            summ += int(k)

        while summ % 10 != 0:
            summ += 1
            checksum += 1
        return str(checksum)

    def luhn_auth(self, card_num):
        f = ''
        summ = 0
        card_num = str(card_num)
        card = card_num[0:15]
        cheksum = card_num[15]
        for i in range(len(card)):
            if i % 2 == 0:
                k = int(card[i]) * 2
                if k > 9:
                    k -= 9
                f += str(k)
            else:
                f += card[i]
        for j in f:
            summ += int(j)

        if (summ + int(cheksum)) % 10 == 0:
            return True
        else:
            return False


session = BankSystem()
session.running()
