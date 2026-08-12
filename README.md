# Dealer Ultimate

Site demo + **public media** for GoHighLevel.

**Repo:** https://github.com/AFROAgencyAI/dealer-ultimate  
**Media CDN (jsDelivr):**  
`https://cdn.jsdelivr.net/gh/AFROAgencyAI/dealer-ultimate@main/media/`

## GHL paste

Open [`ghl-paste/demo-ghl-paste.html`](ghl-paste/demo-ghl-paste.html) (or `index-ghl.html`) and paste the full file into a GHL blank/custom HTML page.

All image `src` values are absolute jsDelivr URLs pointing at this repo’s `media/` folder. No GHL Media Library upload required for static art.

## Local preview

```bash
cd dealer-ultimate-site
python3 -m http.server 8080
# open http://localhost:8080/demo.html
```

## Media

| File | Use |
|------|-----|
| `du-hero-1.png` | Hero |
| `du-more-buyers-1.png` / `du-more-inventory-1.png` | How it works |
| `du-service-1.png` … `3.png` | Solutions cards |
| `du-contact-1.png` | Contact / lead form |
| `du-logo-mark.png` | Logo |
| `trust-*` | Trust marquee |
| `testimonial-*` | Testimonials |

## Note

Lead form is front-end only until you wire a GHL form or webhook.
