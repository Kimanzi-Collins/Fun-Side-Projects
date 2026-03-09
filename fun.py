import random

x = random.randint(1, 100)
y = random.randint(1, 100)

print("Welcome to the random math game! You will be given two random numbers between 1 and 100, and you have to guess the answer to their operation.")
print(f"Are you ready?")
input("Press Enter to continue...")
while(1):
    if random.choice([True, False]):
        print(f"What is {x} + {y}?")
        answer = int(input("Your answer: "))
        if answer == x + y:
            print("Correct! Well done!")
        else:
            print(f"Wrong! The correct answer is {x + y}.")
    else:
        print(f"What is {x} * {y}?")
        answer = int(input("Your answer: "))
        if answer == x * y:
            print("Correct! Well done!")
        else:
            print(f"Wrong! The correct answer is {x * y}.")
    print("Do you want to play again? (yes/no)")
    play_again = input().lower()
    if play_again != "yes":
        break