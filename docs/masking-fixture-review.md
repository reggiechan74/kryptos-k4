# Masking pilot fixture preflight

The fixed pilot specifications were committed at
`9f546aa279ec065f2a4788fe4a1895efbcf87750`, before implementation and K4 tests.
Preflight controls were then run only on supplied vectors and synthetic messages.

- Both supplied autokey hand vectors agree with independently checked arithmetic:
  KEY / ATTACKATDAWN gives KXRAVDAVNAPQ with plaintext feedback and
  KXRKZBKSEKOR with ciphertext feedback. They cross the primer boundary twice.
- The ACA's [published example](https://www.cryptogram.org/downloads/aca.info/ciphers/FractionatedMorse.pdf)
  was read directly: COME AT ONCE, the ROUND TABLE alphabet, ciphertext
  CBIILTMHVVFL, two terminal x padding symbols. The implementation agrees.
  This alphabet remains a control only, outside the two K4 maps.
- One **implementation-authored negative fixture** was incorrectly labeled:
  `.-xx..` is a valid encoding of A I, with a legal xx word separator. The
  preflight caught that label error; it was removed from the negative list and
  added as a positive consecutive-one-letter-word control before any actual K4
  pilot run. It is not an error in the ACA fixture. No decoder rule, registered
  key, alphabet, or K4 case bound changed.

The coding executor also read the relevant Army manual's section122 via PDF
text extraction, independently confirming the feedback principle. Neither
source identifies these pilots as Scheidt's actual masking technique.
