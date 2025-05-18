# Datu strukturas un algoritmi - gala projekts
## Ilja Safronovs un Aleksejs Peņkovs, RDCM0, 1. kurss, 15. grupa
### Automatizētā papildus lekciju mēklēšana
#### Ko dara musu programma?
  Musu jaunizveidota programma palīdz mums automatizēt papildus lekciju mēklēšanu RTU ietvaros, kas patiesībā ir diezgan sarežģits darbs. Protams, tas nav ikdienas problema, tomēr reizi pusgadā, kad katrai grupai tiek veidots jauns lekciju saraksts, mes atkal saskaramies ar vajadzību mēklēt jaunās studiju iespējas, jo esam aktīvi cilvēki un mēģinam daudzpusīgi attistīties. Tā kā tas ir laika un resursu ziņā ļoti apjomigs darbs, mes izvēlējamies tieši šo procesu musu automatizācijas projekta izstrādē.

  Ar musu koda palidzību ikviens lietotājs var atrast sev piemērotas papildus lekcijas RTU ietvaros. Sākumā ir jādefinē savu pamatsarakstu, lai papildus lekcijas neskartu un netraucētu pamatmācības, un tad programma izveidos sarakstu ar visiem pieejamiem papildus kursu variantiem. 

  Tas ļoti atvieglo musu darbu, jo katru reizi manuāli pārskatīt katru studijas virzienu, gadu un grupu visās fakultātēs tiešām ir milzigs darbs. Savukārt musu programma ļauj lietotājam uzreiz dabūt filtrētu sarakstu tikai ar derīgiem lekciju variantiem. Tad jau manuālā režimā katrs lietotājs var iziet cauri salīdzinoši mazam sarakstam un ātri izvēlēties finala variantu.
### Kā darbojas musu programma?
  Sākuma lietotājam ir jāievada nedaudz informācijas par savu grupu un mēklēšanas diapazonu, lai programma varetu izgūt no nodarbibas.rtu.lv lietotāja pamatsarakstu un veselu kaudzi ar papildus lekcijam. Tad programma automatiski pārmēklēs visas lekcijas un atradīs tadas, kuras atbilst šādiem kritērijiem:
- lekcija netraucē pamatmācībam, kas ir papildus lekcijas laiks nesakrīt ar pamalekciju laikiem;
- lekcija atšķiras no lietotāja pamatsaraksta (jo nav jēgas atkartoti apmēklēt tadas pašan nodarbības);
- visas nodarbības tajā priekšmetā ir pieejamas apmeklēšanai, jeb neviena no nodarbībam nedeļas griezumā nepārklājas ar lietotāja pamatsarakstu (jo nav jegas tikai daļēji apgūt lekciju materiālu).

  Ja lekcija neatbilst kaut vienam no kritērijiem, tā netiek atzīta par derīgu, savukārt, jā lekcija visiem kritērijiem atbilst, tā tiek ierakstīta Excel failā tabulas veidā. Tad jau manuālā režīmā lietotājs ar parasto filtru izmantošanu ātri un vienkārši var atlasīt pēc nedeļam (jo RTU ir 2 nedeļu grafiks), dienam, laikam, grupu skaita un nosaukuma, lai izvēlēties sev visatbilstošāko. Protams, tabulā tiek attēlota 1 grupa, kurai sarakstā ir šāda lekcija, lai lietotājs varētu pārbaudīt lekcijas esamību reālajā sarakstā un pārliecināties musu programmas pareizībā.
### Kādas bibliotēkas tika izmantotas musu programmā un kāpēc?
- "selenium", lai emitēt lietotāja uzvēdību nodarbibas.rtu.lv mājaslapā;
- "json", lai saglabat datus .json failā un izmantot to talākai apstrādei;
- "time", lai veidot pauzes starp pieprasījumiem no tīmekļa vietnes un nepaaugstināt dažādu kļudu risku;
- "datetime", lai operet ar datumiem un laikiem lekciju apstrādes un filtrēšanas procesā;
- "pandas", lai sagatavot gala rezultātu tabulas formatā un ierakstīt to Excel failā;
- "collections", lai izmantot ļoti ērtu "defaultdict" datu struktūru.
### Kādas datu struktūras tika izmantotas musu programmā un kāpēc?
- Galvenā datu struktūra ir "dictionary", lai saglabat datus vairakās dimencijās, kārtojot pēc nedeļam, dienam, laikiem, lekciju nosaukumiem, grupam un citiem parametriem, jo dictionary stradā uz {key: value} struktūras, kas palīdz vieglāk sagalabāt datus un operēt ar tiem;
- Kā arī bija izmantots "collections.defaultdict" jeb uzlabots "dictionary", lai ērtāk un vienkāršāk veidot dictionary struktūru un izvairīties no kļūsam;
- "pandas.DataFrame", lai atvieglot tabulas veidošanas procesu un vieglāk parnest datus uz Excel failu;
- Protams tika izmantotas citas datu struktūras, piemēram, masīvi.
### Kopsavilkums
  Programma der visiem RTU studentiem un stradās līdz brīdim, kad nodarbibas.rtu.lv nomainīs lietotnes izkārtojumu vai struktūru. Pati programma aizņēm daudz laika īstenošanas procesā, tomēŗ tā tiešām ļoti atvieglo papildus lekciju mēklēšanas procesu, jo lietotājam vajag iedot programmai pavisam nedaudz informācijas un vienkārši uzgaidīt kādu laiku. Izstrādes procesā tika izmantotas zināšanas, kuras tika iegūtas RTU lekciju laikā, kā arī salīdzinoši neliela AI palīdzība.
