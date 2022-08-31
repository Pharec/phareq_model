
# Dataset collection

1. Find Top domains (target to phishing)
2. Crawl (using spidy) to find URLs of pages associated with each domain
3. Collect screenshots (using splinter) of the list of URLs

# Setup for dataset collection

pip install selenium splinter

wget https://moz.com/top-500/download?table=top500Domains -O top500Domains.csv

# New Dataset collected
### Trusted sites:
- Number of domains = 72
- Number of images = 12740
- Source: domains seed list from a combination of sources (mostly done manually)
### Phishing sites:
- Number of URLs = Number of images = 515
- Source: Phishtank (filtered on active -> then cleaned manually)

# New collection method:

Rather than collecting in two steps, we simulate browsing but in an exhustive
way with parametrized limits. This can be done using splinter to crawl as
well as collect images
