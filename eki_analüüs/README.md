# EKI Veebilehe Analüüs

Selles kaustas on materjalid EKI Sõnaveeb API ja veebilehe struktuuri analüüsimiseks.

## Eesmärk

Uurida, kuidas EKI Sõnaveeb laeb terminite andmeid, et saaksime need automaatselt koguda koos kogu sisuga:
- Definitsioonid
- Ingliskeelsed vasted
- Sünonüümid
- Näited
- Allikad

## Testimine

1. Ava brauser Developer Tools (F12)
2. Mine Network tabile
3. Ava EKI termin: https://sonaveeb.ee/search/unif/dlall/kriis/depressioon
4. Vaata, millised API päringud tehakse
5. Kopeeri siia:
   - API URL-id
   - Request headers
   - Response andmed

## Testitud URL-id

### Otse lehel
- ✅ https://sonaveeb.ee/search/unif/dlall/kriis/depressioon
  - Kasutab JavaScript-i andmete laadimiseks
  - HTML leht ise ei sisalda terminite sisu

### API katsetused (404)
- ❌ https://sonaveeb.ee/api/search/unif/dlall/kriis/depressioon
- ❌ https://sonaveeb.ee/wordweb/api/data/search/kriis/depressioon

### Järgmine samm
Uurida F12 Network tabist, mis päringud tegelikult tehakse.

---

**Kuupäev:** 2025-10-12
