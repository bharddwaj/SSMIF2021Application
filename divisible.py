
import re
def divisible_helper(s,x,numbers_seen):
    '''
        Parameters: string s and integer x and set numbers_seen

        checks every possible number within s and returns those divisible by x. I added
        the numbers_seen set to skip duplicated modulus operations for better runtime.
    '''
    divisble_numbers = set({})
    for i in range(len(s)):
        num = s[i]
        # print(num)
        if num not in numbers_seen:
            numbers_seen.add(num)
            if int(num) % x == 0:
                divisble_numbers.add(int(num))

        for j in range(i+1,len(s)):
            num += s[j]
            # print(num)
            if num in numbers_seen:
                continue
            numbers_seen.add(num)
            if int(num) % x == 0:
                divisble_numbers.add(int(num))
    return divisble_numbers

def preprocessing(s,x):
    '''
        Parameters: string s and integer x

        splits the string using every letter in the alphabet and x as delimiters
        to return a list of strings that only contain numbers
    '''
    characters = '[abcdefghijklmnopqrstuvwxyz' + str(x) + ']'

    numbers = re.split(characters,s)
    return numbers
def divisible(s,x):
    '''
        Parameters: string s and non-negative integer x

        Returns a list of all of the unique numbers contained in that string that
        are divisible by non-negative integer x, but do not include integer x
        within the number itself
    '''
    if x == 0:
        # Zero case
        return []
    filtered_strings = preprocessing(s,x)
    # print(filtered_strings)
    seen_numbers = set({})
    all_divisible_numbers = set({})
    for z in filtered_strings:
        all_divisible_numbers.update(divisible_helper(z,x,seen_numbers))

    return list(all_divisible_numbers)


# print(divisible("tothemoon", 1))
# print(divisible("a465839485739b102988c30jklol4", 7))
# print(divisible("a1234567890ef", 5))
# print(divisible("1782931", 1894792))
# print(divisible("Jennychangeyournumber8675309", 0))
