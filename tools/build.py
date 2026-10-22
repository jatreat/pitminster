#!/usr/bin/env python3
"""Assembles the site's pages from the shared header/footer and the page bodies below.

Run:  python3 tools/build.py
Output: public/*.html (plain HTML; you can also edit those files directly if you prefer).
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from emblem import mark, seal

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Libre+Caslon+Display&family=Libre+Caslon+Text:ital,wght@0,400;0,700;1,400&display=swap">'

NAV = [
    ("church.html", "The church"),
    ("village.html", "The village"),
    ("across.html", "Across the water"),
    ("games.html", "Games"),
    ("wall.html", "Family wall"),
    ("visit.html", "Visit &amp; give"),
    ("contact.html", "Contact"),
]


def head(title, desc, canonical, extra=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://pitminsterchurchonline.org/{canonical}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://pitminsterchurchonline.org/images/church-at-dusk.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
{FONTS}
<link rel="stylesheet" href="assets/site.css">
<script>document.documentElement.classList.add("js")</script>
{extra}
</head>
<body>
"""


def header(current):
    items = "".join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if href == current else ""}>{label}</a></li>'
        for href, label in NAV
    )
    return f"""<header class="masthead"><div class="wrap">
<a class="brand" href="index.html" aria-label="Friends of Pitminster, home">{mark("hd", "")}<span class="brand-name">Friends of Pitminster</span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
<nav class="nav" id="site-nav" aria-label="Main"><ul>{items}</ul></nav>
</div></header>
"""


FOOTER = f"""<footer class="foot"><div class="wrap">
<a class="foot-seal" href="index.html" aria-label="Friends of Pitminster, home">{seal("ft")}</a>
<div>
<p>Friends of Pitminster is an independent community site kept by friends of the village on both sides of the Atlantic. It is not the parish's official site. For services, parish business and giving, the parish's own channels are <a href="https://achurchnearyou.com/church/11367">A Church Near You</a> and the <a href="https://blackdown.org.uk">Blackdown Benefice</a>.</p>
<p>Photographs are by the editors and by Geograph contributors under CC BY-SA 2.0. Credits, sources and a privacy note are on the <a href="about.html">About</a> page.</p>
</div>
<ul>
<li><a href="about.html">About this site</a></li>
<li><a href="contact.html">Contact the editors</a></li>
<li><a href="index.html">pitminsterchurchonline.org</a></li>
</ul>
</div></footer>
<script src="assets/site.js" defer></script>
</body>
</html>
"""


def page(filename, title, desc, body, extra_head=""):
    html = head(title, desc, filename, extra_head) + header(filename) + body + FOOTER
    (PUBLIC / filename).write_text(html, encoding="utf-8")
    print("wrote", filename, len(html))


# ---------------------------------------------------------------- content

EXAMPLE_POSTS = """<article class="post" data-example>
<header><b>The editors</b><span>Pitminster and Maine</span></header>
<p>This is what a note on the wall looks like. Say who you are, which family you belong to if any, where you have ended up, and what you would like to find. Notes are read by a person before they appear.</p>
<p class="ex">Example note</p>
</article>
<article class="post" data-example>
<header><b>The editors</b><span>on the lane by the church</span></header>
<p>Villagers are welcome here too: a date for the diary, a photograph from a drawer, a correction to something on these pages. The site is only as good as the people who write on it.</p>
<p class="ex">Example note</p>
</article>"""

INDEX = f"""
<section class="hero">
<img class="hero-img" src="images/church-at-dusk.jpg" srcset="images/church-at-dusk-800.jpg 800w, images/church-at-dusk.jpg 1400w, images/church-at-dusk-2200.jpg 2200w" sizes="100vw" width="2200" height="1650" alt="The church of St Andrew and St Mary, Pitminster, at dusk, seen across the churchyard: the tower rising to its octagon and lead spire, a lit cloud behind" fetchpriority="high">
<div class="hero-copy"><div class="wrap">
<h1>A church of 1300, a village named in 938, and the families who sailed from it.</h1>
<p class="hero-credit">St Andrew &amp; St Mary from the churchyard, a June evening in 2026</p>
</div></div>
</section>

<section class="intro"><div class="wrap">
<div class="intro-text">
<p class="lede">Pitminster sits four miles south of Taunton, where the Vale of Taunton Deane climbs into the Blackdown Hills. Its church has stood since about 1300. Its name was already old when King Athelstan gave the estate to the Bishop of Winchester in 938. And in the 1630s one of its families crossed the Atlantic and became, by way of Connecticut, one of the large families of America.</p>
<p>This site is for the people who live here, the people who worship here, and the people far away who come back looking for a name on a brass.</p>
</div>
<ul class="intro-links">
<li><a href="church.html">The church</a></li>
<li><a href="village.html">The village</a></li>
<li><a href="across.html">The families who sailed</a></li>
<li><a href="visit.html#give">Give to the church</a></li>
</ul>
</div></section>

<section class="band"><div class="wrap doors">
<article class="door">
<img src="images/church-winter-light.jpg" width="480" height="640" alt="The church tower and spire in low winter sunlight" loading="lazy">
<h2>The church</h2>
<p>Grade I listed and begun around 1300 on the site of a Saxon church. A lead spire that is said to lean, a fifteenth-century font, a Jacobean pulpit with its canopy, and three generations of the Coles family lying in the chancel.</p>
<a class="more" href="church.html">Inside the church</a>
</article>
<article class="door">
<img src="images/blagdon-hill-from-southwest.jpg" width="640" height="422" alt="Blagdon Hill village seen across fields from the south-west, with the Vale of Taunton Deane beyond" loading="lazy">
<h2>The village</h2>
<p>Pitminster, Blagdon Hill, Angersleigh and the hamlets between them. A bishop's deer park where King John hunted, a Tudor house at Poundisford, a hymn written for a Sunday school, and a pageant that put a thousand years of it on stage in 1976.</p>
<a class="more" href="village.html">Around the village</a>
</article>
<article class="door">
<img src="images/view-east-angersleigh-road.jpg" width="640" height="427" alt="Fields and hedges looking east from the Angersleigh road" loading="lazy">
<h2>Across the water</h2>
<p>Richard Trott was baptised here in 1584, married here in 1615, and by 1637 had sailed for New England. His family became the Treats of Connecticut, Massachusetts and Maine, and they have been coming back ever since: a brass in 1902, a window in 1989, a reunion in 2026.</p>
<a class="more" href="across.html">The Treats and their cousins</a>
</article>
</div></section>

<section class="strip"><div class="wrap">
<div>
<div class="rule"></div>
<h2>On the family wall</h2>
<p>Notes from descendants, villagers and visitors. Anyone can write; a person reads each note before it appears.</p>
<div class="wall" id="home-wall">{EXAMPLE_POSTS}</div>
<p style="margin-top:1.25rem"><a class="btn" href="wall.html">Leave a note</a></p>
</div>
<div>
<div class="rule"></div>
<h2>Visit, worship, give</h2>
<p>The church is on Church Lane, Pitminster, Taunton TA3 7AZ. Holy Communion is held on the fourth Sunday of the month at 10.30am, shared with St Nicholas, Corfe; the rest of the month the benefice's services move among its six churches, and <a href="https://achurchnearyou.com/church/11367">A Church Near You</a> has the current list.</p>
<p>The building is looked after by its parish, which has to find the money to keep a seven-hundred-year-old church standing. Gifts go to the parish directly, never through this site.</p>
<p style="margin-top:1.25rem"><a class="btn btn-quiet" href="visit.html">Plan a visit</a> &nbsp; <a class="btn" href="visit.html#give">How to give</a></p>
<hr>
<h2 style="font-size:1.35rem">Play the family's history</h2>
<p><a href="games.html">Treatopoly</a> runs the Treats' four centuries around a board, from Set Sail 1637 to Return to Pitminster, and plays online with family in other houses. <a href="games.html">The Treat Trail</a> makes the same journey the hard way, one stop and one ration at a time.</p>
</div>
</div></section>
"""

