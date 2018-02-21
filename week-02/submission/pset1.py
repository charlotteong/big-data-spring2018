## A. LISTS
## A1. Create a list containing 4 strings
l_4string = ["this is a string", "and another", "stringing along", "high strung"]
## A2. Print 3rd item in the list
print(l_4string[2])
## A3. Print 1st and 2nd item using index slicing
print(l_4string[0:2])
## A4. add a new string with text 'last' and print the list
l_4string.append("last")
print(l_4string)
## A5. get the list length and print it
print(len(l_4string))
## A6. replace the last item in the list with the string 'new'
l_4string.pop()
l_4string.append("new")
print(l_4string)


## B. STRINGS
## B1. convert list into normal sentence
sentence_words = ['I', 'am', 'learning', 'Python', 'to', 'munge', 'large', 'datasets', 'and', 'visualize', 'them']
print(' '.join(sentence_words))
## credit: http://www.java2s.com/Tutorial/Python/0100__String/JoiningStrings.htm
##B2. reverse order of the list
sentence_words.reverse()
print(sentence_words)
## B3: sort the list
sentence_words.sort()
print(sentence_words)
## B4. use sorted function
new_sort_list = sorted(sentence_words)
print(new_sort_list)
## sorted() returns a new sorted list and leaves the original list intact.
## .sort function sorts the list in place and directly changes the order of the elements in the list.

## B5. Modify the sort to do a case insensitive alphabetical sort
sentence_words.sort(key=lambda x: x.lower())
print(sentence_words)
## code adopted from Soner Gönül on https://stackoverflow.com/questions/10269701/case-insensitive-list-sorting-without-lowercasing-the-result


## C. Random Function

## original function:
from random import randint
# this returns random integer: 100 <= number <= 1000
num = randint(100, 1000)
num

max = 500
def newrandint(max,min=0):
    return randint(min, max)

assert(0 <= newrandint(100, min = 0) <= 500)


## D. String Formatting Function
def winnerbook():
    n = int(input("Enter a number: "))
    book = str(input("Enter a title: ")).title()
    print(f"The number {n} bestseller today is: {book}.")
winnerbook()


## E. Password Validation Function
def password_test():
    SpecialSym = ['!', '?', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=']
    password = str(input("Type your password here: "))
    returnval = True
    if len(password) < 8:
        print("The password needs to be between 8-14 char long.")
        returnval = False
        ## test if length of password is less than 8 char
    if len(password) > 14:
        print("The password needs to be between 8-14 char long.")
        returnval = False
        ## test if length of password is more than 14 char
    if sum(char.isdigit() for char in password) < 2:
        print("The password needs to have at least 2 digits.")
        returnval = False
        ## test if no. of digits in password is less than 2
    if not any(char in SpecialSym for char in password):
        print("The password needs at least one special symbol.")
        returnval = False
        ## test if there are any special symbols as defined in password
    if not any (char.isupper() for char in password):
        print("The password needs at least one uppercase letter.")
        returnval = False
        ## test if there are any uppercase characters in password
    if returnval:
        print("SUCCESS!")

password_test()


## Code adapted from Oscar Lopez (https://stackoverflow.com/questions/24878174/how-to-count-digits-letters-spaces-for-a-string-in-python)
## and from srinivasu u (https://stackoverflow.com/questions/41117733/validation-a-password-python)"""


## F. Exponentiation Function

def exp(x, y):
    if(y == 1):
        return(x)
    ## if exponent = 1, returns the base
    if(y!=1):
        return(x*exp(x,y-1))
    print(exp(x,y))
exp(2, 3)
exp(5, 4)
exp(2, 1)

## code adapted from sanfoundry (http://www.sanfoundry.com/python-program-find-power-number-recursion/)


## G. Extra credit
def mymin(list1):
    minz = list1[0]
    for i in list1:
        if i < minz:
            minz = i
    return minz

h = [4, 20, 3, 4, 2, 10, 30, 10]
mymin(h)

def mymax(list2):
    maxx = list2[0]
    for i in list2:
        if i > maxx:
            maxx = i
    return maxx
mymax(h)

## code adopted from Martijn Pieters from (https://stackoverflow.com/questions/30313149/minimum-in-python-without-using-min-function-python-2-7)

""" test code below
HELLO = [12,3,4,5,9]
minimum = HELLO[0]
for number in HELLO:
    if minimum > number:
        minimum = number
print(minimum)
"""
