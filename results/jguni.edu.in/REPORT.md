# Hunt Report — https://jguni.edu.in

Generated: 2026-11-21T19:47:20Z &nbsp;|&nbsp; Duration: 65m 25s

> **Nothing is filtered during collection. This report is only a grouping.**

## Summary

| What | Count | Meaning |
|---|---:|---|
| Routes collected | 595 | Every URL found, nothing removed |
| Distinct routes verified | 113 | One row per URL (method probes excluded) |
| HTTP responses | 521 | Includes method probes — kept in `method_responses.jsonl` |
| **Accessible (200)** | **68** | Confirmed live — the wins |
| Exists but different status | 14 | 301/302/401/403/405 — real route, blocked |
| Other responses | 31 | 404/500/etc — kept, not discarded |
| Subdomains (resolved) | 2 | DNS-verified |
| Virtual hosts (real) | 2 | Cloudflare 403/530/0 excluded |
| Parameters | 164 | URLs with query params |
| JS endpoints (AST) | 0 | anastasis evidence-backed |
| First-party URLs | 402 | jguni.edu.in and subdomains |
| Third-party URLs | 193 | kept in `third_party_routes.jsonl` |
| Method responses | 476 | kept in `method_responses.jsonl` |
| Blocked vhost checks | 0 | kept in `vhost_blocked.jsonl` |
| Secret candidates | 0 | verify manually |

> Collection keeps third-party URLs by design (193). See `third_party_routes.jsonl`. Method-probe responses are in `method_responses.jsonl`.

