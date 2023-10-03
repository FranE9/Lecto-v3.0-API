import statistics

class Perspicuity:
    def __init__(self, values):
        self.words = values['words']
        self.phrases = values['phrases']
        self.syllables = values['syllables']
        self.syllables3 = values['Three_sillabls_words']
        self.letters = values['letters']

    def calculate(self):
        return 0
    
    def limitResult(self,value):
        if value>100.0:
            return 100.0
        if value<0.0:
            return 0.0
        return value

class SzigrisztPazos(Perspicuity):
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0

        if(not(has_words) or not(has_phrases)):
            return 0
        return self.limitResult((207 - (62.3*((self.syllables*1.0)/(self.words*1.0))) - ((self.words*1.0)/(self.phrases*1.0))))


class FernandezHuerta(Perspicuity):
        
    def calculate(self):
        has_words = self.words > 0
        has_phrases = self.phrases > 0
        if (not(has_words) or not(has_phrases)):
            return 0

        P, F = self.__calculateFernandezHuertaValues()
        
        return self.limitResult((206.84 - (60*P) - (1.02*F)))
    
    def __calculateFernandezHuertaValues(self):
        P = (self.syllables*1.0)/(self.words*1.0)
        F = (self.words*1.0)/(self.phrases*1.0)
        return P, F

class MuLegibility(Perspicuity):
    def calculate(self):
        try:
            mean = statistics.mean(self.letters)>0
            variance = statistics.variance(self.letters) >0
        except:
            return 0
        if(not(mean) or not(variance)):
            return 0
        return self.limitResult(((self.words) / ((self.words) - 1.0)) * (statistics.mean(self.letters) / statistics.variance(self.letters) ) * 100)


#==================================================================================================
#                                           INGLES
#==================================================================================================

class Flesch(Perspicuity):
    def calculate(self):
        try:
            has_words = self.words > 0
            has_phrases = self.phrases > 0
            if (not(has_words) or not(has_phrases)):
                return 0
            
            ASL = self.words/self.phrases
            ASW = self.syllables/self.words
            return self.limitResult(206.835 - (1.015 * ASL) - (84.6 * ASW))
        except:
            return 0
    

class Smog(Perspicuity):
    def calculate(self):
        try:
            has_words = self.words > 0
            has_phrases = self.phrases > 0
            if (not(has_words) or not(has_phrases)):
                return 0
            
            ASL = (self.syllables3) * (30/self.phrases)
            Result = 3.1291 + (1.0430 * (ASL**0.5))
            if Result >=1 and Result <=240:
                return Result
            else:
                return 240
        except:
            return 240
    

class Fog(Perspicuity):
    def calculate(self):
        try:
            has_words = self.words > 0
            has_phrases = self.phrases > 0
            if (not(has_words) or not(has_phrases)):
                return 0
            
            ASL = self.words/self.phrases
            ASW = self.syllables3/self.words
            Result = 0.4 * (ASL + 100 * (ASW))
            if Result >=6 and Result <=17 :
                return Result
            else:
                return 17
        except:
            return 17