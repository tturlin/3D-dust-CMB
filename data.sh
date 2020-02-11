#!/usr/bin/fish

mkdir -p data
cd data

# Planck data
mkdir -p planck
cd planck

wget -O ThermalDustModel_2048_R1.20.fits "http://pla.esac.esa.int/pla/aio/product-action?MAP.MAP_ID=HFI_CompMap_ThermalDustModel_2048_R1.20.fits"

cd ..

# HI4PI data
mkdir -p hi4pi
cd hi4pi

wget -O NHI_HPX.fits "https://lambda.gsfc.nasa.gov/product/foreground/fg_hi4pi_get.cfm"