CHURCH = """
<section class="pagehead has-photo"><div class="wrap">
<div class="rule"></div>
<h1>The church of St Andrew &amp; St Mary</h1>
<p class="lede">Built around 1300 on the site of a Saxon church, enlarged in the fifteenth century, restored by the Victorians and twice since, and still in use every month. Grade I listed since 1955.</p>
<figure>
<img src="images/church-from-southeast.jpg" width="640" height="467" alt="The church from the south-east, with the chancel, the south aisle and porch, and the tower and spire behind" fetchpriority="high">
<figcaption>From the south-east: chancel, south aisle and porch, and the tower rising to its octagon and spire. Photograph by Mike Searle, CC BY-SA 2.0.</figcaption>
</figure>
</div></section>

<section class="page"><div class="wrap">
<div class="prose">
<h2>Seven centuries of building</h2>
<p>The church was built around 1300, on the site of an older Saxon church, and enlarged in the fifteenth century. It is built of the local grey stone, laid as random rubble, with the windows, doorways and buttresses dressed in golden Ham stone from Ham Hill to the east. The roofs are slate; the spire and the south porch are covered in lead.</p>
<p>The Victorians were thorough with it. In 1869 Sir George Gilbert Scott rebuilt the north aisle, the south porch and the north-west chapel, replaced the clerestory windows and rebuilt the chancel arch. W. D. Caröe restored the chancel in 1937, and the Lady chapel was restored in 1979. What survives untouched is still considerable: the three-bay arcades of clustered shafts, the south arcade's arches still in the original grey sandstone, the fifteenth-century compartment ceiling under the tower, and a handful of early sixteenth-century bench ends among the Victorian ones.</p>

<h2>The tower and the leaning spire</h2>
<p>The west tower is square for two stages and then becomes an octagon, the change marked by a quatrefoil parapet, and the octagon carries a lead-covered spire. Spires are unusual in this corner of Somerset, where church towers are square and flat-topped, and the spire is the first thing you see of Pitminster from the lanes to the south. It is said to lean. When the village staged its own history as a pageant in 1976, one episode recalled the Great Storm of 1703 that damaged it.</p>
<figure>
<img src="images/church-winter-light.jpg" width="480" height="640" alt="The tower and lead spire of the church in low winter sunlight, seen from the churchyard" loading="lazy" style="max-width:min(24rem,100%)">
<figcaption>The tower from the churchyard. Photograph by Derek Harper, CC BY-SA 2.0.</figcaption>
</figure>

<h2>Inside</h2>
<figure>
<img src="images/nave-roof.jpg" width="1400" height="310" alt="The ribbed wagon roof of the nave, looking east over the pulpit canopy to the chancel arch and the east window" loading="lazy">
<figcaption>The nave roof, looking east over the pulpit's canopy to the chancel. June 2026.</figcaption>
</figure>
<p>The oldest thing in the church is the font: fifteenth century, octagonal, cut from Beer stone, its quatrefoil panels carved with St George and St James of Compostela, with a later panel of Christ. The pulpit is early seventeenth century and one of the few in the district to keep its canopy; its sounding board came from the Bluecoat school at Frome and was probably the work of London craftsmen. Either side of the chancel arch are the turrets of the rood stair, a spiral stair that once led to the rood loft of about 1400. The loft itself went at the Reformation, as most did. By the organ is linenfold panelling; over the chancel, a ceiled and ribbed barrel vault.</p>
<p>Fragments of medieval glass survive in the upper lights of the Lady chapel's north window. The rest of the glass is late Victorian and later: the Lady chapel's east window of 1894 and west window of 1904, both by Keape, and the chancel's east window, which had decayed so badly by the 1950s that the church commissioned a new one. Jane Grey's <i>The Calling of Andrew</i> was installed in 1989, with help from American descendants of Pitminster families. It shows Christ calling Andrew from his nets: follow me, and I will make you fishers of men.</p>

<h2>The Coles tombs</h2>
<p>Three generations of the Coles family, who held the former priory lands at Barton after the Dissolution, lie in the church. Humphrey Coles, who died in 1570, is in the north-west chapel, where his effigy was moved. In the chancel are John Coles (died 1607) with his wife Ann, their monument repainted in 1937, and John Coles (died 1627) with Elizabeth Wyndham (died 1634), an infant lying at her feet. Around them are early nineteenth-century tablets, mostly to the Vibart family, and two hatchments. The brass lectern was given in memory of William Amasa Copp, who died in 1901. In the churchyard, about six metres east of the chancel, the North family monument is listed in its own right.</p>
<figure>
<img src="images/coles-tomb.jpg" width="640" height="427" alt="Alabaster effigies of John Coles and his wife lying on a tomb chest in the chancel, with a small effigy of an infant at her feet" loading="lazy">
<figcaption>John Coles and his wife, with the infant at her feet. Photograph by Mike Searle, CC BY-SA 2.0.</figcaption>
</figure>

<h2>The American brass</h2>
<figure>
<img src="images/treat-brass.jpg" width="1400" height="791" alt="The brass tablet of 1902 in memory of Richard Treat, alias Trott, baptised in this church in 1584, and his son Robert, Governor of Connecticut, erected by their descendant John Harvey Treat of America" loading="lazy">
<figcaption>The brass of 1902, on the wall of the church. June 2026.</figcaption>
</figure>
<p>In the church is a brass tablet placed in 1902 by John Harvey Treat of Lawrence, Massachusetts, the family historian who had published <i>The Treat Family</i> nine years earlier. It commemorates Richard Treat, baptised in this church in 1584, who sailed for New England in 1637 and was named in the Royal Charter of Connecticut, and his son Robert, who became governor of that colony. Their story, and the village's other American connections, are told on the <a href="across.html">Across the water</a> page.</p>

<h2>The church today</h2>
<p>St Andrew and St Mary is one of the six churches of the Blackdown Benefice, in the Somerset South Deanery of the Diocese of Bath and Wells. There is a Holy Communion service on the fourth Sunday of each month at 10.30am, shared with St Nicholas, Corfe; the benefice's other services move among its churches, and <a href="https://achurchnearyou.com/church/11367">A Church Near You</a> has the current pattern. The vicar is the Revd Jim Fallon, at the Vicarage, Pitminster, telephone 01823 421757.</p>
<p>A medieval church costs money to keep standing, and the parish, not the Church of England centrally, is responsible for it. If you would like to help, the <a href="visit.html#give">Visit &amp; give</a> page explains how, and where the money goes.</p>
</div>

<aside class="aside">
<div class="box">
<h3>At a glance</h3>
<dl>
<dt>Dedication</dt><dd>St Andrew and St Mary</dd>
<dt>Listing</dt><dd>Grade I, listed 25 February 1955 (list entry 1344587)</dd>
<dt>Built</dt><dd>About 1300; enlarged in the 15th century</dd>
<dt>Restored</dt><dd>1869, Sir George Gilbert Scott; 1937, W. D. Caröe (chancel); 1979 (Lady chapel)</dd>
<dt>Materials</dt><dd>Local rubble stone with Ham stone dressings; slate roofs; lead spire</dd>
<dt>Benefice</dt><dd>The Blackdown Benefice, Somerset South Deanery, Diocese of Bath and Wells</dd>
<dt>Address</dt><dd>Church Lane, Pitminster, Taunton TA3 7AZ</dd>
<dt>Services</dt><dd>Holy Communion, fourth Sunday, 10.30am (with St Nicholas, Corfe)</dd>
<dt>Vicar</dt><dd>The Revd Jim Fallon, 01823 421757</dd>
</dl>
</div>
<div class="box">
<h3>Sources</h3>
<p class="small">Historic England list entry 1344587; A Church Near You, St Mary &amp; St Andrew, Pitminster, and its church-history page; <i>The Church of St Mary and St Andrew, Pitminster</i> (A. W. Vivian-Neal and Arthur Westall, 1950); the Pitminster and Corfe Pageant programme, 1976, in the Redress of the Past database. Full list on the <a href="about.html">About</a> page.</p>
</div>
</aside>
</div></section>
"""

