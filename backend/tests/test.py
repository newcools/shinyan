import random

lines = open('top3000japaneseword.txt').read().splitlines()
random_line = random.choice(lines)
print(random_line)