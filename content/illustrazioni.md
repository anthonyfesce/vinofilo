# Illustrazioni Vinofilo

Ogni articolo ha un'illustrazione in `assets/img/<slug>.jpg` (1536×1024, JPG q84). Se il file manca, il sito mostra un segnaposto colorato.

Generazione: ComfyUI sul PC (Qwen-Image 2.1, http://127.0.0.1:8000, workflow ricostruibile dai metadati di un PNG v_*), 3 seed per soggetto,
si tiene la migliore. Output in M:\AI Engine\Comfy_Files\output\fixitinpost\vinofilo\v_<slug>_<seed>_00001_.png.

## Regola principale: VARIETÀ (Anthony, 06.10.2026)
"Non puoi farle TUTTE con un soggetto al centro." Le prime versioni (oggetto singolo al centro su fondo crema) sono state scartate:
nei cerchi della home reggevano, nelle schede rettangolari no. Ogni illustrazione riempie tutto il riquadro e cambia inquadratura
rispetto alle vicine. Inquadrature da alternare: panorama, veduta aerea, notturno, interno (anche con figure piccole), vista dall'alto
(tavola apparecchiata), dettaglio/macro, natura morta su fondo scuro, ritmo/ripetizione (scaffali, bicchieri in fila), sezione,
figura umana (di profilo o di lato, mai mani in primo piano), costa/montagna. Per un nuovo articolo scegliere un'inquadratura diversa
da quelle degli ultimi 4–5 articoli.

## Vincolo rigido: il colore del vino (Anthony, 06.10.2026)
Il colore del vino deve essere sempre corretto e credibile (bianchi paglierino/dorati, orange ambrato, rosati dal salmone al ciliegia,
rossi dal rubino al granato, Lambrusco violaceo, spumanti oro pallido). Mai vino verde, azzurro o di colori inventati.
Tutto il resto (soggetto, inquadratura, surreale) è flessibile. Controllare il vino in ogni immagine prima di pubblicarla.

## Stile (uguale per tutte)
Coda del prompt: Sophisticated editorial gouache painting, like the cover of a literary magazine: flat matte gouache shapes, muted
refined palette of deep burgundy, ochre, sage green, dusty blue and cream, quiet poetic mood, mature and elegant. The painting fills
the whole frame edge to edge, with no empty plain background. No text.

Negativo: text, letters, words, numbers, writing, typography, caption, label text, logo, watermark, signature, cartoon, comic, childish,
anthropomorphic, neon colours, 3d render, plastic, deformed hands, extra fingers, distorted face, isolated object on plain background,
empty background, blurry

Attenzione: la palette dello stile (salvia, azzurro) finisce nel vino se il soggetto sono bicchieri di colori diversi: in quel caso
scrivere i colori del vino uno per uno e cambiare la palette (vedi rosati).

## Prompt per articolo (scelti il 06.10.2026: seed 111, rosati seed 444)

| slug | inquadratura | soggetto |
|---|---|---|
| nebbiolo-vitigno-piu-difficile | panorama | Wide panoramic view of the Langhe hills in late autumn, steep vineyard rows climbing the slopes in rhythmic stripes of rust and ochre, banks of white fog filling the valleys, a hilltop village with a medieval tower on the far right, low horizon, two tiny harvesters with baskets among the rows. |
| etna-vulcano-del-vino | notturno | Night view of Etna in the far distance with a thin red glow of lava running down its dark flank, in the foreground on the left old bush vines on black volcanic terraces held by dry-stone walls, deep indigo sky. |
| metodo-classico-charmat | macro | Extreme close-up of the inside of a glass of sparkling wine, the whole frame filled with streams of tiny rising bubbles in pale gold, the curved rim of the glass cutting across the top corner. |
| vini-orange | dall'alto | Top-down view of a rustic wooden table: a glass of amber-orange wine, a terracotta jug, scattered white grapes and grape skins, a folded linen napkin, loosely arranged off-centre, warm afternoon shadows, cropped by the frame edges. |
| temperatura-di-servizio | interno con figura | Interior of a quiet trattoria at dusk seen from the doorway: a waiter in a white apron lifts a bottle of white wine from a silver ice bucket beside a small table by the window, warm lamp light, long room with a tiled floor. |
| forma-del-calice | ritmo | A long shelf seen frontally, crowded with dozens of empty wine glasses of every shape and size in a repeating rhythm, their transparent outlines overlapping, against a deep dusty-blue wall. |
| amarone-appassimento | interno | Interior of a large old drying loft, long wooden racks stacked with hundreds of bunches of red grapes receding into deep perspective, light falling from a row of high windows, one small figure in the distance checking the grapes. |
| leggere-etichetta-vino | dettaglio | Low-angle close-up of a wine shop shelf: rows of bottle necks and shoulders cropped by the frame, foil capsules in burgundy, gold and black, plain blank cream labels, one bottle tilted forward catching the light. |
| decantare-o-no | natura morta scura | Still life on a deep burgundy background: a crystal decanter on the right third of the frame, red wine pouring into it in a thin ribbon from a tilted bottle, a lit candle on the left, strong diagonal shadows. |
| sangiovese-cento-volti | veduta aerea | Aerial view of the Tuscan countryside like a patchwork quilt: vineyards, olive groves, lines of cypresses, a winding white road and scattered stone farmhouses, fields in burgundy, ochre, sage green and dusty blue, filling the whole frame. |
| cantina-in-casa | interno | Interior of a small vaulted brick cellar seen from the bottom of the stairs, wooden racks of bottles lying on their sides along both walls, a single bare bulb, a wicker chair, daylight falling down the stairway from the upper left. |
| aglianico-barolo-del-sud | paesaggio drammatico | Rugged volcanic hills of Irpinia under a stormy late-autumn sky, vineyards in the foreground bending in the wind, a lone stone farmhouse on a ridge to the left, heavy clouds in slate grey and burgundy. |
| verdicchio-bianco-che-invecchia | diagonale | View from a hillside vineyard in the Marche down to the Adriatic sea, rows of vines running diagonally from the bottom left corner towards a distant blue coastline, golden September light. |
| timorasso-vitigno-salvato | figura nel paesaggio | An old winegrower kneeling in a small terraced vineyard on a steep hillside at dawn, tending young vines, seen from a distance, mist lying in the valley behind him. |
| lambrusco-non-e-un-vino-da-poco | dall'alto | Top-down view of a convivial table in Emilia: bowls of tortellini, a board of cured ham and Parmigiano, two glasses of foaming purple red wine and a bottle, crumbs on a checked cloth, everything cropped by the frame edges. |
| vitigni-dimenticati-che-tornano | tavola botanica | A page of an old botanical herbarium: nine different grape varieties painted in a neat three-by-three grid, each bunch and leaf different in colour and shape, on pale aged paper, no writing. |
| chianti-e-chianti-classico | paesaggio con strada | A winding road lined with cypresses climbing through the Chianti hills towards a stone castle, vineyards and olive groves on both sides, long shadows of late afternoon. |
| brunello-mito-recente | notturno | Montalcino at night: the hilltop town and its fortress glow with warm lit windows above dark vineyard slopes, a large pale moon low on the horizon, deep blue sky. |
| sardegna-cannonau-vermentino | costa | Wide view of a wild Sardinian coastline: wind-sculpted granite rocks, low bush vines growing in sandy soil down to the beach, turquoise sea with a small sailboat, strong midday light. |
| alto-adige-vino-di-montagna | montagna | Steep pergola vineyards on terraces below jagged Dolomite peaks turning pink at sunset, a small church with a pointed bell tower in the middle distance, the vineyard pattern filling the lower half of the frame. |
| friuli-collio-grandi-bianchi | sezione | Cross-section of a hillside: at the top a thin strip of vineyard rows with golden grapes, and below the surface bands of grey marl and sandstone filling two thirds of the frame, fine roots threading down through the layers. |
| puglia-primitivo-negroamaro | figure al lavoro | Late-summer harvest in Puglia: three pickers in straw hats among low bush vines on red earth, crates of dark grapes, a whitewashed farmhouse and olive trees in the distance, blazing ochre light. |
| biologico-biodinamico-naturale | notturno | A vineyard at night under a sky full of stars and a thin crescent moon, rows of vines with wild flowers and herbs growing between them, a copper watering can resting on a wooden post, deep blue and silver tones. |
| solfiti-contiene-solfiti | astratto | Abstract close-up of red wine swirling in a glass seen from directly above, a spiral of deep burgundy and garnet filling the entire frame, with a faint pale-yellow wisp dissolving at one edge. |
| tappo-sughero-vite-sa-di-tappo | natura morta | Close-up still life of several natural wine corks and a waiter's corkscrew scattered on a dark slate surface, one cork cut in half showing its texture, low raking light from the left. |
| barrique-botte-cemento-acciaio | prospettiva | A long barrel cellar in deep perspective: two rows of oak barrels stacked on both sides leading to a far arched doorway full of light, a steel tank and a concrete egg-shaped vat glimpsed in a side room. |
| rosati-italiani-come-si-fanno | sequenza | A row of seven glasses of rosé wine on a sunlit windowsill, all pink: from very pale salmon and onion-skin copper to coral, raspberry pink and light cherry red, morning light shining through them and casting soft pink shadows on the white wall. (stile con palette di rosa/corallo/rame; negativo + green/blue/yellow/white wine) |
| vino-dealcolato-cosa-dice-la-legge | interno laboratorio | A quiet wine laboratory: glass distillation apparatus, a copper column and flasks of red wine on a long workbench, a window looking out on vineyards, soft daylight. |
| rossi-da-bere-freschi | all'aperto | Summer picnic on the grass by a lake, seen from slightly above: a checked blanket, a bottle of light red wine cooling in a bucket of water, two glasses, a basket of cherries, dappled shade from a tree. |
| abbinamenti-falsi-miti | dall'alto | Top-down view of a dinner table with unexpected pairings: a grilled fish next to a glass of red wine, roasted artichokes, a slice of cake beside a glass of dry white, plates in a loose asymmetric arrangement on a dusty-blue tablecloth. |
| vino-e-formaggio-abbinamenti | natura morta fiamminga | Still life on a dark wooden board: a large wedge of aged cheese, a crumbly blue cheese, honey, walnuts and pears, a glass of white wine at the edge of the frame, deep shadowy background like a Dutch still life. |
| come-si-degusta-un-vino | ritratto | A woman seen in profile at a window, eyes closed, smelling a glass of red wine, soft daylight, simple elegant figure, part of her face in shadow. |
| bottiglia-aperta-quanto-dura | interno notturno | A kitchen at night lit only by the open fridge door: a half-full wine bottle with its cork pushed back in on the counter, a glass beside it, moonlight through the window, blue and amber shadows. |
| vino-al-ristorante-carta-dei-vini | interno con figure | Elegant restaurant dining room in the evening, seen from a corner: white tablecloths, candles, a sommelier in a dark apron presenting a bottle to a couple at a table, warm light and deep burgundy walls. |
| scegliere-vino-al-supermercato | prospettiva | A long wine aisle in a supermarket seen in strong perspective, shelves filled with rows of bottles in green, brown and clear glass with plain blank labels, a single empty shopping basket on the floor. |
| dieci-vini-italiani-per-cominciare | dall'alto | Top-down view of a long wooden table with ten glasses of different wines in a row, from pale white through rosé to dark red, with corks, grapes and bread between them, cropped by the frame edges. |
| le-annate-contano-davvero | parete | A tall cellar wall of wine bottles lying in wooden racks, the dusty bottles forming horizontal bands like layers of time, a wooden ladder leaning on the left, a shaft of light from above. |
| glossario-parole-del-vino | dall'alto | Top-down view of an open sketchbook on a desk next to a glass of wine, its pages covered only with small painted drawings of a grape bunch, a barrel, a cork, a vine leaf and a decanter, no writing, a fountain pen beside it. |
| come-si-diventa-sommelier | figura | A young sommelier in a dark apron with a silver tasting cup on a chain around the neck, standing in a candlelit cellar holding a bottle up to the flame to check it, seen from the side. |
| regalare-una-bottiglia | dall'alto | Top-down view of a wine bottle being wrapped as a gift on a table: kraft paper, a silk ribbon, scissors, a sprig of rosemary and a small blank card, loose asymmetric arrangement. |

## Immagine di condivisione

og-vinofilo (assets/img/og-vinofilo.jpg, og:image di home, categorie e 404): calice di rosso con un paesaggio collinare dentro, su un muretto.
Ogni articolo usa la propria illustrazione come og:image e nel JSON-LD. Icona iPhone: assets/apple-touch-icon.png.

## Lezioni
- Evitare etichette, quadranti, quaderni con scritte: il modello inventa testo. Scrivere "plain blank labels", "no writing".
- Le metafore vengono disegnate alla lettera ("like the hand of a clock" → una mano): descrivere la forma, non la metafora.
