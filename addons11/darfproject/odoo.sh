#!/usr/bin/env bash

docker run -d -p 8069:8069 --name odooweb --link dbweb:db  \
    --mount type=bind,source=/home/st/Desktop/DARF-ANGeles/addons11,target=/mnt/extra-addons \
    --mount type=bind,source=/home/st/Desktop/DARF-ANGeles/filestore,target=/var/lib/odoo/filestore \
     -t odooweb1
# если не замонтировалось то 
# mount -B /home/st/Desktop/DARF-ANGeles/addons11 /var/lib/docker/volumes/afa663a7ef7f8425b44847d94d6cc381144c3e89d21921d0b5ad241485506cb1/_data/addons/11.0
