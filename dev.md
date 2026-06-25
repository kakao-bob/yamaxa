Склеить сертификаты:

```bash
cat russian_trusted_root_ca_pem.crt > russian_chain.pem
echo "" >> russian_chain.pem
cat russian_trusted_sub_ca_pem.crt >> russian_chain.pem
```