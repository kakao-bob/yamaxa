<h4 align="center"><a href="/README.md">Русский</a> | <a href="/READMEen.md">English</a></h4>

# YaMAXa
## Yet Another MAX API

Python library for implementing MAX bots using **long polling**.

## Installation
Download the `.whl` file from the latest release and install it:
```bash
pip install yamaxa-latest.whl
```

## Documentation (WIP)
Most of the API has been mirrored from the [official documentation](https://dev.max.ru/docs-api).
The basics of working with the bot are covered in [`example.py`](/example.py).

> [!WARNING]
> Starting July 19, 2026, MAX developers mandate the use of Ministry of Digital Development (Mincifry) certificates to avoid SSL errors due to migration to a new domain. The combined root and intermediate [certificate](https://www.gosuslugi.ru/crt) is already built into `yamaxa` (`certs/russian_chain.pem`) and requires no additional configuration. A library patch extending its validity will be released before it expires (**March 6, 2027**).


## License
This repository is licensed under the ISC License. Read more: [LICENSE](/LICENSE)