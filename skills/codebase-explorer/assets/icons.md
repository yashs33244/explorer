# Icon snippets (copy, then translate with transform="translate(x,y)"). All are about 40x40 and use only the diagram class kit.

person (client / user)
<g class="icon"><circle class="d-line" cx="20" cy="12" r="7"/><path class="d-line" d="M6,36 C6,25 34,25 34,36 Z"/></g>

monitor / app
<g><rect class="d-fillpaper" x="3" y="5" width="34" height="23" rx="3"/><path class="d-line" d="M14,35 H26 M20,28 V35"/><path class="d-lineacc" d="M9,14 H21 M9,20 H28"/></g>

database cylinder
<g><path class="d-fillpaper" d="M5,9 V31 C5,36 35,36 35,31 V9"/><ellipse class="d-fillpaper" cx="20" cy="9" rx="15" ry="5"/><path class="d-lineacc" d="M5,20 C5,25 35,25 35,20"/></g>

server rack
<g><rect class="d-fillpaper" x="4" y="4" width="32" height="10" rx="3"/><rect class="d-fillpaper" x="4" y="16" width="32" height="10" rx="3"/><rect class="d-fillpaper" x="4" y="28" width="32" height="9" rx="3"/><circle class="d-fillacc" cx="10" cy="9" r="1.8"/><circle class="d-fillacc" cx="10" cy="21" r="1.8"/><circle class="d-fillacc" cx="10" cy="32.5" r="1.8"/></g>

disk / file
<g><path class="d-fillpaper" d="M8,3 H25 L33,11 V37 H8 Z"/><path class="d-line" d="M25,3 V11 H33"/><path class="d-lineacc" d="M13,20 H28 M13,26 H28 M13,32 H22"/></g>

page of 8kB (grid)
<g><rect class="d-fillpaper" x="5" y="4" width="30" height="32" rx="3"/><path class="d-lineacc" d="M5,12 H35"/><rect class="d-fillacc" x="10" y="17" width="20" height="4" rx="1"/><rect class="d-fillacc" x="10" y="24" width="14" height="4" rx="1"/></g>

lock
<g><rect class="d-fillpaper" x="7" y="17" width="26" height="19" rx="4"/><path class="d-line" d="M12,17 V12 C12,3 28,3 28,12 V17"/><circle class="d-fillacc" cx="20" cy="26" r="2.6"/></g>

gear (process / worker)
<g><circle class="d-fillpaper" cx="20" cy="20" r="9"/><circle class="d-lineacc" cx="20" cy="20" r="3.5"/><path class="d-line" d="M20,3 V8 M20,32 V37 M3,20 H8 M32,20 H37 M8,8 L11.5,11.5 M28.5,28.5 L32,32 M8,32 L11.5,28.5 M28.5,11.5 L32,8"/></g>

clock
<g><circle class="d-fillpaper" cx="20" cy="20" r="15"/><path class="d-lineacc" d="M20,10 V20 L27,24"/></g>

log / journal (WAL)
<g><rect class="d-fillpaper" x="6" y="4" width="28" height="32" rx="3"/><path class="d-line" d="M12,4 V36"/><path class="d-lineacc" d="M17,12 H29 M17,19 H29 M17,26 H25"/></g>

cloud / network
<g><path class="d-fillpaper" d="M10,30 C3,30 3,19 11,19 C12,10 27,9 29,18 C37,17 38,30 30,30 Z"/></g>

arrow with arrowhead: define your own marker per svg, ids MUST be prefixed with the diagram key, for example
<defs><marker id="KEY-d1-ah" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" class="d-fillink"/></marker></defs>
<path class="d-edge" d="M100,100 C160,100 160,160 220,160" marker-end="url(#KEY-d1-ah)"/>

numbered step badge
<g><circle class="d-badge" cx="X" cy="Y" r="11"/><text class="d-bt" x="X" y="Y+4">1</text></g>
