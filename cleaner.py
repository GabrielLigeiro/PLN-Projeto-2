import pandas as pd
import re

class Cleaner():
    def __init__(self):
        # data: 03/04/2021
        
        palavras_banidas = [r'(?:\s-*?|^)(?:fox)*bot(?:\s-*?|$)((?:fox)*bot(?:\s-*?|$))*', # Foxbot ou bot
                            r'(?:\s-*?|^)d[a-z]s*(?:\s-*?|$)(d[a-z]s*(?:\s-*?|$))*' # da, de,di,do
                            
                           ]
        patt = '|'.join(palavras_banidas)
        
        self.patterns = {
            # Fonte : https://pt.stackoverflow.com/questions/15738/como-validar-com-regex-uma-string-contendo-apenas-letras-espa%C3%A7os-em-branco-e-le
            # Tudo que não for letras, letras acentuadas em pt ou traço vira espaço
            # (isso inclui emojis,caracteres especiais e quebras de linha)
            'not_good':r'[^a-zA-Z^\-^á^à^â^ã^é^è^ê^í^ï^ó^ô^õ^ö^ú^ç^ñ]',
            # Sistema para retirar traços emm todas situações não normais na linguagem
            'traco_0':r'--+?',
            'traco_1':r'(?:-*?\s|^)[-]+?(?:\s-*?|$)',
            'traco_2':r'(\S)[-]+?(?:\s-*?|$)',
            'traco_3':r'(?:-*?\s|^)[-]+?(\S)',
            'letras_sozinhas':r'(?:\s|^)\w(?:\s|$)(?:\w(?:\s|$))*',
            'palavra_de_1_letra':r'(?:\s|^)(\w)\1+(?:\s|$)',
            'palavras_banidas':patt,
            'espacos':r'[ ]+'
            
        }
        
        self.replies_mapping = {
            'not_good':r' ',
            'traco_0':r'-',
            'traco_1':r' ',
            'traco_2':r'\1 ',
            'traco_3':r' \1',
            'letras_sozinhas':r' ',
            'palavra_de_1_letra':r' ',
            'palavras_banidas':r' ',
            'espacos':r' '
            
        }
        
        self.matchers = {}
        
        for key,patt in self.patterns.items():
            self.matchers[key] = re.compile(self.patterns[key],re.VERBOSE)
    
    def clean_text(self,text):
        # Deixa em letra minúscula
        clean_text = text.lower()
        
        # Aplica as limpezas
        for matcher_name,matcher in self.matchers.items():
            clean_text = matcher.sub(self.replies_mapping[matcher_name],clean_text)
        
        # Retira espaços nas extremidades
        clean_text = clean_text.strip()
        
        return clean_text
    