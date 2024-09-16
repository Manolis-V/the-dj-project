

from fuzzywuzzy import fuzz
key, key_of_the_curr = "12A", "5A"
print("fuzzy: ", fuzz.ratio(key, key_of_the_curr)/10)