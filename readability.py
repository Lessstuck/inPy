from cs50 import get_string


def main():
    s = get_string("Text: ")
    #  from https://www.geeksforgeeks.org/python-string-length-len
    letter_count = len(s)
    print(f"{letter_count} letters")
    # from https://www.geeksforgeeks.org/python-program-to-count-words-in-a
    word_count = len(s.split())
    print(f"{word_count} words")
    #  from https://stackoverflow.com/questions/29166774/count-number-of-sentences-in-paragraph
    sentence_count = count_sentences(s)
    print(f"{sentence_count} sentence(s)")
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
    print(f"L: {L}")
    S = (sentence_count / (word_count / 100.))
    print(f"S: {S}")
    index = (L * 0.0588) - (S * 0.296) - 15.8
    print(f"index: {index}")
    return (index)


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