## 1. SUCCESS — HTTP 200

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://ajax.aspnetcdn.com/ajax/jquery.validate/1.11.1/jquery.validate.js` | application/javascript | 38951 |  |
| 200 | GET | `https://ajax.aspnetcdn.com/ajax/jquery.validate/1.11.1/jquery.validate.min.js` | application/javascript | 21068 |  |
| 200 | GET | `https://autoconfig.jguni.edu.in` | application/xml | 852 |  |
| 200 | GET | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.js` | application/javascript | 207819 |  |
| 200 | GET | `https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js` | application/javascript | 80721 |  |
| 200 | GET | `https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.js` | application/javascript | 156955 |  |
| 200 | GET | `https://cdn.jsdelivr.net/npm/select2@4.1.0-rc.0/dist/js/select2.min.js` | application/javascript | 73163 |  |
| 200 | GET | `https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.js` | application/javascript | 349021 |  |
| 200 | GET | `https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js` | application/javascript | 154597 |  |
| 200 | GET | `https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js` | application/javascript | 5537 |  |
| 200 | GET | `https://code.jquery.com/jquery-3.6.0.js` | application/javascript | 288580 |  |
| 200 | GET | `https://code.jquery.com/jquery-3.6.0.min.js` | application/javascript | 89501 |  |
| 200 | GET | `https://eequeuestorage.blob.core.windows.net/staticfiles/jguni/ee-form-widget/form-1/widget.js` | application/javascript | 864 |  |
| 200 | GET | `https://eequeuestorage.blob.core.windows.net/staticfiles/jguni/ee-form-widget/form-2/widget.js` | application/javascript | 849 |  |
| 200 | GET | `https://eewidget.extraaedge.com` | text/html | 1370 |  |
| 200 | GET | `https://jguni.edu.in` | text/html | 490274 |  |
| 200 | GET | `https://jguni.edu.in/aboutus-page` | text/html | 319953 |  |
| 200 | GET | `https://jguni.edu.in/blog` | text/html | 295632 |  |
| 200 | GET | `https://jguni.edu.in/captcha.php` | image/png | 505 |  |
| 200 | GET | `https://jguni.edu.in/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-decode.min.js` | application/javascript | 1239 |  |
| 200 | GET | `https://jguni.edu.in/cdn-cgi/speculation` | application/speculationrules+json | 151 |  |
| 200 | GET | `https://jguni.edu.in/contact-us` | text/html | 295682 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/error/js/bootstrap.min.js` | text/javascript | 48910 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/error/js/jquery-3.3.1.slim.min.js` | text/javascript | 69917 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/error/js/popper.min.js` | text/javascript | 19151 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/js/custom.js` | text/javascript | 255446 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/js/developer.js` | text/javascript | 110416 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/js/login.js` | text/javascript | 1412 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/js/main.js` | text/javascript | 54389 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/bootstrap-datepicker.min.js` | text/javascript | 48490 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/bootstrap.min.js` | text/javascript | 51003 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/jquery-3.2.1.min.js` | text/javascript | 86663 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/jquery-ui.js` | text/javascript | 539419 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/jquery.magnific-popup.min.js` | text/javascript | 20219 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/moment.min.js` | text/javascript | 51679 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/morris.min.js` | text/javascript | 35662 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/nice-select.min.js` | text/javascript | 4957 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/owl.carousel.min.js` | text/javascript | 42772 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/popper.js` | text/javascript | 19199 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/print/bootstrap-datetimepicker.min.js` | text/javascript | 38511 |  |
| 200 | GET | `https://jguni.edu.in/public/backEnd/vendors/js/raphael-min.js` | text/javascript | 92142 |  |
| 200 | GET | `https://jguni.edu.in/public/html/JG University Guidelines.html` | text/html | 17288 |  |
| 200 | GET | `https://jguni.edu.in/public/html/admission-open.html` | text/html | 11846 |  |
| 200 | GET | `https://jguni.edu.in/public/html/admission.aspx` | application/octet-stream | 40610 |  |
| 200 | GET | `https://jguni.edu.in/public/html/anti-ragging.html` | text/html | 25393 |  |
| 200 | GET | `https://jguni.edu.in/public/html/doctoral-programmes.html` | text/html | 20838 |  |
| 200 | GET | `https://jguni.edu.in/public/html/enquire.html` | text/html | 13648 |  |
| 200 | GET | `https://jguni.edu.in/public/html/student-grievances.html` | text/html | 18011 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/js/dataTables.responsive.min.js` | text/javascript | 14778 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/js/jquery.dataTables.min.js` | text/javascript | 87103 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/js/jquery.min.js` | text/javascript | 89475 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/js/script.js` | text/javascript | 14347 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/packages/animate-number/multi-animated-counter.min.js` | text/javascript | 736 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/packages/carousel/owl.carousel.min.js` | text/javascript | 44342 |  |
| 200 | GET | `https://jguni.edu.in/public/theme/edulia/packages/zeynep/zeynep.min.js` | text/javascript | 2810 |  |
| 200 | GET | `https://jguni.edu.in/public/vendor/optionbuilder/js/bootstrap.min.js` | text/javascript | 59178 |  |
| 200 | GET | `https://jguni.edu.in/public/vendor/optionbuilder/js/jquery.min.js` | text/javascript | 89500 |  |
| 200 | GET | `https://jguni.edu.in/public/whatsapp-support/scripts.js` | text/javascript | 875 |  |
| 200 | GET | `https://jguni.edu.in/recovery/password` | text/html | 3005 |  |
| 200 | GET | `https://jguni.edu.in/view-page/career?status=error` | text/html | 324263 |  |
| 200 | GET | `https://jguni.edu.in/view-page/cyber-security-programme` | text/html | 342376 |  |
| 200 | GET | `https://jguni.edu.in/view-page/faculty-member` | text/html | 398501 |  |
| 200 | GET | `https://jguni.edu.in/view-page/integrated-bba-mba` | text/html | 346243 |  |
| 200 | GET | `https://linkedin.com/company/99373780/admin/feed/posts/?feedType=following` | text/html | 20557 |  |
| 200 | GET | `https://sst.jguni.in` | text/html | 85302 |  |
| 200 | GET | `https://static.cloudflareinsights.com/beacon.min.js/vce701823e78c4301a35b7e07294d87301792088814092` | text/javascript | 31853 |  |
| 200 | GET | `https://view.vzaar.com` | text/html | 347 |  |
| 200 | GET | `https://x.com/_JGUniversity` | text/html | 157257 |  |

## 2. EXISTS BUT DIFFERENT STATUS (301/302/401/403/405)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 405 | GET | `https://a.nel.cloudflare.com/report/v4?s=q7wwsE957I%2B%2F0D45vTHPDr%2B8SgvNuVe7pRIlPBsTZ%2BFVNcaVFWjXKmNYhnxwQi0mQcMo8%2BjbOGkADZ1VPxhCFtf3hS7BblYVU5Zhdd6nxKruUWi4rCfCs%2FrMuA7WCUI%3D` |  | 0 |  |
| 301 | GET | `https://facebook.com/JGUnIIndia` | text/html | 0 |  |
| 301 | GET | `https://instagram.com/jguniversity` | text/html | 0 |  |
| 302 | GET | `https://jguni.edu.in/activeSmsService` | text/html | 717 |  |
| 301 | GET | `https://jguni.edu.in/career.html?status=error` | text/html | 1162 |  |
| 302 | GET | `https://jguni.edu.in/submit.php` | text/html | 0 |  |
| 302 | GET | `https://n2nsolution.co` | text/html | 154 |  |
| 301 | GET | `https://raphaeljs.com` | text/html | 269 |  |
| 301 | GET | `https://vzaar.com/api/videos` | application/octet-stream | 0 |  |
| 403 | GET | `https://w3.org/2000/svg` | text/html | 5537 |  |
| 302 | GET | `https://wa.me/+917567756758` | text/html | 0 |  |
| 301 | GET | `https://youtube.com/channel/UCyR1OyKN8l2Srj5G0H1WRyg/featured` | application/binary | 0 |  |
| 301 | GET | `https://youtube.com/embed` | application/binary | 0 |  |
| 301 | GET | `https://youtube.com/embed/uvV1q1rH07w` | application/binary | 0 |  |

