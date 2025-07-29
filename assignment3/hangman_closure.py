#Task 4: Closure Practice
def make_hangman(secret_word):
    guesses = []

    def hangman_closure(letter):
        guesses.append(letter.lower())
        display = ''.join([char if char in guesses else "_" for char in secret_word])
        print("current word:", display)

        return all(char in guesses for char in secret_word)
    return hangman_closure


if __name__ == "__main__":
    secret_word = input("Enter the secret word: ").lower()
    game = make_hangman(secret_word)

    print("\nLet's play Hangman!")
    while True:
        guess = input("Guess a letter: ").lower()
        if not guess or len(guess) != 1 or not guess.isalpha():
            print("Please enter a single alphabet letter.")
            continue

        finished = game(guess)
        if finished:
            print("Congratulations! You've guessed the word!")
            break