VILLAGE = """
<section class="pagehead has-photo"><div class="wrap">
<div class="rule"></div>
<h1>The village</h1>
<p class="lede">Pitminster is a village and parish four miles south of Taunton, on the northern slopes of the Blackdown Hills, looking out over the Vale of Taunton Deane. The parish takes in Blagdon Hill, Angersleigh, Sellick's Green, Duddlestone, Poundisford, Feltham and Woodram, and about 950 people.</p>
<figure>
<img src="images/blagdon-hill-from-southwest.jpg" width="640" height="422" alt="Blagdon Hill seen from the edge of a wood to the south-west, fields in the foreground and the Vale of Taunton Deane beyond">
<figcaption>Blagdon Hill from the south-west, where the footpath from Howleigh enters the wood. Photograph by Nick Chipchase, CC BY-SA 2.0.</figcaption>
</figure>
</div></section>

<section class="page"><div class="wrap">
<div class="prose">
<h2>A bishop's manor</h2>
<p>The name is usually read as the minster, or mother church, of Pippa's people: a church was here before the Normans. In 938 King Athelstan gave the estate, with Corfe next door, to the Bishop of Winchester, and for the next six centuries Pitminster was part of the bishops' great manor of Taunton Deane. The bishops kept a deer park in the parish; King John came to hunt in it in 1208, and the park's name survives in Poundisford.</p>
<p>Taunton's priory held land at Barton. When the monasteries were dissolved in 1539 the priory's lands there passed to the Coles family, whose alabaster effigies now lie in the chancel of the church. Pitminster and Angersleigh were counted in the Taunton Deane Hundred; after 1894 they were in Taunton Rural District, then Taunton Deane, then Somerset West and Taunton, and since April 2023 the whole county has been run by one council, Somerset Council. The village still has its own parish council, which sets the precept, comments on planning applications and keeps an eye on conservation.</p>

<h2>Poundisford</h2>
<p>Poundisford Park is a Tudor house built around 1550 for William Hill and still standing in the old park. It stayed with the Hills, who added a dining room in 1692, and then passed to the Welmans in 1706, the Helyars in 1869 and the Vivian-Neals in 1928; A. W. Vivian-Neal went on to write the church's guidebook in 1950. Across the park is its neighbour, Poundisford Lodge.</p>
<p>Poundisford gave the English-speaking world a hymn. Jemima Thompson, who lived there, wrote <i>I think when I read that sweet story of old</i> for her Sunday school class in the village; it was sung in chapels and Sunday schools for a century and more.</p>
<figure>
<img src="images/poundisford-lodge.jpg" width="640" height="426" alt="Poundisford Lodge, a gabled stone house seen across a stream and lawn" loading="lazy">
<figcaption>Poundisford Lodge, from the stream. Photograph by Nick Chipchase, CC BY-SA 2.0.</figcaption>
</figure>

<h2>What the pageant remembered</h2>
<p>On two July evenings in 1976, eighty villagers performed the Pitminster and Corfe Pageant inside the church: fifteen episodes of the parish's history, written by the local historian Joan Peden and staged by the Revd Eric Crowe and his wife, with tickets at fifty pence. It is as good a guide as any to what the village thinks its history is:</p>
<ul>
<li>King Athelstan's charter of 938, and King John hunting at Poundisford with Bishop Peter des Roches.</li>
<li>The building of the church around 1300, the Dissolution seen through the Prior of Taunton and his monks, and the Coles family taking the priory's lands at Barton.</li>
<li>A dispute in 1630 over replacing the church bells. Richard Trott refused to pay, and a few years later took his family to New England; his story continues on the <a href="across.html">Across the water</a> page.</li>
<li>Divided loyalties in the siege of Taunton in 1645, and the Monmouth Rebellion of 1685 and what followed it.</li>
<li>The Great Storm of 1703, which damaged the spire.</li>
<li>A foundling, Thomas Basket, left at a cottage at Paradise above Lowton in 1723.</li>
<li>The Pitminster Volunteers, raised between 1798 and 1802 against the French invasion that never came.</li>
<li>Jemima Thompson's hymn, Queen Victoria's jubilee of 1887 marked with a Queen's Acre at Corfe, and the Home Guard and the war dead of 1939 to 1945.</li>
</ul>
<div class="pair pair-prog">
<figure><img src="images/pageant-programme.jpg" width="900" height="1445" alt="The programme of the Pitminster Parish History Pageant, staged in St Andrew and St Mary's church on Friday 26 and Saturday 27 June 2026" loading="lazy" style="aspect-ratio:auto;object-fit:contain"><figcaption>The programme for the 2026 pageant.</figcaption></figure>
<div><h3>Fifty years on</h3><p>The village did it again. On Friday 26 and Saturday 27 June 2026, half a century after the first, the parish staged a new Pitminster Parish History Pageant inside the church, with painted hills and trees set up in front of the pulpit and the parish's story played out in scenes from the first monks to the ration books of the 1940s. Among the audience were Treat descendants from America, in the village that week for a family reunion.</p></div>
</div>

<h2>Around the parish</h2>
<p>Blagdon Hill is the largest settlement, strung along the road that climbs south out of the vale towards Honiton; the Post Office added the Hill to its name in the nineteenth century to tell it from the other Blagdon in north Somerset. It has two pubs, the Lamb and Flag and the Blagdon Inn. Pitminster's own pub, the Queen's Arms on Church Road, stands on what is said to be one of the earliest recorded mill sites in Somerset, with a mill here in 1036 belonging to St Swithun's Priory at Winchester, a flour mill in 1804 and a public house after that. Angersleigh, to the west, has its own church, St Michael, fourteenth century and Grade II* listed. Corfe, Pitminster and Trull still share an almshouse charity.</p>
<div class="pair">
<figure><img src="images/queens-arms.jpg" width="640" height="428" alt="The Queen's Arms, a stone and rendered building beside the road at Pitminster" loading="lazy"><figcaption>The Queen's Arms, Pitminster. Photograph by Martin Bodman, CC BY-SA 2.0.</figcaption></figure>
<figure><img src="images/lamb-and-flag.jpg" width="640" height="509" alt="The Lamb and Flag public house at Blagdon Hill" loading="lazy"><figcaption>The Lamb and Flag, Blagdon Hill. Photograph by Roger Cornfoot, CC BY-SA 2.0.</figcaption></figure>
</div>
<p>Above the village the Blackdowns begin. Prior's Park and Adcombe Wood, 104 hectares of old broadleaved woodland and marshy grassland on the north-facing slope, is a Site of Special Scientific Interest, part of it looked after by the Somerset Wildlife Trust, and the footpaths through it come out on Adcombe Hill with the whole vale laid out below. Lower down, the lanes between Woodram, Duddlestone and the church are the oldest kind of English walking: high hedges, a three-way bridge over the stream, and the spire ahead.</p>
<div class="pair">
<figure><img src="images/from-adcombe-hill.jpg" width="640" height="427" alt="Looking across hedged fields from Adcombe Hill towards the Vale of Taunton Deane" loading="lazy"><figcaption>From Adcombe Hill. Photograph by Lewis Clarke, CC BY-SA 2.0.</figcaption></figure>
<figure><img src="images/approaching-pitminster.jpg" width="640" height="480" alt="A footpath across a field towards Pitminster, the church spire visible ahead" loading="lazy"><figcaption>The footpath from Woodram Lane, the spire ahead. Photograph by Derek Harper, CC BY-SA 2.0.</figcaption></figure>
</div>

<h2>Help us fill this in</h2>
<p>These pages are written from the published record and from a distance. The village knows more: the school, the village hall, the bowling club, who farmed which fields, what happened to the Pitminster Volunteers' drum. If you can add to it or correct it, <a href="wall.html">leave a note on the wall</a> or <a href="contact.html">write to the editors</a>. Villagers' photographs, old or new, are especially welcome.</p>
</div>

<aside class="aside">
<div class="box">
<h3>Pitminster parish</h3>
<dl>
<dt>Where</dt><dd>Somerset, 4 miles (6.4 km) south of Taunton, on the northern edge of the Blackdown Hills</dd>
<dt>Settlements</dt><dd>Pitminster, Blagdon Hill, Angersleigh, Sellick's Green, Duddlestone, Poundisford, Feltham, Woodram</dd>
<dt>Population</dt><dd>956 at the 2011 census</dd>
<dt>Council</dt><dd>Pitminster Parish Council; Somerset Council (unitary, since 2023); Blackdown ward</dd>
<dt>Parliament</dt><dd>Taunton and Wellington</dd>
<dt>Churches</dt><dd>St Andrew &amp; St Mary, Pitminster (Grade I); St Michael, Angersleigh (Grade II*)</dd>
<dt>Pubs</dt><dd>The Queen's Arms, Pitminster; the Lamb and Flag and the Blagdon Inn, Blagdon Hill</dd>
</dl>
</div>
<div class="box">
<h3>Sources</h3>
<p class="small">Robin Bush, <i>Somerset: The Complete Guide</i> (1994); Historic England list entries for Poundisford Park and the two churches; the Pitminster and Corfe Pageant, 1976 (Redress of the Past); Natural England's citation for Prior's Park and Adcombe Wood SSSI; the 2011 census; photographers' notes on Geograph. Full list on the <a href="about.html">About</a> page.</p>
</div>
</aside>
</div></section>
"""

