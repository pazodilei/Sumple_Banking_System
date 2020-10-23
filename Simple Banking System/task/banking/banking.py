import random
import sqlite3
conn = sqlite3.connect('card.s3db')

cur = conn.cursor()
cur.execute("DROP TABLE card;")
cur.execute('''CREATE TABLE card(
id INTEGER,
number TEXT,
pin TEXT,
balance INTEGER DEFAULT 0
);''')
conn.commit()
_id = 0


def security_chek(number, pin='0000'):
    cur.execute(f"SELECT number, pin FROM card WHERE number = {number} AND pin = {pin};")
    if cur.fetchone():
        print('You have successfully logged in!\n')
        conn.commit()
        return True
    print('Wrong card number or PIN!\n')
    return False


def set_new_card():
    card_number = '400000' + ''.join([str(x) for x in random.sample(range(0, 10), 9)])
    check_sum = 0
    for i in range(len(card_number)):
        minus = int(card_number[i])
        if (i % 2) == 0 or i == 0:
            minus *= 2
            if minus > 9:
                minus = minus - 9
        check_sum += minus
    check_sum = abs(10 - check_sum % 10) if (check_sum % 10) else 0
    card_number += str(check_sum)
    cur.execute(f"SELECT number FROM card WHERE number = {card_number};")
    if cur.fetchone():
        return set_new_card()
    pin = ''.join([str(x) for x in random.sample(range(0, 10), 4)])
    return card_number, pin


def menu(_id):
    while True:
        choice = input('1. Create an account\n'
                       '2. Log into account\n'
                       '0. Exit\n')
        print()
        if choice == '1':
            card_number, pin = set_new_card()
            print(f'Your card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}\n')
            _id += 1
            cur.execute(f"INSERT INTO card (id, number, pin) "
                        f"VALUES ({_id}, {card_number}, {pin});")
            conn.commit()
        elif choice == '2':
            card_number = input('Enter your card number:\n')
            pin = input('Enter your PIN:\n')
            print()
            if security_chek(card_number, pin):
                while True:
                    choice = input('1. Balance\n'
                                   '2. Add income\n'
                                   '3. Do transfer\n'
                                   '4. Close account\n'
                                   '5. Log out\n'
                                   '0. Exit\n')
                    print()
                    if choice == '1':
                        cur.execute(f"SELECT balance FROM card WHERE number = {card_number}")
                        print(f'Balance: {cur.fetchone()[0]}\n')
                    elif choice == '2':
                        cur.execute(f"UPDATE card SET balance=balance+{int(input('Enter income:'))} "
                                    f"WHERE number={card_number}")
                        conn.commit()
                    elif choice == '3':
                        number_to_transfer = input('Enter card number:')
                        cur.execute(f"SELECT number FROM card "
                                    f"WHERE number={number_to_transfer};")
                        number = cur.fetchone()
                        if number is None:
                            print('Probably you made a mistake in the card number. Please try again!\n')
                            print("Such a card does not exist.")
                        else:
                            transfer = int(input("Enter how much money you want to transfer:"))
                            cur.execute(f"SELECT balance FROM card "
                                        f"WHERE number = {card_number}")
                            balance = cur.fetchone()[0]
                            if transfer > balance:
                                print("Not enough money")
                            else:
                                cur.execute(f"UPDATE card SET balance=balance+{transfer} "
                                            f"WHERE number={number_to_transfer}")
                                cur.execute(f"UPDATE card SET balance=balance-{transfer} "
                                            f"WHERE number={card_number}")
                                conn.commit()
                    elif choice == '4':
                        cur.execute(f"DELETE FROM card "
                                    f"WHERE number={card_number}")
                        conn.commit()
                        print("\nThe account has been closed!\n")
                    elif choice == '5':
                        print('You have successfully logged out!\n')
                        break
                    elif choice == '0':
                        print('\nBye!')
                        return
        if choice == '0':
            print('\nBye!')
            return


menu(_id)
