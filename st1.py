import cv2
import os

def encrypt(msg, img, password):
    d = {}
    c = {}
    for i in range(256):
        d[chr(i)] = i
        c[i] = chr(i)

    n, m, z = 0, 0, 0
    for char in msg:
        for i in range(7, -1, -1):
            img[n, m, z] = (img[n, m, z] & 0xFE) | ((d[char] >> i) & 1)
            n += 1
            m += 1
            z = (z + 1) % 3

    cv2.imwrite("stegofile.png", img)
    cv2.imshow("Stegofile", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return img

def decrypt(img, password):
    d = {}
    c = {}
    for i in range(256):
        d[chr(i)] = i
        c[i] = chr(i)

    index = 0
    decrypted_msg = ""

    height, width, _ = img.shape

    for _ in range(len(password)):
        for i in range(7, -1, -1):
            img[index // width, index % width, i % 3] = (img[index // width, index % width, i % 3] & 0xFE) | ((d[password[_]] >> i) & 1)
            index += 1

    # Reset index to 0 before entering the last loop
    index = 0
    
    for _ in range(height * width * 8 // len(password)):
        bits = 0
        for i in range(7, -1, -1):
            if index < height * width:
                bits |= ((img[index // width, index % width, i % 3] & 1) << i)
                index += 1

        decrypted_msg += c[bits]

    print("Decrypted Message:", decrypted_msg)


img = cv2.imread("cars.jpg")

msg = input("Enter your secret message: ")
password = input("Enter password: ")

# Encryption
img = encrypt(msg, img, password)

# Decryption
password_verify = input("Enter your password for decryption: ")

if password == password_verify:
    decrypt(img, password)
else:
    print("Password not valid.")