ARMS_SVG = """<svg viewBox="0 0 120 140" role="img" aria-label="The Treat arms: red and gold vertical stripes with a white canton bearing a black bear rampant">
<defs><clipPath id="shield"><path d="M4 4h112v70c0 36-28 56-56 62C32 130 4 110 4 74Z"/></clipPath></defs>
<g clip-path="url(#shield)">
<rect x="0" y="0" width="120" height="140" fill="#B8862E"/>
<rect x="4" y="0" width="18.67" height="140" fill="#8F2A20"/>
<rect x="41.33" y="0" width="18.67" height="140" fill="#8F2A20"/>
<rect x="78.67" y="0" width="18.67" height="140" fill="#8F2A20"/>
<rect x="4" y="4" width="44" height="46" fill="#F3F0E8"/>
<use href="#bear" x="6" y="5" width="40" height="44" style="color:#141414"/>
</g>
<path d="M4 4h112v70c0 36-28 56-56 62C32 130 4 110 4 74Z" fill="none" stroke="#2A2A2A" stroke-width="2"/>
</svg>"""

ACROSS = """
<section class="pagehead has-photo"><div class="wrap">
<div class="rule"></div>
<h1>Across the water</h1>
<p class="lede">In the 1630s a Pitminster family named Trott sailed for New England. They became the Treats, and four centuries later their descendants are still coming back to the church where it began.</p>
<figure class="natural">
<img src="images/treat-brass.jpg" width="1400" height="791" alt="The 1902 brass to Richard Treat, alias Trott, baptised in this church in 1584, and his son Robert, Governor of Connecticut, erected by their descendant John Harvey Treat of America" fetchpriority="high">
<figcaption>The brass John Harvey Treat placed in the church in 1902, photographed in June 2026.</figcaption>
</figure>
</div></section>

<section class="band"><div class="wrap" style="padding-block:1.5rem 2rem">
<p class="small muted" style="margin-bottom:.25rem">Above the line, Somerset; below it, New England and beyond. Scroll sideways.</p>
<div class="tl"><div class="tl-track">
<div class="tl-item"><div class="above"><span class="where">Pitminster</span>King Athelstan gives the estate, with Corfe, to the Bishop of Winchester.</div><div class="pip"><span>938</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">Pitminster</span>The present church is built on the site of its Saxon predecessor.</div><div class="pip"><span>c.1300</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">St Andrew &amp; St Mary</span>Richard Trott, son of Robert and Honoria, is baptised on 28 August.</div><div class="pip"><span>1584</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">St Andrew &amp; St Mary</span>Richard Trott marries Alice Gaylord, baptised here in 1594, on 27 April.</div><div class="pip"><span>1615</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">Pitminster</span>The parish argues over new bells. Richard Trott refuses to pay.</div><div class="pip"><span>1630</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1637</span></div><div class="below"><span class="where">Wethersfield, Connecticut</span>The Trotts sail for New England and settle on the Connecticut River. The name becomes Treat.</div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1662</span></div><div class="below"><span class="where">Connecticut</span>Richard Treat is named a patentee in the Royal Charter granted by Charles II.</div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1666</span></div><div class="below"><span class="where">New Jersey</span>Robert Treat leads the Milford settlers who found Newark on the Passaic.</div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1687</span></div><div class="below"><span class="where">Hartford</span>Governor Treat receives Sir Edmund Andros; the candles go out and the charter vanishes into the Charter Oak.</div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1759</span></div><div class="below"><span class="where">Penobscot, Maine</span>Lieutenant Joshua Treat is armourer at Fort Pownall and settles up the river.</div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1776</span></div><div class="below"><span class="where">Philadelphia</span>Robert Treat Paine, a Treat on his mother's side, signs the Declaration of Independence.</div></div>
<div class="tl-item"><div class="above"></div><div class="pip"><span>1893</span></div><div class="below"><span class="where">Lawrence, Massachusetts</span>John Harvey Treat publishes <i>The Treat Family</i>, the genealogy the family still keeps.</div></div>
<div class="tl-item"><div class="above"><span class="where">St Andrew &amp; St Mary</span>John Harvey Treat places a brass tablet to Richard and Robert in the church.</div><div class="pip"><span>1902</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">St Andrew &amp; St Mary</span>The village pageant tells the bell dispute as its sixth episode.</div><div class="pip"><span>1976</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">St Andrew &amp; St Mary</span>The new east window, paid for in part by American descendants, is installed.</div><div class="pip"><span>1989</span></div><div class="below"></div></div>
<div class="tl-item"><div class="above"><span class="where">St Andrew &amp; St Mary</span>Treat descendants come back to the church for a family reunion.</div><div class="pip"><span>2026</span></div><div class="below"></div></div>
</div></div>
</div></section>

<section class="page"><div class="wrap">
<div class="prose">
<h2>The Trotts of Pitminster</h2>
<p>Richard Trott was baptised in the church of St Andrew and St Mary on 28 August 1584, the son of Robert and Honoria Trott. On 27 April 1615 he married Alice Gaylord in the same church; she had been baptised there on 10 May 1594. The village's own history remembers him once more before he leaves: in 1630 the parish fell out over the cost of new bells, and Richard Trott refused to pay his share. The 1976 pageant made it the sixth of its fifteen episodes.</p>
<p>By 1637 Richard, Alice and their children had sailed for New England and settled at Wethersfield on the Connecticut River, one of the colony's three founding towns. Somewhere on the crossing the name changed its spelling, as names did, and the Trotts of Pitminster became the Treats of Connecticut. Richard prospered. He served the town and the colony, and when Charles II granted Connecticut its Royal Charter in 1662 he was one of the men named in it as patentees. He died in 1669.</p>
<p>The Gaylord name is a Pitminster name too, and Gaylords from Somerset were among the first settlers of Windsor, Connecticut, a few miles upriver from Wethersfield. Whether Alice was kin to them is a question the parish registers have not yet answered.</p>

<h2>Governor Robert Treat</h2>
<p>Robert Treat was baptised at Pitminster in 1624 and was a boy when the family sailed. His family were among the founders of Milford, Connecticut, in 1639, and in 1666 he led the Milford settlers who founded Newark on the Passaic in New Jersey; early accounts call him, more than anyone, the founder of that city. He came back to Connecticut, commanded its forces in King Philip's War, and was governor of the colony from 1683 to 1698.</p>
<p>His famous hour came on 31 October 1687, when Sir Edmund Andros, the Crown's governor of the new Dominion of New England, rode into Hartford with troops to take the colony's charter. Treat received him formally, spoke long and movingly of what the charter meant to the colony, and as the story has been told ever since the candles went out, and when they were lit again the charter was gone from the table. It was hidden in the hollow of a great oak, the Charter Oak, and brought out again when Andros fell. Treat died in 1710 and lies at Milford.</p>

<h2>The family that came after</h2>
<p>Richard and Alice have a very large number of descendants, and the family's own genealogy, <i>The Treat Family: A Genealogy of Trott, Tratt, and Treat</i>, published by John Harvey Treat in 1893, runs to several hundred pages. A few of the names:</p>
<ul>
<li>The Revd Samuel Treat (1648–1717), Robert's son, minister at Eastham on Cape Cod for forty-five years and a missionary to the Nauset people.</li>
<li>Robert Treat Paine (1731–1814), grandson of Samuel's daughter Eunice, prosecutor at the Boston Massacre trials and a signer of the Declaration of Independence for Massachusetts.</li>
<li>Lieutenant Joshua Treat, armourer at Fort Pownall on the Penobscot in 1759 and by tradition the first settler up that river, whose descendants became the Treats of Frankfort and Winterport in Maine.</li>
<li>Upham S. Treat of Eastport, Maine, who was among the first to put lobster in a can, and whose name is on Treat Island at the mouth of the Bay of Fundy.</li>
<li>Mary Treat (1830–1923) of Vineland, New Jersey, naturalist and author, who corresponded with Charles Darwin about insect-eating plants.</li>
<li>Charles H. Treat (1842–1910), Treasurer of the United States under Theodore Roosevelt.</li>
<li>Judge William W. Treat of New Hampshire, born at Winterport, Maine: judge, state party chairman and presidential elector, saluted by Senator Bob Dole in a speech now kept in the Dole archive.</li>
</ul>

<h2>The arms</h2>
<div class="arms">
""" + ARMS_SVG + """
<p>The arms recorded in the family genealogy and painted on the panel the family still keeps: paly of six, gules and or, that is, red and gold vertical stripes, with on a silver canton a black bear rampant. The crest above the helm is a unicorn's head. In English heraldry arms belong to a man and his descendants, not to a surname, which is one reason the family has kept its line so carefully.</p>
</div>

<h2>The line of descent</h2>
<p>Fourteen generations separate Richard Trott of Pitminster from the family's youngest members. The documented male line, kept on the family tree and checked against the 1893 genealogy, runs through these men; the living generations are left off a public page.</p>
<ol class="line">
<li><b>Richard Trott</b> of Pitminster, who never left Somerset, father of the emigrant.</li>
<li><b>Richard Treat</b> (1584–1669), baptised and married at Pitminster, settler of Wethersfield, patentee of the 1662 Charter.</li>
<li><b>Robert Treat</b> (1624–1710), founder of Newark, Governor of Connecticut.</li>
<li><b>The Revd Samuel Treat</b> (1648–1717), minister at Eastham on Cape Cod.</li>
<li><b>Joseph Treat</b>, gunsmith of Boston.</li>
<li><b>Lieutenant Joshua Treat</b>, armourer at Fort Pownall, settler on the Penobscot.</li>
<li><b>Robert Treat</b> (1777–1845), of the Penobscot towns, who married Mary Ridley.</li>
<li><b>Colonel William Treat</b> (1813–1879) of Winterport, Maine.</li>
<li><b>Joshua Treat</b> (1841–1926), who married Annie Wardwell.</li>
<li><b>Joshua A. Treat II</b> (born 1881).</li>
<li><b>Judge William W. Treat</b>, born at Winterport, Maine.</li>
<li>Three living generations, in Massachusetts and Maine, the youngest of whom stood in the church at Pitminster in 2026.</li>
</ol>

<h2>Coming back</h2>
<p>The family has been returning for a long time. John Harvey Treat came in 1902 and left the brass. When the east window needed replacing in the 1980s, American descendants of Pitminster families helped pay for it. In 2026 a party of Treats came to the church for a reunion, stood in front of the tablet, and walked the lanes their ancestor walked before the bells. If you are a Treat, a Gaylord, or descend from any family that left this parish, the <a href="wall.html">family wall</a> is yours; and if you have a record, a photograph or a story that belongs on this page, the editors would like to hear from you.</p>
<p>The family also tells its story as a game. <a href="games.html">Treatopoly</a> runs the whole line around a board, from Set Sail 1637 to Return to Pitminster.</p>
</div>

<aside class="aside">
<div class="box">
<h3>Richard Treat</h3>
<dl>
<dt>Baptised</dt><dd>28 August 1584, St Andrew &amp; St Mary, Pitminster</dd>
<dt>Married</dt><dd>27 April 1615, Alice Gaylord (baptised Pitminster, 10 May 1594)</dd>
<dt>Sailed</dt><dd>By 1637, to Wethersfield, Connecticut</dd>
<dt>Named in</dt><dd>The Royal Charter of Connecticut, 1662</dd>
<dt>Died</dt><dd>1669, Wethersfield</dd>
<dt>Remembered</dt><dd>Brass tablet in the church, placed 1902</dd>
</dl>
</div>
<div class="box">
<h3>Sources</h3>
<p class="small">John Harvey Treat, <i>The Treat Family: A Genealogy of Trott, Tratt, and Treat</i> (1893); the Pitminster parish registers as summarised in the genealogy; the Pitminster and Corfe Pageant, 1976; A Church Near You, church history page; the Royal Charter of Connecticut (1662), Connecticut State Library; the Dole Archives, University of Kansas. Full list on the <a href="about.html">About</a> page.</p>
</div>
</aside>
</div></section>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>""" + "BEAR_SYMBOL" + """</defs></svg>
"""

