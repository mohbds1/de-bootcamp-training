"""
Text Vectorization Implementation (Bag of Words)
Description: A robust manual implementation of text-to-numerical vector conversion.
             This script processes input text by removing punctuation, normalizing 
             case, and handling extra spaces using Regular Expressions (re). It then 
             maps the cleaned words to a predefined vocabulary (bag of words) to 
             generate accurate word frequency vectors.
"""

import numpy as np
import re 

def text_to_vector(text, bag_of_words):
    # هذا السطر يحذف أي شيء ليس حرفاً (a-z) أو رقماً (0-9) أو مسافة (\s)
    clean_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    
    words = clean_text.lower().split()
    vector = []
    
    for vocab_word in bag_of_words:
        count = 0

        clean_vocab = re.sub(r'[^a-zA-Z0-9\s]', '', vocab_word).lower()
        
        for word in words:
            if word == clean_vocab:
                count += 1
                
        vector.append(count)
        
    return np.array(vector)


text1 = " Hello Mr. Ali "
text2 = "Hello Mr. Khaled"
text3 = "Ali Ali Ali Khaled Khaled"
text4 = "Hello, Mr. Ali!" 
text5 = "100% Hello!!! Mr... Ali???" 

bag = ["Hello", "Mr.", "Ali", "Khaled"]

print("Result 1: ", text_to_vector(text1, bag))
print("Result 2: ", text_to_vector(text2, bag))
print("Result 3: ", text_to_vector(text3, bag))
print("Result 4: ", text_to_vector(text4, bag))
print("Result 5: ", text_to_vector(text5, bag))