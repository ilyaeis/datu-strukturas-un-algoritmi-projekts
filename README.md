# Datu strukturas un algoritmi - gala projekts
## Ilja Safronovs un Aleksejs Peņkovs, RDCM0, 1. kurss, 15. grupa
### Automatizētā papildus lekciju mēklēšana
#### Ko dara musu programma?
Musu jaunizveidota programma palīdz mums automatizēt papildus lekciju mēklēšanu RTU ietvaros, kas patiesībā ir diezgan sarežģits darbs. Protams, tas nav ikdienas problema, tomēr reizi pusgadā, kad katrai grupai, ieskaitot musu, tiek veidots jauns lekciju saraksts, mes atkal saskaramies ar vajadzību manuāli mēklēt jaunās studiju iespējas. Tā kā tas ir laika un resursu ziņā ļoti apjomigs darbs, mes izvēlējamies tieši šo procesu musu automatizācijas projekta izstrādē.
Ar musu koda palidzību ikviens lietotājs var atrast sev piemērotas papildus lekcijas. Sākumā ir jādefinē savu pamatsarakstu, lai papildus lekcijas neskartu un netraucētu pamatmācības, un tad programma izveidos sarakstu ar visiem pieejamiem papildus kursu variantiem. Tad lietotājs var izdzēst no saraksta liekus elementus un dabūt finala rezultātu.
### Kā darbojas musu programma?
Sākuma lietotājam ir jāievada savas grupas parametrus, lai programma varetu izgūt no nodarbibas.rtu.lv lietotnes pamatsarakstu. Tad programma automatiski pārmēklēs visu lietotni un atradis visas lekcijas, kuras atbilst šādiem kritērijiem:
- lekcija netraucē pamatmācībam, kas ir papildus lekcijas laiks nesakrīt ar pamalekciju laikiem
- lekcija notiek uzreiz pirms vai pēc pamatlekcijam, lai litotājam neterētu lieko laiku gaidīšanai
- lekcijā piedalās vismaz 2 grupas (ja būtu tikai 1 grupa, visi zinātu, ka mes esam svešinieki)
- lekcija atšķiras no lietotāja pamatsaraksta (jo nav jēgas atkartoti apmēklēt tadas pašan nodarbības)
- visas nodarbības tajā priekšmetā ir pieejamas apmeklēšanai, jeb neviena no nodarbībam nedeas griezumā nepārklājas ar lietotāja pamatsarakstu
Ja lekcija neatbilst kaut vienam no kritērijiem, tā netiek atzīta par derīgu, savukārt, jā lekcija visiem kritērijiematbilst, tā tiek ierakstīta teksta failā.
