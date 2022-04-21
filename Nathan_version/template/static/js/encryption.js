function encodeString(string) {
    var encoder = new TextEncoder();
    return encoder.encode(string);
  }
  
  function decodeString(encoded) {
    var decoder = new TextDecoder();
    return decoder.decode(encoded);
  }


let keyPair = await crypto.subtle.generateKey(
  {
    name: "RSA-OAEP",
    modulusLength: 4096,
    publicExponent: new Uint8Array([1, 0, 1]),
    hash: "SHA-256"
  },
  true,
  ["encrypt", "decrypt"]
);