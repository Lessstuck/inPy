from cs50 import get_string


def main():
    s = get_string("Text: ")
    #  from https://www.geeksforgeeks.org/python-string-length-len
    letter_count = count_letters(s)
    # from https://www.geeksforgeeks.org/python-program-to-count-words-in-a
    word_count = len(s.split())
    #  from https://stackoverflow.com/questions/29166774/count-number-of-sentences-in-paragraph
    sentence_count = count_sentences(s)
    index = coleman_liau(letter_count, word_count, sentence_count)
    # print messages for different index values
    if (index < 1):
        print("Before Grade 1")
    elif (index >= 16):
        print("Grade 16+")
    else:
        print(f"Grade {index}")

# calculte Coleman-Liau Index


def coleman_liau(letter_count, word_count, sentence_count):
    L = (letter_count / (word_count / 100.))
    S = (sentence_count / (word_count / 100.))
    index = round((L * 0.0588) - (S * 0.296) - 15.8)
    return (index)


# counts letters in string
def count_letters(s):
    i = 0
    letters = 0
    while True:
        #  count upper-case letters
        if (ord(s[i]) >= 65 and ord(s[i]) <= 90):
            letters += 1
        # count lower-case letters
        elif (ord(s[i]) >= 97 and ord(s[i]) <= 122):
            letters += 1
        i += 1
        if (i == len(s)):
            break
    return letters


#  counts periods, question marks, and exclamation marks
def count_sentences(s):
    sentence_endings = 0
    i = 0
    while True:
        # counting periods, exclamation marks, and question marks
        # if (('.' in s) or ('!' in s) or ('?' in s)):
        if ((s[i] == '.') or (s[i] == '!') or (s[i] == '?')):
            sentence_endings += 1
        i += 1
        if (i == len(s)):
            break
    return(sentence_endings)


main()