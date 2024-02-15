## Kyle Deleyer
## Program: test 1

import random


def guess_the_number():
    # Define the range
    low = 1
    high = 100
    answer = random.randint(low, high)

    print(f"Welcome to Guess the Number! I'm thinking of a number between {low} and {high}.")

    attempts = 0
    while True:
        attempts += 1
        try:
            guess = int(input("Make your guess: "))

            if guess < low or guess > high:
                print(f"Please guess a number within the range {low} to {high}.")
                continue

            if guess < answer:
                print("Too low! Try again.")
            elif guess > answer:
                print("Too high! Try again.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
        except ValueError:
            print("Please enter a valid integer.")


guess_the_number()