GAMES = """
<section class="pagehead"><div class="wrap">
<div class="rule"></div>
<h1>Games</h1>
<p class="lede">The family's history, playable. Both games run in the browser on a phone or a laptop, cost nothing, and were made by and for the family. Every square and every stop carries a line of the real history; where a story is a tradition rather than a document, the game says so.</p>
</div></section>

<section class="page"><div class="wrap" style="display:block">
<div class="games">
<article class="game">
<h2>Treatopoly</h2>
<p class="status">Playable now, on a phone or a laptop. Two to six players.</p>
<p>The family's board game. Forty spaces run in order from Set Sail 1637 to Return to Pitminster: the Atlantic crossing, the Passaic voyage, the Pownall expedition and the Penobscot survey are the four journeys, Treat Mills and the lobster cannery are the utilities, the Stocks stand in for jail and Andros Arrives sends you there, and free parking is a lobster bake. The Charter Oak and the Family Bible are the two decks. Play online with family in other houses, or against bots named for the ancestors.</p>
<p class="small muted">Tap the dice to roll. No trading and no auctions; the host can call the game at any point and the biggest net worth wins.</p>
<p><a class="btn" href="games/treatopoly.html">Play Treatopoly</a></p>
</article>
<article class="game">
<h2>The Treat Trail</h2>
<p class="status">Playable now, on a phone or a laptop.</p>
<p>The first of the family's games, in the style of the Oregon Trail. Three hundred and eighty-nine years from Pitminster: the Atlantic crossing, Wethersfield, Newark, the Penobscot, and on. Buy provisions, mind the rations and the weather, and get the family through. Every stop carries a line of the real history, and the road ends where it began.</p>
<p><a class="btn" href="games/treat-trail.html">Play The Treat Trail</a></p>
</article>
</div>
<p class="small muted" style="margin-top:2rem;max-width:66ch">These are fan-made family histories. The landscapes, buildings and people are stylised. If a date or a name in them is wrong, <a href="contact.html">tell the editors</a> and it will be fixed in the next version. The family keeps its own page, with the games, the notable Treats and the line of descent, at <a href="https://treatfamily.org">treatfamily.org</a>.</p>
</div></section>
"""

