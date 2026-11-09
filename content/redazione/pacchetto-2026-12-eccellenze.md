# Serie "Eccellenze italiane" 12–16.12.2026 (10 articoli, richiesta di Anthony del 9.11.2026)

Dieci ritratti di case storiche del vino italiano, 2 al giorno dal 12 al 16 dicembre 2026, in aggiunta alle uscite del pacchetto 21.11–4.1
(che negli stessi giorni ha i n. 183–192). Una casa per regione. Fontanafredda è fissata al 14.12, seconda del giorno.
Numeri 231–240 (139–140 restano riservati alla patch guide 2027/Barolo). Categoria Territori per tutti.
Titoli: "Eccellenze italiane: <Casa>, ..." (nelle traduzioni: en Italian Excellence, de Italiens große Weinhäuser,
fr Grandes maisons italiennes, es Excelencias italianas, ru Великие винные дома Италии, zh 意大利名庄, ar دور النبيذ الإيطالية الكبرى).
Ogni attacco dice "N-esimo ritratto della serie"; in fondo a ogni articolo la sezione "## La serie completa" con i dieci titoli linkati
nella lingua dell'articolo (l'articolo corrente in grassetto, senza link).

Link: per la nuova regola di Anthony (9.11.2026) ogni articolo linka i siti ufficiali verificati della casa (storia, vini, visite),
dei consorzi/disciplinari o enti citati, più 1–2 articoli Vinofilo già usciti. I link interni verso articoli non ancora pubblicati
restano solo testo finché il bersaglio non esce: lo fa build.py (funzione `unlink` in build_lang), quindi i link della serie
si accendono da soli giorno per giorno con le uscite del mattino.

Bozze e script di lavoro (fuori dal repo, sessione temporanea): scratchpad/ecc/<lingua>/<slug>.md, scratchpad/finalize.py
(risolve [[slug|testo]] e il segnaposto della serie per ogni lingua).

Stato: colonna 'stato' = da fare / it / tradotto / nel repo / illustrazione.

| n | data | casa | regione | slug | cat | cover | inquadratura | soggetto illustrazione (in breve) | stato |
|---|---|---|---|---|---|---|---|---|---|
| 231 | 2026-12-12 | Ferrari Trento | Trentino | ferrari-trento-metodo-classico | Territori | Ferrari | ritmo/ripetizione | file di pupitres in una cantina a volta, un flûte paglierino-oro, Dolomiti dall'arco in fondo | nel repo |
| 232 | 2026-12-12 | Marchesi Antinori | Toscana | marchesi-antinori-tignanello | Territori | Antinori | notturno | facciata di palazzo fiorentino di notte, buchetta del vino aperta con un calice rubino | nel repo |
| 233 | 2026-12-13 | Masi | Veneto | masi-amarone-valpolicella | Territori | Masi | interno con figure piccole | fruttaio alto con arele di Corvina in appassimento, due figure lontane | nel repo |
| 234 | 2026-12-13 | Mastroberardino | Campania | mastroberardino-taurasi-irpinia | Territori | Mastroberardino | sezione | spaccato di paese irpino: strada sopra, cantina a volte affrescate sotto, calice granato | nel repo |
| 235 | 2026-12-14 | Donnafugata | Sicilia | donnafugata-sicilia-pantelleria | Territori | Donnafugata | veduta aerea | Pantelleria: terrazze di pietra lavica, alberelli nelle conche, dammusi, giardino pantesco | nel repo |
| 236 | 2026-12-14 | Fontanafredda | Piemonte | fontanafredda-barolo-serralunga | Territori | Fontanafredda | panorama | villaggio a facciate a strisce, anfiteatro di vigne d'autunno, bosco sul colle, torre di Serralunga | nel repo |
| 237 | 2026-12-15 | Lungarotti | Umbria | lungarotti-torgiano-umbria | Territori | Lungarotti | natura morta su fondo scuro | anfora antica, brocca di maiolica, calice rubino di Sangiovese, rametto d'olivo | nel repo |
| 238 | 2026-12-15 | Leone de Castris | Puglia | leone-de-castris-five-roses | Territori | Leone de Castris | figura umana di profilo, piccola | cortile di masseria salentina anni '40, carretto di bottiglie vuote, cinque rose, caraffa rosa corallo | nel repo |
| 239 | 2026-12-16 | Livio Felluga | Friuli | livio-felluga-rosazzo | Territori | Livio Felluga | vista dall'alto (tavola apparecchiata) | tavolo con una mappa disegnata delle colline (senza scritte), due calici paglierini, castagne | nel repo |
| 240 | 2026-12-16 | Sella & Mosca | Sardegna | sella-e-mosca-alghero | Territori | Sella & Mosca | costa o montagna | piana di vigne verso il mare, Capo Caccia, ingresso di una domus de janas in primo piano | nel repo |

Il prompt completo di ogni illustrazione è nel campo `illustrazione:` dell'articolo italiano. Le immagini sono DA GENERARE
(skill immagini-vinofilo): senza `assets/img/<slug>.jpg` l'articolo non esce.

Prezzi: solo quelli verificati (listini visite sui siti ufficiali a novembre 2026, Campofiorin da The Drinks Business 2023,
Abbazia di Rosazzo 2021 da L'Espresso 2026); per il resto "i prezzi variano". Dati lasciati in forma prudente o tolti:
anno del titolo di contessa a Rosa Vercellana (fonti discordi 1858/1877), prezzo d'acquisto di Fontanafredda da parte del
Monte dei Paschi (cifre discordi sul sito), ettari attuali di Donnafugata a Pantelleria (53 o 68 secondo la pagina), anno
esatto in cui Livio Felluga arrivò a Rosazzo (fine anni Trenta secondo L'Espresso e Gambero Rosso), alcol dell'Anghelu Ruju
(da schede commerciali, non dalla casa).
