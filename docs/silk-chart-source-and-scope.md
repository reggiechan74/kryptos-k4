# Photographed silk chart: source and scope

The [Duke collection page](https://people.duke.edu/~ng46/collections/crypto-silks.htm)
attributes its artifact to WWII SOE and cites John Brunner, *OSS WEAPONS* (1994),
p. 205. The [Proc page](https://jproc.ca/crypto/silk_otp.html), displayed date
May 12, 2007, credits Michael Graham's photograph and Frode Weierud's commentary.
It describes reciprocal substitution and OTP five-letter groups. These are modern
attributions, not a located primary wartime worked example for this exact table.
Matching photographs corroborate the mapping; independent artifact provenance is
not established. Neither citation establishes public availability of this exact
chart before 1990 or knowledge of it by Sanborn or Scheidt.

The [Duke photo](https://people.duke.edu/~ng46/collections/silk-red-black-alphabets.jpg)
and [Proc photo](https://jproc.ca/crypto/silkcode_chart_b.jpg) were both viewed.
The executor visually checked the 24 decisive crib cells and 12 modern-example
cells on both photographs; a second review supplied before the pilot checked all
24 decisive cells on both. This is not a claim of independent pixel retranscription
of all 676 cells. The full supplied transcription passes row/column permutation
and reciprocity checks. [Receipt](../sources/silk-chart-verification.json) pins
source-image byte counts, SHA256 digests, cell records and review scope. Photographs
are linked, not included in this repository.

Black top labels are keys; black row labels are plaintext. The adjacent red letter
is output. Our fixture preserves that literal table, normalizing red lowercase to
uppercase only. Columns are involutions. The modern PHOENIX demonstration for
ATTACKATDAWN computes **ZEAAIZXQOTFL**. The Duke text prints ZEAAINXQOTFL;
the decisive sixth cell, key I / plaintext K, is red z in both photographs.
This correction is source-pixel based and was fixed before the K4 pilot.
The modern repeating-key demonstration is not authenticated SOE key doctrine.

[Ardennes Archives' comparison lead](https://archives.cd08.fr/activites-culturelles/le-document-du-mois/les-mouchoirs-de-codage-des-agents-clandestins-en-france-occupee)
identifies fonds Georges-Henri Lallement 74J35. Its image was not inspectable in the
supplied review and was not inspected by this executor. No same-chart conclusion
or outreach follows.

The chart permits fixed points, including S→S and K→K with key X. A standard
Enigma no-self-encipherment argument therefore does not reject this table. The
previous narrow direct-Enigma finding is a separate model. This pilot treats a
source-backed mathematical table with a hypothetical direct repeating key, not a
reconstructed wartime system or an established K4 connection.
