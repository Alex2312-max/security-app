from cryptography.fernet import Fernet


# In main app
def encrypt(path_to_key, data):
    '''
        Function to encrypt data and transform the encrypted elements from byte type to str.
    :param path_to_key: Path to file where the key is contained;
    :param data: Data about user that should be encrypted;
    :return: Returns the encrypted data in json format;
    '''
    key = open(path_to_key, "rb").read()

    f = Fernet(key)

    for idx_key, key in enumerate(data.keys()):
        new_data = [f.encrypt(element.encode('ascii')) for element in data[key]]
        data[key] = [str(element.decode("utf-8")) for element in new_data]

    return data


# In web app
def decrypt(path_to_key, data):
    '''
        Function that decrypts the data recieved from desktop application.
    :param path_to_key: Path to file where the key is contained;
    :param data: Data about user that should be decrypted;
    :return: Returns the decrypted data in json format;
    '''
    key = open(path_to_key, "rb").read()
    new_data = {}
    f = Fernet(key)

    for idx_key, key in enumerate(data.keys()):
        # Each element from the list that is mapped to a key is transformed in bytes format,
        # decrypted using fernet and decoded to string format from bytes
        user_info = [(str(f.decrypt(bytes(element, 'utf-8')).decode("utf-8"))) for element in list(data[key])]
        new_data[key] = user_info

    return new_data


def preprocess_function(data):
    '''
        Function to organize the decoded information.
    :param data: Data to be organized;
    :return: Organized data;
    '''
    assert type(data) is dict, 'Invalid type.'

    new_data = {}

    for idx_key, key in enumerate(data.keys()):
        user_info = [''.join(data[key])][0]
        new_data[key] = user_info
    return new_data


# # Generate key
# key = Fernet.generate_key()
# with open("key.key", "wb") as key_file:
#     key_file.write(key)
#
# # Load key
# key = open("key.key", "rb").read()
user_info = {
    'user_name': 'John',
    'last_name': 'Andrew',
    'email': 'andreson@yahoo.com',
    'speed': '179'
}

key = "key.key"
result = encrypt(key, user_info)

with open("user.txt", 'w') as user_data:
     user_data.write(str(result))

print(result)
result_decrypt = decrypt(key, result)
print(result_decrypt)
print(preprocess_function(result_decrypt))