WALL = """
<section class="pagehead"><div class="wrap">
<div class="rule"></div>
<h1>The family wall</h1>
<p class="lede">A place to leave a note: who you are, which family you belong to if any, where you have ended up, and what you are looking for. Descendants, villagers and visitors are all welcome. A person reads every note before it appears, so there may be a day or two's delay.</p>
</div></section>

<section class="page"><div class="wrap">
<div>
<form id="wall-form" novalidate>
<div class="rule"></div>
<h2>Leave a note</h2>
<div class="field"><label for="w-name">Your name</label><input type="text" id="w-name" name="name" maxlength="80" required autocomplete="name"></div>
<div class="field"><label for="w-place">Where you are writing from</label><input type="text" id="w-place" name="place" maxlength="80" placeholder="Taunton; Winterport, Maine; Melbourne" autocomplete="off"></div>
<div class="field"><label for="w-conn">Your connection, if any</label><input type="text" id="w-conn" name="connection" maxlength="120" placeholder="Treat descendant; grew up at Blagdon Hill; just visiting"><span class="hint">Optional.</span></div>
<div class="field"><label for="w-msg">Your note</label><textarea id="w-msg" name="message" maxlength="1200" required></textarea><span class="hint">Up to 1,200 characters. No street addresses or phone numbers, please; the wall is public.</span></div>
<div class="field"><label for="w-email">Your email</label><input type="email" id="w-email" name="email" maxlength="120" autocomplete="email"><span class="hint">Optional and never shown. The editors use it only to reply if someone is looking for you.</span></div>
<div class="hp" aria-hidden="true"><label for="w-web">Leave this empty</label><input type="text" id="w-web" name="website" tabindex="-1" autocomplete="off"></div>
<div id="w-turnstile" class="field"></div>
<p style="margin-top:1.25rem"><button class="btn" type="submit" id="w-submit">Post the note</button></p>
<div id="w-notice" class="notice" hidden></div>
</form>
</div>
<aside class="aside">
<div class="box">
<h3>House rules</h3>
<ul>
<li>Notes are read by a person before they appear.</li>
<li>No street addresses, phone numbers or anything you would not say in the churchyard.</li>
<li>Nothing for sale.</li>
<li>If you want a note taken down, <a href="contact.html">ask</a> and it will be.</li>
</ul>
</div>
</aside>
</div></section>

<section class="band"><div class="wrap" style="padding-block:2rem 3rem">
<div class="rule"></div>
<h2>Notes</h2>
<div class="wall" id="wall">""" + EXAMPLE_POSTS + """</div>
<p id="wall-empty" class="muted" hidden style="margin-top:1rem">No notes yet. Leave the first one.</p>
</div></section>
"""

