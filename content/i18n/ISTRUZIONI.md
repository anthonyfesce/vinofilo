# Traduzioni di Vinofilo — istruzioni

Lingue: en, de, fr, es, ru, zh, ar. L'italiano (content/articles/) è l'originale.

## File
Per ogni articolo italiano `content/articles/<slug>.md` si crea `content/i18n/<lingua>/<slug>.md`
(stesso nome file dell'italiano), con questo formato:

```
---
title: <titolo tradotto>
description: <descrizione tradotta, 140–170 caratteri circa>
slug: <slug tradotto>
cover: <nome breve del soggetto, 1–3 parole (es. "Nebbiolo", "Orange wines")>
---

<testo tradotto in Markdown>
```

- Front matter: SOLO questi quattro campi, una riga ciascuno, nessuna virgoletta attorno ai valori, nessun ":" nel valore di `slug`.
  Nel titolo e nella descrizione i due punti sono permessi (si legge solo il primo ":" della riga).
- `slug`: minuscolo, solo lettere a-z, cifre e trattini, senza accenti; 3–7 parole chiave della lingua.
  Russo: traslitterazione latina (es. `nebbiolo-samyj-trudnyj-sort`). Cinese: pinyin senza toni (es. `nebbiolo-yidali-zui-nan-de-putao`).
  Arabo: traslitterazione latina semplice (es. `nebbiolo-ashab-anwa-al-inab`).
- Il testo mantiene ESATTAMENTE la struttura Markdown dell'originale: stessi titoli `##`, stessi paragrafi, elenchi,
  grassetti, tabelle e link (gli URL dei link non si cambiano).

## Stile
- Traduzione da giornalista del vino madrelingua, non letterale: deve leggersi come scritta in quella lingua,
  con lo stesso tono colto, ironico e con un punto di vista. Niente aggiunte di fatti, niente tagli.
- Numeri, date, percentuali, temperature e nomi propri restano identici. Denominazioni (Barolo DOCG, Etna DOC,
  Prosecco, Franciacorta…) e nomi di vitigni restano in italiano; si può aggiungere una brevissima spiegazione solo
  dove un lettore straniero non capirebbe (es. "contrade, the local named vineyards").
- Termini italiani usati come tali (appassimento, fruttaio, contrada, ripasso…) in corsivo `*così*` la prima volta.
- Virgolette e punteggiatura della lingua: en “…”, de „…“, fr « … » con spazi fini, es «…», ru «…», zh “…” e
  punteggiatura cinese a larghezza piena, ar «…» e punteggiatura araba (، ؛ ؟).
- Unità: si lasciano °C, litri, ettari come nell'originale.
- Il titolo deve funzionare per la ricerca in quella lingua (parole che la gente cercherebbe), restando elegante.

## Numeri della home
`content/i18n/<lingua>/_numeri.json`: dizionario `"<slug>|<numero>": "<didascalia tradotta>"` per tutte le
voci di NUMERI in build.py (stessa chiave, numero identico).

## Pagine
`content/i18n/<lingua>/pagine/privacy.md`: traduzione di content/pagine/privacy.md (stesso front matter con
`title`, `description`, `slug: privacy`; i blocchi `<!--ga-->…<!--/ga-->` e `<!--noga-->…<!--/noga-->` si
mantengono identici attorno al testo tradotto). Indirizzi email, nomi, indirizzi e ragione sociale non si traducono.
