from .exceptions import *
import random as rand

class GuessAttempt(object):
    def __init__(self, letter, hit=None, miss=None):
        if hit is True and miss is True:
            raise InvalidGuessAttempt()
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit is True:
            return True
        return False
        
    def is_miss(self):
        if self.miss is True:
            return True
        return False


class GuessWord(object):
    def __init__(self, word):
        if len(word) == 0:
            raise InvalidWordException()
            
        self.answer = word
        self.masked = "*" * len(word)
    
    def perform_attempt(self, letter):
        letter = letter.lower()
        if len(letter) > 1:
            raise InvalidGuessedLetterException()
        if letter in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.unveil_word(self.answer, self.masked, letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt

    def unveil_word(self, answer, mask, letter):
        s = ""
        for i in range(len(self.answer)):
            word_letter = self.answer[i]
            mask_letter = self.masked[i]
            
            if mask_letter != "*":
                s += mask_letter
            elif letter == word_letter.lower():
                s += word_letter.lower()
            else:
                s += "*"
        return s

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        if word_list == None:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        selected_word = self.select_random_word(word_list)
        self.word = GuessWord(selected_word)
        self.previous_guesses = []
        
    
    def guess(self, letter):
        if self.is_finished():
            raise GameFinishedException()
        
        self.previous_guesses.append(letter.lower())
        
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -= 1
            if self.is_lost():
                raise GameLostException()
        
        if self.is_won():
            raise GameWonException()
        
        
        return attempt
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    
    #choose class method because we can call the method without requiring an instance
    @classmethod
    def select_random_word(cls, word_list):
        if len(word_list) == 0:
            raise InvalidListOfWordsException()
        return rand.choice(word_list)
    