## 3. OTHER RESPONSES — kept, never discarded

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 404 | GET | `https://img.youtube.com/vi` | image/jpeg | 1097 |  |
| 404 | GET | `https://jguni.edu.in/active-payment-gateway` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/cdn-cgi/l/email-protection` | text/html | 4715 |  |
| 404 | GET | `https://jguni.edu.in/cdn-cgi/scripts/5c5dd728/cloudflare-static` | text/html | 518 |  |
| 404 | GET | `https://jguni.edu.in/cdn-cgi/scripts/5c5dd728/cloudflare-static/email-dec` | text/html | 518 |  |
| 404 | GET | `https://jguni.edu.in/editor/upload-file` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/fees-groups-print` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/fees-payment-invoice-print` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/generate-certificate-print` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/generate-id-card-print` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/news-details/start-assessment.html` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/player?autoplay=true` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/html/include/footer.js` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/html/include/nav.js` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/html/js/jquery-ui.js` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/html/js/swiper-bundle.min.js` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/images/JG Tech Ecosystem/Untitled design (1` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/images/JG Tech Ecosystem/Untitled design (2` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/images/JG Tech Ecosystem/Untitled design (3` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/images/JG Tech Ecosystem/Untitled design (4` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/images/images/_MG_0127.CR2` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/images/images/_MG_0157.CR2` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/public/theme/edulia/js/Moment.js` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/start-assessment.html` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/storage/app/public/optionbuilder/uploads/253305-21-2026_0601pmRecording` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/storage/app/public/optionbuilder/uploads/257505-30-2026_0454pmCoding` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/storage/app/public/optionbuilder/uploads/372905-21-2026_0426pmIMG_8629` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/storage/app/public/optionbuilder/uploads/383305-21-2026_0348pmScreenshot_20260318-170543_Video` | text/html | 11905 |  |
| 404 | GET | `https://jguni.edu.in/storage/app/public/optionbuilder/uploads/635605-21-2026_0601pmGame` | text/html | 11905 |  |
| 404 | GET | `https://player.vimeo.com/video` | text/html | 3648 |  |
| 404 | GET | `https://vimeo.com/api/v2/video` | text/html | 164210 |  |

## 4. DATA FILES (accessible)

| Status | Method | URL | Type | Size | Source |
|---|---|---|---|---|---|
| 200 | GET | `https://autoconfig.jguni.edu.in` | application/xml | 852 |  |
| 200 | GET | `https://jguni.edu.in/cdn-cgi/speculation` | application/speculationrules+json | 151 |  |

## 5. SUBDOMAINS (detailed)

Found **2**, DNS-resolved **2**.

| Host | Resolved | Source |
|---|---|---|
| `autoconfig.jguni.edu.in` | yes | passive |
| `www.jguni.edu.in` | yes | passive |

## 6. VIRTUAL HOSTS (real statuses only)

| Host | Status |
|---|---|
| `autoconfig.jguni.edu.in` | 200 |
| `www.jguni.edu.in` | 200 |
Blocked/noisy vhost checks (403/530/0) are kept in `vhost_blocked.jsonl` (0).

## 7. JS ENDPOINTS (AST, evidence-backed)

_None extracted._

## 8. PARAMETERS

| URL | Params |
|---|---|
| `https://a.nel.cloudflare.com/report/v4?s=%2Bz3QIJNbic%2B3EGeaZwtU%2BNJE54RoVG0imVY%2BpJI2SX7wjo6o3FfKBPRxFGah6EZPhaY9jGu21WQsg2w2b%2Fxr4TerwRurOtpS9YLyQxkE6qt39bIOgMxiKa5YLD32I00%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FDDS0%2BqBTgqGDHYG7fsU8z7NRAIBYST%2BHXQorYu%2F2B2iNuXXHFy6aaaXzK5RUnUwq92Y2tXiKuXPJyJh8fEB7PX0jf6%2Fo5PRD2r0A52qx%2BAIH%2BbjSh6wtMoNhPuiNMY%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=%2FSjQELinTkw0MZfRUlYFX2E7beMfuSBynnQjsAgQC2JUnYKZ72xLvepJKCZ7ycqbjVy%2F5hKfwo2Vt0o3%2BbcP%2BF8a2vdhvnIfv2x8OHP2PblT7CA%2F5ap6f1%2FiprzB5N4%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0LV9mm7S8MVSwTxaCygnHvTauRD0t3nBJhxo7df%2F%2FUX3TZrh4XIO%2BvyGZNKvVvZeoMqmIaVMALRyDOZqqFWjuBnaY7%2Bnh%2B0WdQhPgvOyWLhVzopfk3f6uL0reDgqJ1c%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=0kn9eZ3%2F8yxq1pLtP4ddyDd4A0VgTV6Q2Pym7SGK1ST2EtQDtixPfhVZuFxwDbcvgyEF1%2FOZLRP2icjLXIbNjWdjty7kIWPXtysvQScDntmFxdqYUvlY3Kgy55iAfd8%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=1kFAhwpoKKXcJIMBXa9ltCglxzBykqLPxJAWilt0Oat9IxanovplvhpzsyUfqtIECmPFpHP%2Bse7oNfOreyQbV5KipQHN19FYaDymMHAnjNUmmfadekaBUGZA88Oq54Y%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=2HE1SIj%2FI7LEUmqNOt3xY8Kogn5BriQrQDE%2FIPoV7Ul3DFkeM5G4jUZh%2BoQV6NrNwx%2FU%2BHne25O8Wr8EcBxun5vyFJOWbGaYqNAAaaBGvv1vdnyM0J0Jztmc7gZI8XU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=2RKvkYXvBdsEAzkXj%2Bv4g4Q4ZBS6V2VBBqbPiB20ZAuHYM4WfSMI9NdGuz0ADGcOBnCWS4T8Lbc13c9Zd9y2%2B4JGNKzksJ%2BCeqmQ0CMK7Zq687Xdv1ake%2F4wqvTEOvU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=2XUmS51WNnI91moZTDTDoeIsasJbRshMnV02rKRESvjjFPtOVJ0p3Zg4KWnzBSaTyr9AVfg9jDzPADAA8JtXaXfbWg1imkAHb%2FKrL94YoCcniPq7k%2BQUZbQ4XRpp0s4%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=38tt1yVjjZRS7wPre1uVexdgGavfoU2HpV529BuBryaRksMrX%2FSdOnYsESMjGgbGTXup7%2Fu511RI4IAPoJehTT%2BeoRxTw1ZmmEnawt1DBeac%2FsfN9GVfxfy%2BLzPeRiU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3BzsI1VJvM2%2FQE%2BnLXqcL3e0W9kXqxQLr9yCR%2Bc%2FbcUBSN3YWQ64B6YI6eLKYlUnHKVxcAautAlCugu9TCFUwVtHtoxyfZyOJCNGE7PwrqhNycqqUyKMpsFEp5uOhkU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3LNsl2WhDb%2ByJKio2T0wcSYcuYVsLHfvKi415fkpcGxFiNiBiFhoN5Ph%2FVeGPC%2Fjv9%2BUiZqDJJiKxI4ilIlopfrLg0Srx0%2FYQOQ84md3LP57%2B8isKPp8v7ahf9F4Okw%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3g87Us0W5qbxJVql%2Fkv6dHYWdt7qg0AuFUOJFXJvQqbW6YVUt8QnXceXO5weCpkwm9kTKRCJrg7YZJTg7nkpjgISZAL9VxnIDZFMZCeJXx8BDOid8htfW4PDqm%2BhL9E%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3tZ4bH4naTLD96Vh0u5k%2BQB6Z8qvzy7UzIek%2FbUStHhL%2BvmasMpNXPNS81XSXAahZEz3CqGXM%2FQfKrjF2ph7bkcyvt2yFmL%2B20KESwpKBwmtZRfHTnmN%2BPovRVCGHak%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=3w6LPspJkiVFJjh2GGULOyBuxUYwAFpaxKi3AgYipwJ2HYSywAPboe6%2F6rqkx%2Brt15%2B%2FZ2jxsVaTw64mKRMCfN8oWDQ%2Bo0pHM9ezOCFrOiByEkfhhNhKcUAnY3x7Iyg%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=4O6gZtZp55NU11Bv3iEUHxeSI8lmbkhWI4y8r2sJZrjBKmCrssJ5a7sBAUXS6q3pXPra4FNIc7N08n6sWI6ljDbnSH%2BHRwbH7Yk8xTuhk7mtIPO425fYHQYJE5M77tM%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=5rwX7toRTy66I1BUJ3%2B0JjK2q1KwJxJk8zS%2B9uVRBqXJmcZON1BiMJ9LPlV8EMIXnYZpPPYIByef99zwsHIERKAYYAt2mI1hlOfLDsg9k9VsaEKOOjShetDnDSuqsR4%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=8U2V9LBZ%2BeU4XFeo7%2Fp7AXyb3yaKfIypSZ8b2wP3QUrTrpX5mG1vOO9p61EzQLBnJ7elGYquA%2Fi%2BqEVbucdN%2FgtsvSeAa38rpUXuthrYdmNsvhA5jUIPJlnTojnjY%2FI%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=8Ui9vGACpspYAkGg0EOVCak6tH0Ua4VE5bO5n8FpvrjIpxAlscxEMJMdjA1GSFANw1TKJG0F%2Bg5Rq2QKrH7%2FQToUXizcddc%2FEXIrPuAuWyYixpIzqwJPGlHFvWNj%2FlE%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=9AZTIMMIcyFMEHuHuU6KviqZrMf%2FwDWLUJ%2BHEvm%2FcnyOjIaD1oRhe8hRUDgOLttGa7Au7ejQzA8vPW3akX%2FEgXjuszc0p1%2BuEfI0yV%2BPetpQRfmQn9sBnQVe1gZFMLs%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=9Z%2FlKXJ%2FruCZ%2BuQC5lJjk50lIn6rb4Bxl5XPOCUyqCp3SKQnD%2Bk9rBWDMjeS62l4yzoN4FD8WSJq50Xs3cjgKaYtQ2s%2B11R20hKIfh%2BbozGhWDgKlE2ftz8de3IBBoI%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=9soDDu%2BX8iWOn0GA32uKP1cRd40kaqu989OJVobrk45slY4o0ahWl9rHZjFPJDhv3oq3xXfFSjjzOk0%2Fcg4PoI0uuMvqVtV56D5Q%2BFMeeKkHs%2B0KCOqQPOd2T%2BLa3Hg%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=A15jOUDP2V04jIAAt2YxqtkZfty1Pow2GH%2FLrolJUofBE4dxhQ9osERwnN00n8GsmhD5Eje2RY7vD9IhhqW4hW7TY2OkUOgd0CfYysFlYctA1AqG4F11Fp7n3bYG5xs%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=APRWMs%2BgO9mkXzINJDUNfAubYd%2Bj284Os5oss8Ze8QWVOmdz3Gktw%2FvvMwAKRI4HhqsW3i0oijWqgosiTT97qBcdcb4P9N7ddxzOG02zQ54i12RJHhs8wKQC3gE0wCQ%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=AQ9kg1alxhFm2EzUX1vEhSxt7b7OCWxEhLfPwr%2FAuWSXbDyyk4Pq%2FstD39BqTAeMTtnLu3p5B7oDwwvmZp3ZIL%2BoZRlHJaRu1q0cXKAVo1n9xwd6O70U%2BNA7Iif0K7E%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=B%2BL2hQE0AKdtPPrp0tMC4sDYGpeA%2FMCNy%2F2Bg5ACKIlmhgYDIgsZoTlNwksPmcvIxKbbCty8bOlNkIHkoByWn4kKWyi6RJCCRgVToTMHstt9Rm4Mu2KH0pcYk9Ge280%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=B6Lw8E7XIUZL%2F%2B2RzjGx%2FqF6hWDh3gU1C0cyvkRTvGIRIMwVRAdxXkeIf%2FUssXI3%2Blfta5T%2FogqBYJvCIpqtoD06h3NTUws89YN28mMOAxeFKBr0RFW1VYNKzv02q4E%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=BMDrEXHT7ARsHxmQhwkZSZHBHZZsEEDHYlo7W%2FTIOL0hUsW7%2FBp7QpjBrK2BGk%2BJ7fe3CW2QLN1HYKCZ1PMJwDPgPfVufY6kcp3tmUDKftKWhnETHQjW2%2FXcQILzZzQ%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=ByuizN9PbFMNRx3m9G%2Bs5gn61bAw9VWTsixJpuTyxSvDDnQzTU8fyr%2B2jTVN%2B%2Fk5tqCVyC3fpxPAyrKr3Z88B0kjNkQf%2B9rJqXH8xjX6syR14C09LY74XlcBjaPEwrs%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=CCqiOAIi9MVTuVq0q%2BrzdYRUbnegIpPtLfy5mtu7V22oF%2BEZ4%2FiEMvpx8%2FoF0A8VIkiqKmPyY2axp8qZe4CCCkkPyIzsvB8IlKAtwiWlsrIegY5teFly4aniry6mWqE%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=CDL7CoR0e6rf8c%2By0PEq8JsBcND%2B0VQJBIHgkqPRoHvGD95tqTAGu3goHzEm5Uz2TxHx5g2cu1mJCLBmLzDkkPWZnUKFqfZ5AAXi0v5Fa%2BIk8Y8XEsQtpJplUbz1RQM%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=CHsD2ys3%2Fbr5efXDDqDFn%2BljP3HIzi%2FWrN2XhYJFvmgshONUjR%2FHuCQCGGPSe56PxgWpEIuzQwvZxKJd9WgnJEtmPU3QqvPykbtmoqgumWkl%2BFqvKlPiZfIRU70%2FxE8%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=D%2FQ8gCGUBAx7vdB%2FpAKY0Zb9t1le50qjZhhqWgpDfqd8KhGkLSQdv9VLFuvCVMyi7NwVr%2BZXAKJ%2FXRLGjzzi9l3yiA02yhWArVdWzPWLBodznXMqgNds6KTCszeEAag%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=D8wRMgi0diG6K%2FpWuHpyJtjNaI9GuGJdt%2BFVCHarYueUTKiN1NhN0vziGAsdQM%2FDRW3cDAzkgsuYYiDQof89eFeV5wqPpa5buSn3UAmZTDqAzYjhv%2Fa8dBSfTMt732Q%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=DPaDvarqloyH1WVbkge1BMoG7b4FlAqrEiTBcnwuQdeponoyqg6ia59ZBIWHGmWxX9cKiJGb4b5zRTNKQC1kY1s%2Bp%2Bm4%2FojM7LU59fOjL24qbyoYSnQKzHYqxja%2BFgI%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=Fr4IOHTksE1au45YChLpGyd1I7u9uZoE2F9DSku8EoG40qOZMnTzWsFFOX9Xm82mw1Apb4gl%2FIRq8AKK8TLeJ6kDDFSCeZ896vRZRR5lt66YsKcyuXgFuw4HU5XtMsc%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=GATErUJgTDvCBnuyHb7xQvZaI%2BwfgAOcidLlg%2BhSji%2B5AubDVIGihYxq95GSuUKFs1sYtWLMqrt0%2BQj6ZygefLMamsh6Hln2hrahutd2Ucgg7qiMBuibnnb5pjO7F94%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=GckaILxa8DkUVHarz3t8Xc6%2FM7EiNZNpPEiLJTmzYu%2F%2FoGrxXvXvOZxxuAGTTMtCI8J0pKSZZWbKUXR1cGLEUIakqQrbPLyPwl5ycIoM2pwrziEn0z87iR4KTdNBVNk%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=GwpU3pC%2BYssv6fcjKwshypkYc15XriEkdRf%2BhbhJiWR%2BmE2xuv6mYWMyF3iyBgRYUSx%2BiZFW1wSAy7xtQAGAGQMzWQ2GcKL3o3yFz%2FaH1DomrYQwIxrhXSaGt7ID138%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=HY42SqNZkvq8bs2UO%2F0lHBaQxouBvcxoxVzpI%2BFQiMLdkZb5ytj%2F%2FvzgZtWMYhnytbBc39VacH4i2LlaJiQBtncgiYEgm%2FZZLNQslmxz19SlbZtSUYjoEiADKZgsstk%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=IUwSNxdZqehc4CCZh8zRMvRBIBFBfUc%2Ffvi8NWeIuFxgYmyYUmeDBd7WcJ7MkNxqiTk73FB3%2FT7ApN3e%2BN4DzYvuMqv14TyqDS11vnjhh3j7JjtDhMrkDjEUJThqcnc%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=IcbDpfRxV9tkNYMPIsBl6NcKz2fFq3MR4y%2B1evrLeJTlpDqnFzDZnY4pKtfeXsyGiP%2BEH7mYxv%2FdOQni075bw8nQ3churS3mbo0K3Va1e2k5trXqxo%2Bkd8zSst8WvrY%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=J%2BYnXOoT9MgK%2B8JgyZdvKQy4Sjjb6uBIYzm4JvuPyP%2FlLoVsqZ%2BOzg66asAbBDSt9PbHY2Qybv%2FZUYkKOuUX9AzllIVnFpHy9s40Sv3D5Hfd5IlTPtFqL%2BH3LSzW9XI%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=KWBW0Z2THrdyeNUTEIzLZx3z3ojTsVVREiD9SlhQT2RDNJK%2BEr5RtV9D0ClN5naEOm33ZmZCfHYPMMrYEkyRuS%2FNikR6333TfQukaDTLxAxlVk90l2bfokm8TT18gTU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=L3Fj2jquHVqTSRziqyReIRxjaKb9FMBNOCgzJltRcVbC%2F1%2BMEUKZRsPhhejRwWlDROYYNZJMAkZHvPj4y%2BDX5Q2o%2FIh1VYbRx33KvR9tZLzBEyR0fkzW2cAQVDXKBGU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=MQrZ%2Fgzk4JvrsY3J462Xi4LZDoF7KyPVFZoqTcDhXmcQGPXYXzgaNPpXTwsnIcV1QZ6OnT%2B%2FSkjkwU8mgYvSb65p6TnJTwZoZbm68vgFD8H%2BjRSvzW5L4XQUNu67jAQ%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=MYY6M8tNdpRFo%2B9wcmT3J6NHIfBqlNfcCyvGheP5N%2FDdSU5AotpNguxoLhIlMnr9peoxziMzJnbRVrMkE%2FSb5DjhogK1z77M29JxxERlqH2sAw%2BPUvMPTr0f8KQLYM0%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=MsQMtndbUp6NsN8m%2FHl1dkWjUezHTaT0c0qy%2Bd2L7Gr9G8jZrJ5vd9JbqlsstA5AAWsjNh6qqXSlFvP3k0i5uSxwgWX6Br5VMquxVBDT1SKYKOsAzhegBea8KX6HZr0%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=N%2Bgs1rYq7%2FGzzWJ2D%2B7IJAxL0fTXFnL54EczbK8%2FcOmeYkPj97KQzAdmi15%2BeuZuF8q5hSL70YxV85TWxmxUa%2Bdn6z1h1Bmx5f6TLW%2Bl6PBtRjGdS75vyAakyzMgfFU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=NjxTC67mGAVYiMj2LZRE5Tmrd6C9mC6LpA0QYQbcBkwRlfM5AkvWHgabvhw%2FBuhvrtq9i9e31bPiYDa%2F8l3SML3c4UEts%2BSPLdQV6bCfN4NuzvK5VH2ejeOngaqUH68%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=O%2FCxih%2FMJWqNHtgFmw5ivwXKbjk1B5O0tgeDGtAj67vwLJ2szwWy8oS37aRWTs5HGygPZ0v6S78%2FPhoOWWbyCQ22IYOalqFtIbbU3RkrsyUXPJM61jvuwJBK6SeOqAw%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=ONOpkgeBeCFozTmkSX3EdxovdLCuqf%2Blzrqa5qmReMQQQnotEeErXKa7oC7gobICvw%2BS9VmqPf4DhTDiCsJNjB8MBmgje9TWAct%2BH%2FtXsqJHspkMZ3y9r2h1nyUwewk%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=OWhfZMp49jMBEtKZNjCGKFF8f3k9%2BowHmG5jR7AnZ078Fc6ArlPkEKRxj2lONGxs2s073QkJSkjKR%2BIuNMf8aKkhHweGD%2FgAzGaHyUhQ1%2BLL70vkmVBYokTXeLz57lY%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=P1xUdY44w8SCNidpboiBs9pV5DRe14uXH6G5P0UlBKNNMGt8zuN6Ic1e%2FqIUKDcRaZ8EZZmIyGjv%2BIBm%2FF2EHwPdGfY15DQfbAARBn4c%2Bb0siOGuwRJ6ZiVzKvEYYQw%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=PAq5uQCtfNug1aCOM6uwzQwibF952moOTov4uvochAjaFN50PPqB%2FamEz42BzbHEn9NrTf4H8uJZDRZ1Lvm9JEZfhzmWftaiQlLf%2FCKh%2BmRP%2Fzfz7jwFkYGU1czL%2Buw%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=PQ1gZToYp%2BmPd0ygQrmEAwPdvuKQEnjUdGc5olH8laVYvUbRFW3mjal3Gj0oksNmBRYsRaWBRFbmKxVefVRoHZ%2BrS1QSfN%2BiYV2KVa5f7wHSaUAnBvexLruVPD306x4%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=Qi6y%2F2o4ZCIPTDtn2KMEgGHOg2IAdlR4rRUX8ioYBDLIbP7MW2QB282oqmn40kO2vM2hmM9A0d%2FYxQKOzU2a4IYvojMe5gKuVoa%2BFN3myrIQVHuaBLhnpuNHhbNyUnE%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=R1DFWYrwWgwV0DJ%2FB32oBRZKfG7qs25v8Wx8ZOsMQF5487SzkrAaneqVpTN84r963SrjYg1vY8mMPailBTXHeyScAkoDvtsUcBhPJG5q1UHSdpDTRNTVZQozA8DCmaw%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=RJCXXtl44az0ytLTd3CGvPddCPBTgJlEtw9HYTQLKe4cFZBPLKTPv71MjsJpXGx4ytG2dlLO92uyfyqpESf%2Bm0W8LdzM8yjkkBMA3%2BogDuCzZwLCA8Wy9VVkavHJrIU%3D` | s |
| `https://a.nel.cloudflare.com/report/v4?s=RLlsE5dum4gYFYjtpPKOokXmmjRfgSJwz8Al64fBDcVRzNaEA%2FoQC1m8%2Ft618BUJvp591Pl6v9fQgaoxJeopxZ6A2DJLCv1JJabwjqldq9AW7JVZBTJTuDTC93dzrKY%3D` | s |

## 9. SECRET CANDIDATES

_None found._

## 10. TOOL RUN STATUS (no silent skips)

| Tool | Result | Detail |
|---|---|---|
| `anastasis` | exit 254 | no output produced — see logs/ |
| `dnsx` | OK | completed |
| `ffuf` | OK | off by choice — wordlist prepared |
| `gau` | OK | completed |
| `gospider` | OK | completed |
| `httpx` | OK | completed |
| `js-download` | OK | 40 chunks saved over 3 round(s) |
| `jscope` | OK | completed |
| `jsluice` | OK | 40 files parsed |
| `katana` | exit 124 | see logs/ |
| `methods` | OK | 476 method responses |
| `subfinder` | OK | completed |
| `trufflehog` | OK | completed |
| `uncover` | OK | no API key configured — no external data |
| `urlfinder` | OK | completed |
| `uro` | OK | completed |
| `vhost` | OK | 2 real of 2 tested |
| `x8` | OK | parameter scan complete |

## 11. INTENTIONALLY NOT RUN

- **ffuf path brute** — off by default; `wordlist.txt` is ready. Set `enable_brute: true` later.
- **kiterunner** — off by default alongside ffuf.

## 12. OUTPUT FILES

| File | Meaning |
|---|---|
| [`all_routes.jsonl`](all_routes.jsonl) | every route, unfiltered (102,581 B) |
| [`accessible_200.jsonl`](accessible_200.jsonl) | HTTP 200 wins (60,200 B) |
| [`exists_blocked.jsonl`](exists_blocked.jsonl) | exists but blocked (10,832 B) |
| [`other_status.jsonl`](other_status.jsonl) | all other statuses (28,827 B) |
| [`data_files.jsonl`](data_files.jsonl) | JSON/CSV/XML among 200s (1,500 B) |
| [`params.jsonl`](params.jsonl) | parameters (35,952 B) |
| [`subdomains.jsonl`](subdomains.jsonl) | subdomains + resolution (163 B) |
| [`third_party_routes.jsonl`](third_party_routes.jsonl) | third-party URLs — kept, not deleted (40,991 B) |
| [`method_responses.jsonl`](method_responses.jsonl) | all method-probe responses — kept (61,746 B) |
| [`vhost_real.jsonl`](vhost_real.jsonl) | non-blocked virtual hosts (105 B) |
| [`vhost_blocked.jsonl`](vhost_blocked.jsonl) | blocked vhost checks — kept (0 B) |
| [`js_endpoints.jsonl`](js_endpoints.jsonl) | AST endpoints (0 B) |
| [`vhost.jsonl`](vhost.jsonl) | all vhost checks (105 B) |
| [`jsluice.jsonl`](jsluice.jsonl) | JS-derived URLs (21,718 B) |
| [`gospider.txt`](gospider.txt) | second crawler URLs (11,408 B) |
| [`jscope.txt`](jscope.txt) | evidence-ranked JS analysis (12,317 B) |
| [`secrets.jsonl`](secrets.jsonl) | secret candidates (0 B) |
| [`wordlist.txt`](wordlist.txt) | target-specific fuzz list (54,018 B) |
| [`params.txt`](params.txt) | parameter wordlist (19 B) |
| [`js_urls.txt`](js_urls.txt) | JS chunk URLs (2,671 B) |
| [`logs/`](logs/) | raw tool logs (4,096 B) |

## Status meaning

| Status | Meaning |
|---|---|
| 200 | Accessible — confirmed win |
| 301/302/307/308 | Redirect — route exists |
| 401/403 | Exists but blocked |
| 405 | Exists, wrong method |
| 404 | Not found — kept for completeness |
| 530 | Cloudflare error — excluded from vhosts |

> Collect wide, verify status, categorize last. Nothing deleted from data files.