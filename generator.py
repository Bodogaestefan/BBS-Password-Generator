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
        num = secrets.randbelow(10 ** 10 - 10 ** 9) + 10 ** 9
        if is_prime(num):
            return num


def generate_blum_blum_shub_bit_sequence(bits):
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


def generate_bbs_password(password_alphabet, password_length=32):
    random_bits = generate_blum_blum_shub_bit_sequence(password_length * 8)

    password = ''.join(
        password_alphabet[int(''.join(map(str, random_bits[i * 8:(i + 1) * 8])), 2) % len(password_alphabet)] for i
        in range(password_length))

    return password


def generate_bbs_salt():
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_?"
    random_bits = generate_blum_blum_shub_bit_sequence(16 * 8)

    iv = ''.join(
        alphabet[int(''.join(map(str, random_bits[i * 8:(i + 1) * 8])), 2) % len(alphabet)] for i
        in range(16))

    return iv.encode()

# def generate_bbs_salt():
#     print()


if __name__ == "__main__":
    password_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*-_?"

    # Generate enough random bits for the password
    # random_bits = generate_blum_blum_shub(password_length * 8)

    # password = ''.join(
    #     password_characters[int(''.join(map(str, random_bits[i * 8:(i + 1) * 8])), 2) % len(password_characters)] for i
    #     in range(password_length))
    # print(f"Generated password: {password}")

    rand_password = generate_bbs_password(password_characters)
    print("PASSWORD: " + rand_password)
