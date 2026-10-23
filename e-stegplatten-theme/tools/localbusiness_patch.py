#!/usr/bin/env python3
"""Patcht snippets/microdata-schema.liquid (aus Shopify geladen): LocalBusiness-Schema auf der Startseite,
Breadcrumb-Fix für Artikel (Position 3 = Artikeltitel statt Blogtitel).

  localbusiness_patch.py <microdata-schema.liquid (Original)> <Ausgabe>"""
import pathlib, sys

src = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')

old_bc = '''            "name": {{ blog.title | json }},
            "item": "{{ shop.url }}{{ article.url }}"'''
assert src.count(old_bc) == 1, 'Breadcrumb-Stelle nicht gefunden'
src = src.replace(old_bc, '''            "name": {{ article.title | json }},
            "item": "{{ shop.url }}{{ article.url }}"''')

anchor = "  {%- comment -%}e-Stegplatten: FAQPage-Schema (AEO/GEO)"
assert src.count(anchor) == 1, 'FAQ-Anker nicht gefunden'
LB = '''  {%- comment -%}e-Stegplatten: LocalBusiness (Fachhandel in Gelsenkirchen) – Adresse/Telefon/Öffnungszeiten für Google Maps und KI-Suche. Maps-Link ("hasMap") ergänzen, sobald er vorliegt.{%- endcomment -%}
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": ["LocalBusiness", "HardwareStore"],
    "@id": "{{ shop.url }}/#local",
    "name": "e-Stegplatten (TSZ GmbH)",
    "alternateName": "e-stegplatten.de",
    "legalName": "TSZ GmbH",
    "url": "{{ shop.url }}",
    "telephone": "+49 209 51307834",
    "email": "info@e-stegplatten.de",
    {%- if shop.brand.logo -%}
    "image": {{ shop.brand.logo | image_url: width: 600 | prepend: "https:" | json }},
    "logo": {{ shop.brand.logo | image_url: width: 600 | prepend: "https:" | json }},
    {%- endif -%}
    "description": "Fachhandel für Doppelstegplatten, Hohlkammerplatten, Wellplatten und Alu-Terrassenüberdachungen nach Maß. Zuschnitt millimetergenau, Beratung Mo–Fr 8–17 Uhr.",
    "address": {
      "@type": "PostalAddress",
      "streetAddress": "Magdeburger Straße 37",
      "postalCode": "45881",
      "addressLocality": "Gelsenkirchen",
      "addressRegion": "Nordrhein-Westfalen",
      "addressCountry": "DE"
    },
    "openingHoursSpecification": [{
      "@type": "OpeningHoursSpecification",
      "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
      "opens": "08:00",
      "closes": "17:00"
    }],
    "areaServed": [{"@type": "Country", "name": "Deutschland"}, {"@type": "Country", "name": "Österreich"}],
    "currenciesAccepted": "EUR",
    "paymentAccepted": "PayPal, Klarna, Kreditkarte, Zahlung bei Lieferung",
    "priceRange": "€€",
    "foundingDate": "2013",
    "sameAs": [
      {%- for social_link in shop.brand.metafields.social_links -%}
        {{- social_link.last.value | json -}}{%- unless forloop.last -%},{%- endunless -%}
      {%- endfor -%}
    ]
  }
  </script>

'''
src = src.replace(anchor, LB + anchor)
pathlib.Path(sys.argv[2]).write_text(src, encoding='utf-8')
print('ok', len(src.encode('utf-8')))
