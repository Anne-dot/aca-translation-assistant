#!/usr/bin/env python3
"""
EKI Terminibaasi Koguja

Kogub termineid Eesti Keele Instituudi (EKI) Sõnaveeb terminibaasidest.
Salvestab terminid JSON formaati koos viidetega allikale.

Kasutamine:
    python3 eki_koguja.py <terminibaasi_kood>

Näited:
    python3 eki_koguja.py skt        # Skeemiteraapia
    python3 eki_koguja.py dkt        # DKT/DBT
    python3 eki_koguja.py kriis      # Kriisinõustamine
    python3 eki_koguja.py TAI        # Tervisesõnastik
"""

import requests
import json
import sys
import time
from datetime import datetime
from typing import List, Dict
from html.parser import HTMLParser
import urllib.parse
from bs4 import BeautifulSoup

# EKI terminibaasid
TERMINIBAASID = {
    'skt': {
        'nimi': 'Skeemiteraapia terminisõnastik',
        'url': 'https://sonaveeb.ee/ds/skt',
        'kontakt': 'Kaia Kastepõld-Tõrs (skeemiteraapia@gmail.com)'
    },
    'dkt': {
        'nimi': 'Dialektilise käitumisteraapia terminibaas',
        'url': 'https://sonaveeb.ee/ds/dkt',
        'kontakt': 'dkteesti@gmail.com'
    },
    'kriis': {
        'nimi': 'Kriisinõustamise terminibaas',
        'url': 'https://sonaveeb.ee/ds/kriis',
        'kontakt': 'Kirsti Talu (kirstit@gmail.com)'
    },
    'TAI': {
        'nimi': 'Tervisesõnastik',
        'url': 'https://sonaveeb.ee/ds/TAI',
        'kontakt': 'Ruth Erm (ruth.erm@tai.ee)'
    }
}

# Kõik võimalikud tähed (eesti + vene)
KOIK_TAHED = [
    # Eesti tähed
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'õ', 'ä', 'ö', 'ü',
    # Vene tähed (mõned terminibaasid sisaldavad neid)
    'а', 'б', 'в', 'г', 'д', 'е', 'ж', 'з', 'и', 'к', 'л', 'м', 'н',
    'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я'
]


class TerminParser(HTMLParser):
    """HTML parser terminite ekstrakteerimiseks Sõnaveeb lehtedelt"""

    def __init__(self, terminibaas_kood: str):
        super().__init__()
        self.terminibaas = terminibaas_kood
        self.terminid = []
        self.current_link = None
        self.in_term_link = False

    def handle_starttag(self, tag, attrs):
        """Leia terminite lingid"""
        if tag == 'a':
            attrs_dict = dict(attrs)
            href = attrs_dict.get('href', '')

            # Kontrolli, kas see on termini link
            # Formaat: /search/unif/dlall/TERMINIBAAS/TERMIN
            if f'/search/unif/dlall/{self.terminibaas}/' in href:
                self.in_term_link = True
                self.current_link = href

    def handle_data(self, data):
        """Ekstrakteeri termini tekst"""
        if self.in_term_link and data.strip():
            self.terminid.append({
                'termin': data.strip(),
                'link': f"https://sonaveeb.ee{self.current_link}"
            })

    def handle_endtag(self, tag):
        """Lõpeta termini lugemine"""
        if tag == 'a':
            self.in_term_link = False
            self.current_link = None


