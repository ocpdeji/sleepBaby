# Images — How to replace any image

Drop a file with the **exact same name** into this folder and push to GitHub.
Netlify will redeploy automatically and your new image goes live.

---

## Hero banner

| File | Used on |
| --- | --- |
| `hero2.jpg` | Home page hero (right side) |

**To replace:** save your image as `hero2.jpg` and drop it here.

---

## Kate's photo

| File | Used on |
| --- | --- |
| `kate.jpg` | Home page "Meet Kate" section, About page, blog author bio |

**To replace:** save your photo as `kate.jpg` and drop it here.

---

## Product covers — `products/` folder

| File | Product |
| --- | --- |
| `products/book.jpg` | Sleep, Baby. Please. ($19.99) |
| `products/bundle.png` | Premium Bundle ($39.99) |
| `products/toddler.png` | Toddler Bedtime Kit ($12) |
| `products/newborn.png` | Newborn Starter Kit ($9) |

**To replace:** drop a new file with the same name into `products/`.
PNG or JPG both work — just keep the same extension.

---

## Blog covers — `blog/` folder

Blog posts currently use Unsplash URLs (clean, purpose-shot baby photos).
If you want to use your own images instead:

1. Drop your image into `blog/` with one of these names:
   - `wake-windows.jpg`
   - `regression.jpg`
   - `sleep-train.jpg`
   - `contact-nap.jpg`
   - `3-minute-pause.jpg`

2. Open the matching `.mdx` file in `content/blog/` and change the `cover:` line from the Unsplash URL to `/images/blog/your-filename.jpg`

---

## Social share image (Open Graph)

| File | Used for |
| --- | --- |
| `og-default.jpg` | Preview image when someone shares your site on social media |

Ideal size: **1200 × 630 px**

---

## Tips

- Images are served directly — no resizing happens automatically. Keep files under 500 KB where possible.
- JPG is best for photos. PNG is best for graphics with text or transparent backgrounds.
- After dropping a file in, run `git add . && git commit -m "update image" && git push` and Netlify redeploys in ~2 minutes.
