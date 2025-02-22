<!--
SPDX-FileCopyrightText: 2021 Anders Rune Jensen

SPDX-License-Identifier: CC0-1.0
-->

# Bendy Butt

What is Bendy Butt?

> A new feed format designed for [meta feeds]

Why a new feed format, when we already have [gabby grove] and [bamboo]?

> Because we would want to offer a feed format that is simple and easy
> to implement in any programming language by reusing an established
> format ([bencode]) with existing encoder libraries.  Furthermore, as
> meta feeds makes it easier to have multiple feed formats, we wanted
> to show that creating a new feed format does not have to be hard.

Can't you just use the classic format?

> That would mean clients would have to support reading and writing
> the classic format forever, even for applications that only use
> newer feed formats.

What is wrong with the classic format?

> There are multiple problems, most of them come from the fact that it
> is very tied to the internals of the v8 engine for Javascript. JSON
> is good as an exchange format for values of data but not well suited
> to cryptographically sign messages where a canonical representation
> of each value is paramount.

Can I use Bendy Butt for purposes other than meta feeds?

> Yes, but Bendy Butt was not designed as a general purpose feed 
> format. We do not intend to extend Bendy Butt to cover any other
> use cases besides meta feeds, but if the feed format constraints
> are sufficient for your use cases, nothing stops you from using it.
> To preserve the simplicity of this spec, we recommend not sending
> patches to the spec to generalize it.

## Definitions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in RFC 2119.

**Notations for bencode and BFE**

To avoid confusion with JSON, we shall use the notation `{ "a" => 1, "b" => 2 }`
to denote a [bencode] *dictionary* with two entries: key "a" mapping to value
`1` and key "b" mapping to value `2`.  We shall use the notation `[a, b, c]` to
denote a [bencode] *list* of three values `a`, `b`, and `c`.

For sequences of bytes, we use the notation `<03 02 01>` to represent the
sequence of bytes `03` followed by `02` followed by `01`. We use the notation
`a + b + c` to denote *byte concatenation* of the byte sequences `a` followed by
`b` followed by `c`. In other words `<05 04> + <03 02 01>` equals
`<05 04 03 02 01>`.

For abstract substitutions, we use `(something)` to denote whatever `something`
describes. In other words, anything wrapped in parentheses is just a placeholder
for something else.

## Specification

A *Bendy Butt message* is encoded in [bencode] as a list of message `payload`
and `signature`, which we shall denote `[payload, signature]`. SSB Binary Field
Encodings ([SSB-BFE]) is used to encode all non-list non-dictionary non-integer
values contained in the `payload` and `signature`. BFE also helps to
disambiguate binary data like feed IDs and message IDs from generic data types
such as strings.

The message `payload` is a bencode list with 5 elements in this specific order,
in other words, `[author, sequence, previous, timestamp, contentSection]`:

1) `author`, a BFE-encoded "feed ID"
2) `sequence`, a [bencode integer] greater than or equal to 1
3) `previous`, a BFE-encoded "message ID" of the previous message
  on the feed. For the first message this must be the BFE "nil" generic data
  type.
4) `timestamp`, a [bencode integer] representing the UNIX epoch timestamp of message
  creation.
5) `contentSection` can be one of two possible shapes:
    1. `[content, contentSignature]` such that `content` is any bencode
    dictionary representing the message contents, all of which are internally
    encoded with BFE; and `contentSignature` is a BFE-encoded "signature". The
    signature is applied on `prefix + content`, where `prefix` is the string
    "bendybutt" encoded as UTF8 bytes. The signature uses some cryptographic
    keypair which **MAY** be different from the `author` keypair (for example,
    under the [meta feeds] spec, this will be the subfeed keypair).
    2. BFE-encoded "encrypted data". Upon decryption, it takes the shape
    `[content, contentSignature]` as described above.

The message `signature` is applied on `payload` using the `author`'s
cryptographic keypair.

Both the `signature` and the `contentSignature` use the same [HMAC signing capability]
(`sodium.crypto_auth`) and `sodium.crypto_sign_detached` as in the classic
SSB format (ed25519).

The key or ID of a Bendy Butt message is the SHA256 hash of the bencoded bytes
for `[payload, signature]`, i.e. `key = SHA256([payload, signature])`.

## Example

Following our `[a, b]` and `{ "a" => 1, "b" => 2}` notation, which may look
similar to JSON, here is a Bendy Butt message with the `content` dictionary
equal to `{ "type" => 'greet', "text" => 'Good morning!' }`.