VISIT = """
<section class="pagehead has-photo"><div class="wrap">
<div class="rule"></div>
<h1>Visit, worship &amp; give</h1>
<p class="lede">The church is open for worship once a month and welcomes visitors at other times; the village is a good day out from Taunton in any season. The parish, not this site, receives every gift to the church.</p>
<figure>
<img src="images/approaching-pitminster.jpg" width="640" height="480" alt="A footpath across a field towards Pitminster, the church spire visible ahead" fetchpriority="high">
<figcaption>The footpath from Woodram Lane, the spire ahead. Photograph by Derek Harper, CC BY-SA 2.0.</figcaption>
</figure>
</div></section>

<section class="page"><div class="wrap">
<div class="prose">
<h2>Finding the church</h2>
<p>St Andrew and St Mary stands on Church Lane in Pitminster, postcode TA3 7AZ, about four miles south of Taunton off the road to Blagdon Hill and Honiton. The spire shows the way from the lanes to the south. Taunton has the nearest railway station. <a href="https://www.openstreetmap.org/?mlat=50.9661&amp;mlon=-3.1111#map=16/50.9661/-3.1111">Open the map</a>.</p>
<p>If you are coming to see the Treat brass, the Coles tombs or the east window, it is worth writing to the vicarage first to check the church will be open, and the editors are always glad to hear from a visitor before and after.</p>

<h2>Services</h2>
<p>Holy Communion is celebrated on the fourth Sunday of each month at 10.30am, a service shared with St Nicholas, Corfe. For the rest of the month the six churches of the Blackdown Benefice take turns; <a href="https://achurchnearyou.com/church/11367">A Church Near You</a> keeps the current list, and the benefice's own site is <a href="https://blackdown.org.uk">blackdown.org.uk</a>. The vicar is the Revd Jim Fallon, the Vicarage, Pitminster, Taunton TA3 7AZ, telephone 01823 421757.</p>

<h2 id="give">Giving to the church</h2>
<p>A medieval church is kept standing by its parish. The Parochial Church Council is responsible for the building, its roof, its lead and its glass, and for the day-to-day cost of keeping it open; the Church of England does not pay for it centrally. The parish is an excepted charity, and gifts to it are charitable gifts.</p>
<p>Gifts go to the parish directly. This site does not handle money, and never will.</p>
<div class="notice" id="give-link">
<p><b>The parish's online giving page</b> will be linked here once the Parochial Church Council has confirmed which one it uses. Until then, the surest way to give is to contact the vicarage, telephone 01823 421757, which can also take a cheque made out to the parish.</p>
</div>
<ul>
<li><b>UK taxpayers</b> can add Gift Aid, which lets the parish reclaim the basic-rate tax on a gift; the parish will have the form.</li>
<li><b>Giving regularly</b> is what helps a small parish most. Many Bath and Wells parishes use the Parish Giving Scheme, which takes a monthly gift by direct debit or card.</li>
<li><b>From the United States and elsewhere</b>, a gift to an English parish is welcome but is not deductible on a US return; give because the church matters to you, not for the deduction.</li>
<li><b>In your will</b>, a legacy to the parish church is the gift that repairs roofs. The vicarage can tell you how the parish should be named.</li>
</ul>

<h2>Other ways to help</h2>
<p>Come to a service when you visit. Buy the church guide if one is on the table. Write a note on the <a href="wall.html">family wall</a> so the village knows who is coming and why. And if you have skills the church or this site could use, whether building, history, photography or fundraising, <a href="contact.html">say so</a>.</p>
</div>

<aside class="aside">
<div class="box">
<h3>The church</h3>
<dl>
<dt>Address</dt><dd>Church Lane, Pitminster, Taunton, Somerset TA3 7AZ</dd>
<dt>Services</dt><dd>Holy Communion, fourth Sunday of the month, 10.30am, with St Nicholas, Corfe</dd>
<dt>Vicar</dt><dd>The Revd Jim Fallon, the Vicarage, Pitminster; 01823 421757</dd>
<dt>Benefice</dt><dd>The Blackdown Benefice, Diocese of Bath and Wells</dd>
</dl>
</div>
<div class="box">
<h3>In the village</h3>
<dl>
<dt>Eat and drink</dt><dd>The Queen's Arms, Pitminster; the Lamb and Flag and the Blagdon Inn, Blagdon Hill</dd>
<dt>Walk</dt><dd>Prior's Park and Adcombe Wood; the lanes to Woodram and Duddlestone</dd>
<dt>Nearby</dt><dd>Taunton (4 miles); the Blackdown Hills; the Wellington Monument</dd>
</dl>
</div>
</aside>
</div></section>
"""

CONTACT = """
<section class="pagehead"><div class="wrap">
<div class="rule"></div>
<h1>Contact the editors</h1>
<p class="lede">Corrections, additions, photographs, questions about a family, or a note you would rather not post on the wall. Messages go to the people who keep this site, not to the parish; for parish business, ring the vicarage on 01823 421757.</p>
</div></section>

<section class="page"><div class="wrap">
<div>
<form id="contact-form" novalidate>
<div class="field"><label for="c-name">Your name</label><input type="text" id="c-name" name="name" maxlength="80" required autocomplete="name"></div>
<div class="field"><label for="c-email">Your email</label><input type="email" id="c-email" name="email" maxlength="120" required autocomplete="email"><span class="hint">So the editors can reply. Never shown or shared.</span></div>
<div class="field"><label for="c-msg">Your message</label><textarea id="c-msg" name="message" maxlength="3000" required></textarea></div>
<div class="hp" aria-hidden="true"><label for="c-web">Leave this empty</label><input type="text" id="c-web" name="website" tabindex="-1" autocomplete="off"></div>
<div id="c-turnstile" class="field"></div>
<p style="margin-top:1.25rem"><button class="btn" type="submit" id="c-submit">Send the message</button></p>
<div id="c-notice" class="notice" hidden></div>
</form>
</div>
<aside class="aside">
<div class="box">
<h3>What helps most</h3>
<ul>
<li>A photograph of the font or the east window: the site has none yet.</li>
<li>Old photographs of the village, with roughly when and where.</li>
<li>Parish-register entries or family papers that mention Pitminster families overseas.</li>
<li>Anything on these pages that is wrong.</li>
</ul>
</div>
</aside>
</div></section>
"""

