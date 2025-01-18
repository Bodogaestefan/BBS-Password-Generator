import secrets

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_large_prime():
    while True:
        num = secrets.randbelow(10**10 - 10**9) + 10**9
        if is_prime(num):
            return num

def generate_blum_blum_shub(bits):
    p = generate_large_prime()
    q = generate_large_prime()
    while p == q:
        q = generate_large_prime()
    
    n = p * q
    seed = secrets.randbelow(n)
    x = seed * seed % n
    
    random_bits = []
    for _ in range(bits):
        x = x * x % n
        random_bits.append(x % 2)
    
    return random_bits

if __name__ == "__main__":
    bits = 128  # Number of bits you want to generate
    random_bits = generate_blum_blum_shub(bits)
    random_number = int(''.join(map(str, random_bits)), 2)
    print(f"Generated random number: {random_number}")
    
    password_length = 16  # Length of the password you want to generate
    password_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
    
    # Generate enough random bits for the password
    random_bits = generate_blum_blum_shub(password_length * 8)
    
    password = ''.join(password_characters[int(''.join(map(str, random_bits[i*8:(i+1)*8])), 2) % len(password_characters)] for i in range(password_length))
    print(f"Generated password: {password}")