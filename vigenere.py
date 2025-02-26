import string

def vigenere_decrypt(ciphertext, key):
    alphabet = string.ascii_uppercase 
    decrypted_text = []
    key = key.upper()
    
    key_length = len(key)
    
    key_indices = [(alphabet.index(k) + 1) for k in key]  
    
    j = 0  
    for char in ciphertext:
        if char in alphabet:
            cipher_index = alphabet.index(char) + 1  
            key_index = key_indices[j % key_length]  
            
     
            plain_index = (cipher_index - key_index) % 26
            if plain_index == 0:
                plain_index = 26  
                
            decrypted_text.append(alphabet[plain_index - 1])  
            
            j += 1  
        else:
            decrypted_text.append(char) 

    return "".join(decrypted_text)


ciphertext = "EMD BZHNP"  
key = "KEY"
print(vigenere_decrypt(ciphertext, key))  