ABOUT = """
<section class="pagehead"><div class="wrap">
<div class="rule"></div>
<h1>About this site</h1>
<p class="lede">Friends of Pitminster is an independent community site about the church of St Andrew and St Mary, the village of Pitminster, and the families who left it for America. It is kept by descendants of one of those families, with roots in Maine, together with friends of the village.</p>
</div></section>

<section class="page"><div class="wrap">
<div class="prose">
<h2>What it is and is not</h2>
<p>It is not the parish's official site and does not speak for the Parochial Church Council, the Blackdown Benefice or the Diocese of Bath and Wells. For services, parish business and giving, use the parish's own channels: <a href="https://achurchnearyou.com/church/11367">A Church Near You</a> and <a href="https://blackdown.org.uk">blackdown.org.uk</a>. This site handles no money.</p>
<p>It tries to give the church, the village and the emigrant families equal weight, and to be useful to someone standing in the churchyard, someone who has lived here all their life, and someone in Connecticut who has just found the name Pitminster in a family Bible.</p>

<h2>Corrections</h2>
<p>Everything on these pages is written from the published record, listed below, and from a distance. Where the record is a tradition rather than a document, the text says so. If you know better, <a href="contact.html">write to the editors</a>; corrections are made and credited.</p>

<h2>Sources</h2>
<ul>
<li>Historic England, National Heritage List for England: Church of St Andrew and St Mary, Pitminster, list entry 1344587 (Grade I); Poundisford Park, 1060307; Church of St Michael, Angersleigh, 1177574; North family monument in the churchyard, 1060302.</li>
<li>A Church Near You (Church of England): St Mary &amp; St Andrew, Pitminster, church 11367, and its church-history page.</li>
<li>A. W. Vivian-Neal and Arthur Westall, <i>The Church of St Mary and St Andrew, Pitminster</i> (Somerset County Herald, 1950).</li>
<li>Robin Bush, <i>Somerset: The Complete Guide</i> (Dovecote Press, 1994), pp. 168–169.</li>
<li>The Pitminster and Corfe Pageant, 1976: programme and script summary in <i>The Redress of the Past: Historical Pageants in Britain</i>, pageant 1164.</li>
<li>Natural England, citation for Prior's Park and Adcombe Wood SSSI.</li>
<li>Office for National Statistics, 2011 census, Pitminster parish and Blackdown ward.</li>
<li>John Harvey Treat, <i>The Treat Family: A Genealogy of Trott, Tratt, and Treat for Fifteen Generations, and Four Hundred and Fifty Years in England and America</i> (Salem, 1893).</li>
<li>The Royal Charter of Connecticut, 1662, Connecticut State Library.</li>
<li>Robert Bartlett Dole papers, Dole Archive and Special Collections, University of Kansas (speech honouring William W. Treat).</li>
<li>Wikipedia articles on the church, the village, Richard Treat and Robert Treat, used as finding aids and checked against the sources above.</li>
<li>Photographers' notes on Geograph Britain and Ireland for the mill at the Queen's Arms and the footpaths.</li>
</ul>

<h2>Photographs and artwork</h2>
<p>The church at dusk, the nave roof, the Treat brass and the 2026 pageant programme were photographed by the site's editors in June 2026 and may be reused freely with a credit to Friends of Pitminster. The other photographs are from Geograph Britain and Ireland and are used under the Creative Commons Attribution-ShareAlike 2.0 licence. Each is credited where it appears:</p>
<ul>
<li>Church of St Andrew &amp; St Mary, Pitminster, and the monument to John Coles: Mike Searle (<a href="https://www.geograph.org.uk/photo/3157616">3157616</a>, <a href="https://www.geograph.org.uk/photo/3157709">3157709</a>).</li>
<li>Pitminster church; Approaching Pitminster; Countryside near Sellick's Green: Derek Harper (<a href="https://www.geograph.org.uk/photo/126380">126380</a>, <a href="https://www.geograph.org.uk/photo/1610088">1610088</a>, <a href="https://www.geograph.org.uk/photo/1382182">1382182</a>).</li>
<li>Blagdon Hill from the south-west; View east from the Angersleigh road; Poundisford Lodge: Nick Chipchase (<a href="https://www.geograph.org.uk/photo/1238519">1238519</a>, <a href="https://www.geograph.org.uk/photo/3496668">3496668</a>, <a href="https://www.geograph.org.uk/photo/1207938">1207938</a>).</li>
<li>The Queen's Arms; the Blagdon Inn: Martin Bodman (<a href="https://www.geograph.org.uk/photo/46480">46480</a>, <a href="https://www.geograph.org.uk/photo/195110">195110</a>).</li>
<li>The Lamb and Flag, Blagdon Hill: Roger Cornfoot (<a href="https://www.geograph.org.uk/photo/4778483">4778483</a>).</li>
<li>From Adcombe Hill: Lewis Clarke (<a href="https://www.geograph.org.uk/photo/7631088">7631088</a>).</li>
</ul>
<p>The bear rampant in the Treat arms is adapted from an illustration by Rinaldum on Wikimedia Commons, licensed CC BY-SA 3.0, recoloured. The typefaces are Libre Caslon Text and Libre Caslon Display, under the SIL Open Font License; Caslon was the type of eighteenth-century England and of the printed Declaration of Independence, which seemed right for a page about both.</p>

<h2>Privacy</h2>
<p>The site sets no advertising or tracking cookies. When you post a note on the wall or send a message, the site stores what you typed, the time, and a scrambled version of your network address used only to stop floods of spam. Email addresses are never shown and never passed to anyone else. To have a note or message removed, <a href="contact.html">ask</a>, and it will be deleted.</p>
</div>
<aside class="aside">
<div class="box">
<h3>Add to it</h3>
<p>Villagers' photographs, old or new, memories of the church and the pubs and the school, and any record of a Pitminster family overseas are all welcome. <a href="contact.html">Write to the editors</a>.</p>
</div>
</aside>
</div></section>
"""

ADMIN = """
<section class="pagehead"><div class="wrap">
<div class="rule"></div>
<h1>Editors' desk</h1>
<p class="lede">Read and approve notes for the family wall, and read messages sent through the contact form. This page is for the site's editors; it does nothing without the editors' key.</p>
</div></section>
<section class="page"><div class="wrap" style="display:block">
<form id="admin-login" novalidate style="max-width:28rem">
<div class="field"><label for="a-key">Editors' key</label><input type="password" id="a-key" name="key" autocomplete="current-password"></div>
<p style="margin-top:1rem"><button class="btn" type="submit">Open the desk</button></p>
<div id="a-notice" class="notice" hidden></div>
</form>
<div id="admin-desk" hidden>
<div class="tabs" role="tablist">
<button role="tab" aria-selected="true" data-tab="pending">Waiting</button>
<button role="tab" aria-selected="false" data-tab="approved">On the wall</button>
<button role="tab" aria-selected="false" data-tab="messages">Messages</button>
</div>
<div id="admin-list"></div>
<p style="margin-top:1.5rem"><button class="btn btn-quiet" type="button" id="a-logout">Close the desk</button></p>
</div>
</div></section>
"""

NOTFOUND = """
<section class="pagehead"><div class="wrap">
<div class="rule"></div>
<h1>There is no page here</h1>
<p class="lede">The address may have changed when the site was rebuilt. Try the <a href="index.html">front page</a>, the <a href="church.html">church</a>, the <a href="village.html">village</a> or <a href="across.html">Across the water</a>.</p>
</div></section>
"""


def build():
    bear = (PUBLIC / "assets" / "bear.svg").read_text(encoding="utf-8")
    # turn the standalone bear into a <symbol> the arms can reference
    inner = bear.split(">", 1)[1].rsplit("</svg>", 1)[0]
    symbol = '<symbol id="bear" viewBox="-40 -40 763 1035">' + inner + "</symbol>"
    across = ACROSS.replace("BEAR_SYMBOL", symbol)

    page("index.html", "Friends of Pitminster",
         "The church of St Andrew and St Mary, the village of Pitminster in the Blackdown Hills, and the families who sailed from it to New England.", INDEX)
    page("church.html", "The church of St Andrew & St Mary, Pitminster",
         "The Grade I church of St Andrew and St Mary at Pitminster, Somerset: its leaning lead spire, font, pulpit, Coles tombs, the Treat brass and the 1989 east window.", CHURCH)
    page("village.html", "Pitminster, the village",
         "Pitminster, Blagdon Hill and Angersleigh in the Blackdown Hills: a bishop's manor, Poundisford Park, the 1976 pageant, the pubs and the walks.", VILLAGE)
    page("across.html", "Across the water: Pitminster's American families",
         "Richard Trott was baptised at Pitminster in 1584 and sailed for New England in 1637. His family became the Treats of Connecticut, Massachusetts and Maine.", across)
    page("games.html", "Games: the Treat family history, playable",
         "Treatopoly, the family's board game, and The Treat Trail, 389 years from Pitminster in the style of the Oregon Trail, both playable in the browser.", GAMES)
    page("wall.html", "The family wall",
         "Leave a note for the village and the Pitminster diaspora. Every note is read by a person before it appears.", WALL)
    page("visit.html", "Visit, worship and give",
         "How to find the church of St Andrew and St Mary at Pitminster, when services are held, and how gifts reach the parish.", VISIT)
    page("contact.html", "Contact the editors",
         "Write to the people who keep Friends of Pitminster with corrections, photographs and family questions.", CONTACT)
    page("about.html", "About Friends of Pitminster",
         "What this site is, who keeps it, its sources, photograph credits and privacy note.", ABOUT)
    page("admin.html", "Editors' desk", "Moderation for the family wall.", ADMIN,
         extra_head='<meta name="robots" content="noindex,nofollow">')
    page("404.html", "Page not found", "There is no page at this address.", NOTFOUND)


if __name__ == "__main__":
    build()
