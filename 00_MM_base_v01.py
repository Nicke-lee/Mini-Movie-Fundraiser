import pandas
import random

# functions go here


# checks that user response is not blank
def not_blank(question):

    while True:
        response = input(question)

        # is the response is blank, output error
        if response == "":
            print("Sorry this can't be blank. Please try again")
        else:
            return response


# check user enter an integer to a given question
def num_check(question):

    while True:

        try:
            response = int(input(question))
            return response
        except ValueError:
            print("Please enter an integer. ")


# Calculate the ticket price based on the age
def calc_ticket_price(var_age):

    # ticket is $7.50 for users under 16
    if var_age < 16:
        price = 7.5

    # ticket is $10.50 for users between 16 and 64
    elif var_age < 65:
        price = 10.5

    # ticket price is $6.50 for seniors (65+)
    else:
        price = 6.5

    return price


# checks that users enter a valid response (e.g. yes / no)
# cash / credit based on a list of options
def string_checker(question, num_letters, valid_responses):

    error = "Please choose {} or {}".format(valid_responses[0],
                                            valid_responses[1])

    while True:
        response = input(question).lower()

        for item in valid_responses:
            if response == item[:num_letters] or response == item:
                return item

        print("Please enter a valid response")


# currency formatting function
def currency(x):
    return "${:.2f}".format(x)


# main routine starts here

# set maximum number of tickets below
MAX_TICKETS = 5
tickets_sold = 0

yes_no_list = ["yes", "no"]
payment_list = ["cash", "credit"]

# List to hold ticket details
all_names = []
all_ticket_cost = []
all_surcharge = []

# Dictionary used to create data frame ie: column_name:list
mini_movie_dict = {
    "Name": all_names,
    "Ticket Price": all_ticket_cost,
    "Surcharge": all_surcharge
}

# Ask user if they want to see the instructions
want_instructions = string_checker("Do you want to read the instructions? (y/n): ",
                                   1, yes_no_list)

if want_instructions == "yes":
    print("Instructions go here")

    print()

# loop to sell tickets
while tickets_sold < MAX_TICKETS:
    name = not_blank("Enter your name (or 'xxx' to quit) ")

    if name == 'xxx':
        break

    age = num_check("Age: ")

    if 12 <= age <= 120:
        pass
    elif age < 12:
        print("Sorry you are too young for this movie")
        continue
    else:
        print("?? That looks like a typo, please try again. ")
        continue

    # calculate ticket cost
    ticket_cost = calc_ticket_price(age)

    # get payment method
    pay_method = string_checker("Choose  payment method (cash / credit): ",
                                2, payment_list)

    if pay_method == "cash":
        surcharge = 0
    else:
        # calculate 5%  surcharge if users are paying by credit
        surcharge = ticket_cost * 0.05

    tickets_sold += 1

    # add ticket names, cost and surcharge to list
    all_names.append(name)
    all_ticket_cost.append(ticket_cost)
    all_surcharge.append(surcharge)

# create data frame from dictionary to organise information
mini_movie_frame = pandas.DataFrame(mini_movie_dict)
# mini_movie_frame = mini_movie_frame.set_index('Name')

# Calculate the total ticket cost (ticket + surcharge)
mini_movie_frame['Total'] = mini_movie_frame['Surcharge']\
                            + mini_movie_frame['Ticket Price']

# calculate the profit for each ticket
mini_movie_frame['Profit'] = mini_movie_frame['Ticket Price'] - 5

# calculate ticket profit totals
total = mini_movie_frame['Total'].sum()
profit = mini_movie_frame['Profit'].sum()

# Currency Formatting (users currency function)
add_dollars = ['Ticket Price', 'Surcharge', 'Total', 'Profit']
for var_item in add_dollars:
    mini_movie_frame[var_item] = mini_movie_frame[var_item].apply(currency)

# choose a winner from our name list
winner_name = random.choice(all_names)

# get position of winner name in list
win_index = all_names.index(winner_name)

# look up total amount won (ie: ticket price + surcharge)
total_won = mini_movie_frame.at[win_index, 'Total']

print("---- Ticket Data ----")
print()

# output table with ticket data
print(mini_movie_frame)

print()
print("---- Ticket Cost / Profit ----")

# output total ticket sales and profit
print("Total Ticket Sales: ${:.2f}".format(total))
print("Total Profit: ${:.2f}".format(profit))

print()
print("--------Raffle Winner---------")
print("Congratulations {}, You have won ${} ie: your "
      "ticket is free!".format(winner_name, total_won))


print()
# Output number of tickets sold
if tickets_sold == MAX_TICKETS:
    print("Congratulations you have sold all the tickets")
else:
    print("You have sold {} ticket/s. There is {} ticket/s "
          "remaining".format(tickets_sold, MAX_TICKETS - tickets_sold))
