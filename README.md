
### Monitoring Vaksinasi
Script sederhana untuk memonitor perkembangan vaksinasi oleh Kementrian Kesehatan RI

### Live API
- [Cekdiri](https://cekdiri.id/vaksinasi/)
- [Mamajahit](https://mamajahit.id/vaksinasi/)

## Pre-requisites
1. python3


## Setup
1. Clone this repo: `git clone https://github.com/lantip/monitoring-vaksin.git`
2. CD into this repo: `cd monitoring-vaksin`
3. Install python requirements: `pip install -r requirements.txt`

## Cron
1. Jalankan crontab tiap sepuluh menit di antara jam 15:00 sampai 16:50, karena update dari kemkes biasanya di jam segitu

`0/10 15-16 * * * /path/to/python /path/to/repo/main.py`

## API
1. Jalankan `python serve.py` untuk serve API di http://localhost:5000
