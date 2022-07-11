	"""
    	PythonBitcoinMiniKey v0.1 is a stand alone Bitcoin mini private key generator
	Source code was found on BitcoinTalk.org, and has been modified to use the
	SystemRandom() function for secure generation of keys.
	Change: GenerateKeys(numKeys = 21) = will create 21 mini private keys per run.
	
	"""

import random
import hashlib
 
BASE58 = '23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def Candidate():
    """
    Generate a random, well-formed mini private key.
     new version uses SystemRandom() which is safe per python docs
     old version   [BASE58[ random.randrange(0,len(BASE58)) ] for i in range(29)])))
    """

    srandom = random.SystemRandom()

    return('%s%s' % ('S', ''.join(
        [BASE58[ srandom.randrange(0,len(BASE58)) ] for i in range(29)])))
 
def GenerateKeys(numKeys = 21):
    """
    Generate mini private keys and output the mini key as well as the full
    private key. numKeys is The number of keys to generate, and 
    """
    keysGenerated = 0
    totalCandidates = 0
    while keysGenerated < numKeys: 
        try:
            cand = Candidate()
            # Do typo check
            t = '%s?' % cand
            # Take one round of SHA256
            candHash = hashlib.sha256(t).digest()
            # Check if the first eight bits of the hash are 0
            if candHash[0] == '\x00':
                privateKey = GetPrivateKey(cand)
                print('\n%s\nSHA256( ): %s\nsha256(?): %s' %
                      (cand, privateKey, candHash.encode('hex_codec')))
                if CheckShortKey(cand):
	             print('Validated.')
                else:
                    print('Invalid!')
                keysGenerated += 1
            totalCandidates += 1
        except KeyboardInterrupt:
            break
    print('\n%s: %i\n%s: %i\n%s: %.1f' %
          ('Keys Generated', keysGenerated,
           'Total Candidates', totalCandidates,
           'Reject Percentage',
           100*(1.0-keysGenerated/float(totalCandidates))))
 
def GetPrivateKey(shortKey):
    """
    Returns the hexadecimal representation of the private key corresponding
    to the given short key.
    """
    if CheckShortKey(shortKey):
        return hashlib.sha256(shortKey).hexdigest()
    else:
        print('Typo detected in private key!')
        return None
 
def CheckShortKey(shortKey):
    """
    Checks for typos in the short key.
    """
    if len(shortKey) != 30:
        return False
    t = '%s?' % shortKey
    tHash = hashlib.sha256(t).digest()
    # Check to see that first byte is \x00
    if tHash[0] == '\x00':
        return True
    return False

GenerateKeys()
