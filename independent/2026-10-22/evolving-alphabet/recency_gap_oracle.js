// A third implementation: compute rank directly, never construct a current alphabet.
// Run after the frozen pilot solely as an independent numerical cross-check.
const ct = 'OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR';
const alphabets = {AZ: 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', KRYPTOS: 'KRYPTOSABCDEFGHIJLMNQUVWXZ'};
const models = [];
for (const [rn, r] of Object.entries(alphabets)) {
  for (const [sn, s] of Object.entries(alphabets)) {
    const ranks = [];
    let plaintext = '';
    for (let i = 0; i < ct.length; i++) {
      const prefix = ct.slice(0, i), current = ct[i];
      const last = prefix.lastIndexOf(current);
      let rank;
      if (last >= 0) {
        // Exactly the distinct symbols emitted since the most recent current symbol.
        rank = new Set(prefix.slice(last + 1)).size;
      } else {
        // Every seen symbol precedes an unseen symbol; remaining unseen retain S0 order.
        const seen = new Set(prefix);
        const priorUnseen = [...s.slice(0, s.indexOf(current))].filter(x => !seen.has(x)).length;
        rank = seen.size + priorUnseen;
      }
      ranks.push(rank);
      plaintext += r[rank];
    }
    models.push({model: `R=${rn},S0=${sn}`, plaintext, ranks});
  }
}
process.stdout.write(JSON.stringify(models, null, 2) + '\n');