```
[
  [
    <00 03 5c 27 ac 6e f0 cd fb d0 f8 9a 89 a1 b6 5a 36 04 77 a3 3e c7 9c b7 ab 14 cd 90 76 25 59 be e2 ff>,
    1,
    <06 02>,
    12345,
    [
      {
        "type" => <06 00 67 72 65 65 74>,
        "text" => <06 00 47 6f 6f 64 20 6d 6f 72 6e 69 6e 67 21>
      }
      <04 00 51 a6 7a 43 6a 66 f6 6d e0 3d 77 73 c0 b7 ba 98 84 61 32 46 c6 ee 6c 74 1b 1d 9e 59 18 24 b3 c7 1d a3 ec 35 bf e0 32 cf 86 55 7c f8 72 30 e9 56 ... 16 more bytes>
    ]
  ],
  <04 00 6d 57 9f 55 14 d2 d8 69 09 ad 7b 31 f8 24 4f a7 fc 6a 0d c1 1e f4 1a 92 71 86 fb 8d 1b fc d5 17 b3 88 05 f0 a6 48 aa ba 24 f4 46 b0 9e 65 64 b6 ... 16 more bytes>
]
```

Notice that is has the shape:

```
[
  [
    author,
    sequence,
    previous,
    timestamp,
    [
      content,
      contentSignature
    ]
  ],
  signature
]
```

Here is the same data as above, but displayed in raw binary (hexadecimal):

```
    Offset   00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
    000000   6C 6C 33 34 3A 00 03 5C 27 AC 6E F0 CD FB D0 F8   ll34:..\'¬nðÍûÐø
    000010   9A 89 A1 B6 5A 36 04 77 A3 3E C7 9C B7 AB 14 CD   ..¡¶Z6.w£>Ç.·«.Í
    000020   90 76 25 59 BE E2 FF 69 31 65 32 3A 06 02 69 31   .v%Y¾âÿi1e2:..i1
    000030   32 33 34 35 65 6C 64 34 3A 74 65 78 74 31 35 3A   2345eld4:text15:
    000040   06 00 47 6F 6F 64 20 6D 6F 72 6E 69 6E 67 21 34   ..Good morning!4
    000050   3A 74 79 70 65 37 3A 06 00 67 72 65 65 74 65 36   :type7:..greete6
    000060   36 3A 04 00 51 A6 7A 43 6A 66 F6 6D E0 3D 77 73   6:..Q¦zCjfömà=ws
    000070   C0 B7 BA 98 84 61 32 46 C6 EE 6C 74 1B 1D 9E 59   À·º..a2FÆîlt...Y
    000080   18 24 B3 C7 1D A3 EC 35 BF E0 32 CF 86 55 7C F8   .$³Ç.£ì5¿à2Ï.U|ø
    000090   72 30 E9 56 8E D5 7B 25 F6 77 FE 58 3B 17 3D BD   r0éV.Õ{%öwþX;.=½
    0000A0   E7 08 82 0F 65 65 36 36 3A 04 00 6D 57 9F 55 14   ç...ee66:..mW.U.
    0000B0   D2 D8 69 09 AD 7B 31 F8 24 4F A7 FC 6A 0D C1 1E   ÒØi.­{1ø$O§üj.Á.
    0000C0   F4 1A 92 71 86 FB 8D 1B FC D5 17 B3 88 05 F0 A6   ô..q.û..üÕ.³..ð¦
    0000D0   48 AA BA 24 F4 46 B0 9E 65 64 B6 9A DE 97 F9 18   Hªº$ôF°.ed¶.Þ.ù.
    0000E0   04 AF 5F 7A F3 5E 5D 4B FD 85 0B 65               .¯_zó^]Ký..e
```


## Validation

For validation we differentiate between *message validity* and *content
validity*. Since the content can be encrypted, there is potentially no way to
validate that. This means a message should only be rejected before insertion
into the local database if it fails the message validation rules. A message
should not be included in the bendy butt feed if its content is not valid.

The message **MUST** conform to the following rules:

 - Has the shape of a bencode list `[payload, signature]`
 - The payload has the shape of bencode list `[author, sequence, previous, timestamp, contentSection]`
 - The `previous` field matches the previous message's ID
 - The `signature` field must be correctly signing the `payload`
 - The [SSB-BFE] *type-format* for `author` is `0x0003` (there is no
 upgradeability in the middle of a feed)
 - The [SSB-BFE] *type-format* for `previous` is `0x0104`
 - The `author` is the same as in previous messages on the feed
 - The maximum size of a `[payload, signature]` in bytes must not exceed 8192 bytes

Under the Bendy Butt spec, the content is free-form, but under the [meta feeds]
spec there are strict constraints applied to this bencode dictionary.

[SSB]: https://github.com/ssbc/
[gabby grove]: https://github.com/ssbc/ssb-spec-drafts/tree/master/drafts/draft-ssb-core-gabbygrove/00
[bamboo]: https://github.com/AljoschaMeyer/bamboo
[meta feeds]: https://github.com/ssb-ngi-pointer/ssb-meta-feed-spec
[SSB-BFE]: https://github.com/ssb-ngi-pointer/ssb-binary-field-encodings
[HMAC signing capability]: https://github.com/ssb-js/ssb-keys#signobjkeys-hmac_key-obj
[bencode]: https://en.wikipedia.org/wiki/Bencode
[bencode integer]: https://wiki.theory.org/index.php/BitTorrentSpecification#Integers
