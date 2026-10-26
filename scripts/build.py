"""Build the static site from the single editable content file. No dependencies."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parents[1]

def render(data):
    def e(value): return escape(str(value), quote=True)
    def lines(value): return '<br>'.join(e(value).split('\n'))
    name, facebook = e(data['name']), e(data['facebook'])
    phone = data.get('phone')
    primary_url = 'tel:' + phone['e164'] if phone else data['facebook']
    primary_label = 'Call the Shop' if phone else 'Visit Facebook'
    arrow = '<span aria-hidden="true">↗</span>'
    nav = ('<a href="#offerings">Products &amp; services</a>' if data['offerings'] else '')
    nav += '<a href="#about">About</a>' if data.get('about') else ''
    nav += '<a href="#contact">Visit &amp; contact</a>'
    photos = data.get('photos', [])[:4]
    if photos:
        pictures = ''
        for i, p in enumerate(photos):
            loading = 'fetchpriority="high"' if i == 0 else 'loading="lazy"'
            pictures += f'<figure class="slide" {"hidden" if i else ""}><picture><source srcset="{e(p["webp"])}" type="image/webp"><img src="{e(p["fallback"])}" width="{p["width"]}" height="{p["height"]}" alt="{e(p["alt"])}" style="object-position:{e(p.get("focus","50% 50%"))}" {loading}></picture></figure>'
        controls = '' if len(photos)<2 else '<div class="slider-controls" hidden><button type="button" data-prev aria-label="Previous photograph">←</button><span data-position role="status" aria-live="polite">1 / '+str(len(photos))+'</span><button type="button" data-next aria-label="Next photograph">→</button></div>'
        visual = '<div class="photo-slider" aria-label="Shop photographs">'+pictures+controls+'</div>'
    else:
        visual = f'''<aside class="inquiry-panel" aria-labelledby="inquiry-title"><div class="panel-top"><span>START HERE</span>{arrow}</div><h2 id="inquiry-title">What brings<br>you in?</h2><ul><li>A computer question</li><li>A product inquiry</li><li>Planning a visit</li></ul><a href="{facebook}">Ask the shop on Facebook {arrow}</a></aside>'''
    promo = ''
    if data.get('promo'):
        p = data['promo']; image = p['image']
        promo = f'''<section class="repair-promo wrap" aria-labelledby="repair-title"><figure class="repair-photo"><picture><source srcset="{e(image['webp'])}" type="image/webp"><img src="{e(image['fallback'])}" width="{int(image['width'])}" height="{int(image['height'])}" alt="{e(image['alt'])}" loading="lazy"></picture><figcaption>{e(image['caption'])}</figcaption></figure><div class="repair-copy"><p class="eyebrow">{e(p['eyebrow'])}</p><h2 id="repair-title">{lines(p['heading'])}</h2><p>{e(p['description'])}</p><a class="button" href="{e(primary_url)}">{e(p['cta']) if phone else primary_label} {arrow}</a></div></section>'''
    owner_note = ''
    if data.get('owner_note'):
        note = data['owner_note']
        owner_note = f'<aside class="owner-note wrap" id="owner-note" aria-labelledby="owner-note-title"><h2 id="owner-note-title">{e(note["heading"])}</h2><p>{e(note["description"])}</p></aside>'
    offerings = ''
    if data['offerings']:
        rows = ''.join(f'<article class="offering"><span class="offering-number" aria-hidden="true">{i+1:02}</span><h3>{e(item["title"])}</h3><p>{e(item["description"])}</p></article>' for i,item in enumerate(data['offerings']))
        offerings = '<section class="offerings wrap" id="offerings"><div class="section-heading"><p class="eyebrow">WHAT TO ASK ABOUT</p><h2>Find your next step.</h2></div><div class="offering-list">'+rows+'</div><a class="text-link" href="'+facebook+'">Ask about availability '+arrow+'</a></section>'
    about = '' if not data.get('about') else '<section id="about" class="about wrap"><p class="eyebrow">ABOUT THE SHOP</p><h2>'+e(data['about']['heading'])+'</h2><p>'+e(data['about']['description'])+'</p></section>'
    contact_rows = ''
    if phone: contact_rows += f'<div class="contact-row"><span>Call</span><a href="tel:{e(phone["e164"])}">{e(phone["display"])} {arrow}</a></div>'
    if data.get('email'): contact_rows += f'<div class="contact-row"><span>Email</span><a href="mailto:{e(data["email"])}">{e(data["email"])} {arrow}</a></div>'
    if data.get('website'): contact_rows += f'<div class="contact-row"><span>Website</span><a href="{e(data["website"])}">{e(data["website"].removeprefix("https://").rstrip("/"))} {arrow}</a></div>'
    if data.get('address'):
        a=data['address'];contact_rows += f'<div class="contact-row"><span>Visit</span><a href="{e(a["directions"])}">{e(a["display"])} {arrow}</a></div>'
    hours = ''
    if data.get('hours'):
        hours = '<section class="hours" aria-labelledby="hours-title"><h3 id="hours-title">Hours of service</h3><table class="hours-table" aria-labelledby="hours-title"><tbody>'+''.join('<tr><th scope="row">'+e(h['day'])+'</th><td>'+e(h['time'])+'</td></tr>' for h in data['hours'])+'</tbody></table></section>'
    contact_rows += f'<div class="contact-row"><span>Connect</span><a href="{facebook}">The Computer Hub on Facebook {arrow}</a></div>'
    hero=data['hero'];contact=data['contact']
    return f'''<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#faf8f5">
<title>{name} — Computer &amp; technology inquiries</title>
<meta name="description" content="{e(hero['description'])}">
<meta property="og:type" content="website"><meta property="og:title" content="{name}"><meta property="og:description" content="{e(hero['description'])}">
<link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script>
</head><body>
<a class="skip-link" href="#main">Skip to content</a>
<div class="preview-note">Independent design preview · Not the official business website.</div>
<header class="site-header wrap"><a class="brand" href="./" aria-label="{name}, home"><picture><source srcset="assets/logo.webp" type="image/webp"><img src="assets/logo.jpg" width="900" height="375" alt="{name}"></picture></a><button class="menu-button" type="button" aria-expanded="false" aria-controls="main-nav" hidden>Menu <span aria-hidden="true">+</span></button><nav id="main-nav" aria-label="Main navigation">{nav}<a class="nav-contact" href="{e(primary_url)}">{primary_label} {arrow}</a></nav></header>
<main id="main" tabindex="-1"><section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="brand-dash" aria-hidden="true"></span>{e(hero['eyebrow'])}</p><h1>{lines(hero['heading'])}</h1><p class="hero-description">{e(hero['description'])}</p><div class="hero-actions"><a class="button" href="{e(primary_url)}">{primary_label} {arrow}</a><a class="text-link" href="#contact">Contact details <span aria-hidden="true">↓</span></a></div></div>{visual}</section>{promo}{offerings}{about}
<section class="contact-section" id="contact"><div class="wrap contact-layout"><div class="contact-intro"><p class="eyebrow">VISIT &amp; CONTACT</p><h2>{lines(contact['heading'])}</h2><p>{e(contact['description'])}</p>{hours}</div><div class="contact-details">{contact_rows}</div></div></section>
</main>{owner_note}<footer class="wrap"><a class="footer-name" href="./">{name}</a><span>Keep in touch.</span><a href="{facebook}">Facebook {arrow}</a><a href="#main">Back to top ↑</a></footer>
</body></html>'''

def main():
    data=json.loads((ROOT/'content.json').read_text(encoding='utf-8'))
    (ROOT/'index.html').write_text(render(data),encoding='utf-8')
    print('Built index.html from content.json')

if __name__ == '__main__': main()
