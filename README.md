# [Newhope](https://newhopecrypto.org/) Attack

In this project I am trying to attack this algorithm with a brute-force attack.

## Instructions

The script that does the attack is `ref/breaker.py`.

It will run `ref/test/test_newhope` (which uses `ref/newhope` which I have modified to print a, sk and pk and not to use NTT) and will get data for a new key exchange (both public and private, first for attack, second to test results).

Then it will compute all possible secret keys and will compare them with sk (the real secret key).

If `VERBOSE` is set to False, it will print only the number of combinations to test and then if the key was found or not.
If `VERBOSE` is set to True, it will also print additional details.

You can change the PARAM_K (variable in script). Less than 20 catches less keys but a lot faster (less brute force combinations), 20 catches most keys, more than 20 may catch even more keys but it brute force may have too many values to test (still a lot less than the security it should provide).

## Requirements

The script uses [pwntools](https://github.com/Gallopsled/pwntools) for communication with the process.
