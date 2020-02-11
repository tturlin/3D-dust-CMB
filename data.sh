#!/usr/bin/fish

mkdir -p data
cd data

# Planck data
mkdir -p planck
cd planck

wget https://pla.esac.esa.int/pla-sl/data-action?MAP.MAP_OID=9300 -O ThermalDustModel_2048_R1.fits --timeout=0