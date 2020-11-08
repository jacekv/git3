Generate with ssh

ssh-keygen -t ecdsa -b 256 -m pem

take the base64 encoded string and decode it
http://tomeko.net/online_tools/base64.php?lang=en
Shouldn't use in production!! The git client will do it once I get there

Extract the private key
# ASN.1 STRUCTURE FOR PRIVATE KEY:
#   30  <-- declares the start of an ASN.1 sequence
#   74  <-- length of following sequence 
#   02  <-- declares the start of an integer
#   01  <-- length of integer in bytes (1 byte)
#   01  <-- value of integer (1)
#   04  <-- declares the start of an "octet string"
#   20  <-- length of string to follow (32 bytes)
#           3cd0560f5b27591916c643 ... a738d2e912990dcc573715d2c 
#           \--------------------------------------------------/
#            this is the private key 
#   a0   <-- declares the start of context-specific tag 0
#   07   <-- length of context-specific tag 
#   06   <-- declares the start of an object ID
#   05   <-- length of object ID to follow 
#   2b 81 04 00 0a <-- the object ID of the curve secp256k1
#   a1   <-- declares the start of context-specific tag 1
#   44   <-- declares the length of context-sepcifc tag (68 bytes)
#   03   <-- declares the start of a bit string
#   42   <-- length of bit string to follow (66 bytes)
#   00   <-- ??
#            04 f1 44 f0 dc 00 80 af d2 b7 3f 13 37 6c ... 05 49 cd 83 f4 58 56 1e
#            \-------------------------------------------------------------------/
#             this is the public key

taken from https://bitcoin.stackexchange.com/questions/66594/signing-transaction-with-ssl-private-key-to-pem
Tested with metamask :) Work great