def leia_saadaolevad_tahed(terminibaas: str) -> List[str]:
    """
    Leiab, millised tähed on terminibaasis saadaval

    Args:
        terminibaas: Terminibaasi kood (nt 'skt')

    Returns:
        Nimekiri saadaolevatest tähtedest
    """
    url = f"https://sonaveeb.ee/ds/{terminibaas}"

    try:
        print(f"  🔍 Kontrollin saadaolevaid tähti: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Otsi tähte-linke HTML-ist
        # Formaat: <a href="/ds/TERMINIBAAS/TAHT">
        import re
        pattern = rf'href="/ds/{terminibaas}/([^"]+)"'
        matches = re.findall(pattern, response.text)

        tahed = []
        for href_taht in matches:
            # Dekodeeri URL-kodeeritud täht
            taht = url_decode_estonian(href_taht)
            # Võta ainult ühe tähe pikkused (ei ole "search" vms)
            # Säilita ka suurtähed (EKI kasutab mõnikord A, mõnikord a)
            if len(taht) == 1 and (taht.lower() in KOIK_TAHED or taht in KOIK_TAHED):
                tahed.append(taht)

        # Eemalda duplikaadid ja sorteeri
        tahed = sorted(list(set(tahed)))

        print(f"    ✓ Leitud {len(tahed)} tähte: {' '.join(tahed)}")
        return tahed

    except requests.exceptions.RequestException as e:
        print(f"    ⚠️  Viga tähtede leidmisel: {e}")
        print(f"    ℹ️  Kasutan kõiki tähti")
        return KOIK_TAHED


def url_decode_estonian(text: str) -> str:
    """
    Dekodeeri URL-kodeeritud eesti tähed

    Args:
        text: URL-kodeeritud tekst

    Returns:
        Dekodeeritud tekst
    """
    return urllib.parse.unquote(text)


def kogu_termini_detailid(termin_link: str) -> Dict:
    """
    Kogub termini täielikud andmed EKI lehelt

    Args:
        termin_link: Link termini lehele

    Returns:
        Sõnastik termini detailidega
    """
    try:
        response = requests.get(termin_link, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        detailid = {
            'keel': None,
            'synonyymid': [],
            'definitsioon': None
        }

        # Leia homonym-list-item
        homonym = soup.find('li', class_='homonym-list-item')
        if homonym:
            # Leia keelekood
            lang_code = homonym.find('span', class_='lang-code')
            if lang_code:
                detailid['keel'] = lang_code.get('title', lang_code.get_text(strip=True))

            # Leia sünonüümid
            matches = homonym.find('span', class_='homonym__matches')
            if matches:
                synonyymid_text = matches.get_text(strip=True)
                if synonyymid_text:
                    detailid['synonyymid'] = [s.strip() for s in synonyymid_text.split(',')]

            # Leia definitsioon
            definition = homonym.find('p')
            if definition:
                detailid['definitsioon'] = definition.get_text(strip=True)

        return detailid

    except Exception as e:
        print(f"      ⚠️  Detailide laadimisel viga: {e}")
        return {
            'keel': None,
            'synonyymid': [],
            'definitsioon': None
        }


def kogu_terminid_tahelt(terminibaas: str, taht: str, kogu_detailid: bool = True) -> List[Dict]:
    """
    Kogub terminid ühelt tähelt

    Args:
        terminibaas: Terminibaasi kood (nt 'skt')
        taht: Täht (nt 'a')
        kogu_detailid: Kas koguda ka termini detailid (aeglasem)

    Returns:
        Nimekiri terminitest koos kõigi andmetega
    """
    url = f"https://sonaveeb.ee/ds/{terminibaas}/{taht}"

    try:
        print(f"  Laen: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Parsi HTML
        parser = TerminParser(terminibaas)
        parser.feed(response.text)

        # Dekodeeri eesti tähed ja kogu detailid
        terminid = []
        for item in parser.terminid:
            termin_nimi = url_decode_estonian(item['termin'])
            termin_link = item['link']

            termin_dict = {
                'termin': termin_nimi,
                'link': termin_link,
                'taht': taht
            }

            # Kui soovitakse, kogu ka detailid
            if kogu_detailid:
                print(f"    → {termin_nimi}", end='', flush=True)
                detailid = kogu_termini_detailid(termin_link)
                termin_dict.update(detailid)

                # Näita, mis leiti
                if detailid.get('definitsioon'):
                    def_preview = detailid['definitsioon'][:50] + '...' if len(detailid['definitsioon']) > 50 else detailid['definitsioon']
                    print(f" ✓ ({detailid.get('keel', '?')}) {def_preview}")
                else:
                    print(f" ⚠ (definitsioon puudub)")

                # Väike paus, et serverit mitte üle koormata
                time.sleep(0.3)

            terminid.append(termin_dict)

        print(f"    ✓ Leitud {len(terminid)} terminit" + (" (koos detailidega)" if kogu_detailid else ""))
        return terminid

    except requests.exceptions.RequestException as e:
        print(f"    ✗ Viga: {e}")
        return []


def kogu_koik_terminid(terminibaas_kood: str) -> Dict:
    """
    Kogub kõik terminid terminibaasist

    Args:
        terminibaas_kood: Terminibaasi kood (nt 'skt', 'dkt')

    Returns:
        Sõnastik kõigi terminitega ja metaandmetega
    """
    if terminibaas_kood not in TERMINIBAASID:
        print(f"❌ Viga: Tundmatu terminibaas '{terminibaas_kood}'")
        print(f"Võimalikud valikud: {', '.join(TERMINIBAASID.keys())}")
        sys.exit(1)

    info = TERMINIBAASID[terminibaas_kood]
    print(f"\n🔍 Kogun termineid: {info['nimi']}")
    print(f"📍 URL: {info['url']}")
    print(f"📧 Kontakt: {info['kontakt']}\n")

    # Leia, millised tähed on saadaval
    saadaolevad_tahed = leia_saadaolevad_tahed(terminibaas_kood)
    print()

    koik_terminid = []

    # Käi läbi ainult saadaolevad tähed
    for taht in saadaolevad_tahed:
        terminid = kogu_terminid_tahelt(terminibaas_kood, taht)
        koik_terminid.extend(terminid)

        # Väike paus, et serverit mitte üle koormata
        time.sleep(0.5)

    # Eemalda duplikaadid (kui on)
    unikaalsed = {}
    for t in koik_terminid:
        if t['termin'] not in unikaalsed:
            unikaalsed[t['termin']] = t

    koik_terminid = list(unikaalsed.values())

    # Sorteeri tähestiku järgi
    koik_terminid.sort(key=lambda x: x['termin'].lower())

    print(f"\n✅ Kokku kogutud: {len(koik_terminid)} unikaalset terminit")

    # Koosta tulemus koos metaandmetega
    tulemus = {
        'metaandmed': {
            'terminibaas_kood': terminibaas_kood,
            'terminibaas_nimi': info['nimi'],
            'terminibaas_url': info['url'],
            'kontakt': info['kontakt'],
            'kogumise_kuupaev': datetime.now().isoformat(),
            'terminite_arv': len(koik_terminid)
        },
        'terminid': koik_terminid
    }

    return tulemus


def salvesta_json(andmed: Dict, terminibaas_kood: str) -> str:
    """
    Salvestab terminid JSON faili

    Args:
        andmed: Terminite andmed koos metaandmetega
        terminibaas_kood: Terminibaasi kood

    Returns:
        Salvestatud faili tee
    """
    import os

    # Loo väljundi kaust kui vaja
    output_dir = '../data/eki_terminid'
    os.makedirs(output_dir, exist_ok=True)

    # Genereeri failinimi
    kuupaev = datetime.now().strftime('%Y%m%d')
    failinimi = f"{output_dir}/eki_{terminibaas_kood}_{kuupaev}.json"

    # Salvesta JSON
    with open(failinimi, 'w', encoding='utf-8') as f:
        json.dump(andmed, f, ensure_ascii=False, indent=2)

    print(f"\n💾 Salvestatud: {failinimi}")

    return failinimi


def main():
    """Peamine funktsioon"""

    if len(sys.argv) < 2:
        print("Kasutamine: python3 eki_koguja.py <terminibaasi_kood>")
        print(f"\nVõimalikud terminibaasid:")
        for kood, info in TERMINIBAASID.items():
            print(f"  {kood:6} - {info['nimi']}")
        sys.exit(1)

    terminibaas_kood = sys.argv[1]

    # Kogu terminid
    andmed = kogu_koik_terminid(terminibaas_kood)

    # Salvesta JSON
    failitee = salvesta_json(andmed, terminibaas_kood)

    print(f"\n✅ Valmis!")
    print(f"📊 Kogutud {andmed['metaandmed']['terminite_arv']} terminit")
    print(f"📁 Fail: {failitee}")


if __name__ == '__main__':
    main()
