import sys
import workingmode
import keystore


def print_error_message():
    print('Wrong usage of program\n')
    print(
        'Run the program like: python3 main.py <mode of encryption(CBC/CTR/GCM/OFB)> <path to keystore> <key name> <working mode(encor/challenge)>\n')
    exit(0)


def resolve_mode(key, encryption_mode):
    if working_mode == 'encor':
        return workingmode.EncryptionOracleWorkingMode(key, encryption_mode)
    elif working_mode == 'challenge':
        return workingmode.ChallengeWorkingMode(key, encryption_mode)
    else:
        raise Exception('Incorrect working mode')


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print_error_message()
    mode_of_encryption = sys.argv[1]
    if mode_of_encryption not in ('CBC', 'CTR', 'GCM', 'OFB'):
        print_error_message()
    path_to_keystore = sys.argv[2]
    key_identifier = sys.argv[3]
    working_mode = sys.argv[4]
    if working_mode not in ('encor', 'challenge'):
        print_error_message()

    key = keystore.KeyLoader(path_to_keystore).load_key(key_identifier)
    mode = resolve_mode(key, mode_of_encryption)
    mode.run()
