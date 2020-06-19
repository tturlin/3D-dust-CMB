import numpy as np
import matplotlib.pyplot as plt

N = 64

if N == 64:
    lon, lat, a, m, s = np.loadtxt("temp_rohsa_res64.dat", unpack=True)
    mn = 0.0023456318082015495 # !!! pour N=64
else:
    lon, lat, a, m, s = np.loadtxt("temp_rohsa_res.dat", unpack=True)
    mn = 0.0023172528573618934 # !!! pour N=16

def gaussian(x, A, mu, sig):
    return A * mn * np.exp(-(x - mu)**2 / (np.sqrt(2) * sig)**2)

a *= mn
# lat.astype(int)
# lon.astype(int)

dist = 500
step = 5


m *= step
s *= step

abscisse = range(step, dist, step)

data = np.zeros((12, N, N, len(abscisse)))  # shape : compo, lon, lat, dist

index = 0
# reconstruction data
# si tracé par compo, amplitude intégré de la composante
for i in range(N):
    for j in range(N):
        for k in range(12):
            data[k, i, j] += gaussian(abscisse, a[index], m[index], s[index])
            index += 1

# carte amplitude intégrée
amp_int = np.sum(data, axis=3)
print(amp_int.shape)

for i in range(12):
    plt.figure()
    plt.imshow(amp_int[i], origin='lower', extent=[169,179, -18, -8])
    plt.title("Comp {}, ampli integree".format(i))
    plt.savefig("int/compo{}.png".format(i))
    plt.close()

# carte totale
amp_tot = np.sum(amp_int, axis=0)
print(amp_tot.shape)
plt.figure()
plt.imshow(amp_tot, origin='lower', extent=[169,179, -18, -8])
plt.title("Ampli integree sur la distance et les composantes".format(i))
plt.savefig("ampli.png")
plt.close()


#carte amplitude par composante
amp_compo = np.zeros((12, N, N))
mean_compo = np.zeros((12, N, N))
sig_compo = np.zeros((12, N, N))

x = np.linspace(169, 179, N)
y = np.linspace(-18, -8, N)
XX, YY = np.meshgrid(x, y)

for i in range(12):
    index_amp = range(i, len(lon), 12)
    amp_compo[i] = np.array(a[index_amp]).reshape((N,N))
    mean_compo[i] = np.array(m[index_amp]).reshape((N,N))
    sig_compo[i] = np.array(s[index_amp]).reshape((N,N))

    plt.figure()
    plt.title("Comp {}, flat ampli, contour mean".format(i))
    plt.imshow(amp_compo[i], vmin=0, vmax=5, origin='lower', extent=[169,179, -18, -8])
    plt.colorbar()
    plt.contour(XX, YY, mean_compo[i], cmap='jet')
    plt.colorbar()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("amp/mean/compo_{}".format(i))
    plt.close()

    plt.figure()
    plt.title("Comp {}, flat ampli, contour sig".format(i))
    plt.imshow(amp_compo[i], vmin=0, vmax=5, origin='lower', extent=[169,179, -18, -8])
    plt.colorbar()
    plt.contour(XX, YY, sig_compo[i], cmap='jet')
    plt.colorbar()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("amp/sig/compo_{}".format(i))
    plt.close()


    plt.figure()
    plt.title("Comp {}, flat mean, contour sig".format(i))
    plt.imshow(mean_compo[i], vmin=1, vmax=500, origin='lower', extent=[169,179, -18, -8])
    plt.colorbar()
    plt.contour(XX, YY, sig_compo[i], cmap='jet')
    plt.colorbar()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("mean/sig/compo_{}".format(i))
    plt.close()

    plt.figure()
    plt.title("Comp {}, flat mean, contour ampli".format(i))
    plt.imshow(mean_compo[i], vmin=1, vmax=500, origin='lower', extent=[169,179, -18, -8])
    plt.colorbar()
    plt.contour(XX, YY, amp_compo[i], cmap='jet')
    plt.colorbar()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("mean/ampli/compo_{}".format(i))
    plt.close()


    plt.figure()
    plt.title("Comp {}, flat sig, contour mean".format(i))
    plt.imshow(sig_compo[i], vmin=0, vmax=np.max(sig_compo[i]), origin='lower', extent=[169, 179, -18, -8])
    plt.colorbar()
    plt.contour(XX, YY, mean_compo[i], cmap='jet')
    plt.colorbar()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("sig/mean/compo_{}".format(i))
    plt.close()

    plt.figure()
    plt.title("Comp {}, flat sig, contour ampli".format(i))
    plt.imshow(sig_compo[i], vmin=0, vmax=np.max(sig_compo[i]), origin='lower', extent=[169,179, -18, -8])
    plt.colorbar()
    plt.contour(XX, YY, amp_compo[i], cmap='jet')
    plt.colorbar()
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.savefig("sig/ampli/compo_{}".format(i))
    plt.close()


dat = np.loadtxt("temp_rohsa_{}.dat".format(N), skiprows=1)
res = np.loadtxt("temp_rohsa_res{}.dat".format(N))

dlen_x = int(np.max(dat[:, 1])) + 1
dlen_y = int(np.max(dat[:, 2])) + 1
dlen_z = int(np.max(dat[:, 0])) + 1

rlen_x = int(np.max(res[:, 0])) + 1
rlen_y = int(np.max(res[:, 1])) + 1

m_dat = np.zeros((dlen_x, dlen_y, dlen_z))
m_res = np.zeros((rlen_x, rlen_y, dlen_z))

print(rlen_x, dlen_x)

x = np.arange(dlen_z)

for i in range(dat.shape[0]):
    m_dat[int(dat[i, 1]), int(dat[i, 2]), int(dat[i, 0])] += dat[i, 3] * mn

for i in range(res.shape[0]):
    m_res[int(res[i, 0]), int(res[i, 1]), :] += gaussian(x, res[i, 2], res[i, 3], res[i, 4])


fig, axs = plt.subplots(rlen_x, rlen_y)
for i in range(rlen_x):
    for j in range(rlen_y):
        axs[i, j].plot(m_dat[i, j])
        axs[i, j].plot(m_res[i, j])
        axs[i, j].set_xticks([])
        axs[i, j].set_yticks([])
plt.savefig("Profils extinction.png")
plt.close()

plt.figure()
plt.plot(m_dat[16,16], label="data")
plt.plot(m_res[16,16], label="ROHSA")
for i in range(12):
    plt.plot(gaussian(x, res[16*64+16+i, 2], res[16*64+16+i, 3], res[16*64+16+i, 4]), label='compo {}'.format(i))
plt.title("spectre located in pix {} {}".format(16,16))
plt.xlabel("Distance")
plt.legend()
plt.savefig("pix_16_16.png")
plt.close()

plt.figure()
plt.plot(m_dat[16,48], label='data')
plt.plot(m_res[16,48], label='ROHSA')
for i in range(12):
    plt.plot(gaussian(x, res[16*64+48+i, 2], res[16*64+48+i, 3], res[16*64+48+i, 4]), label='compo {}'.format(i))
plt.title("spectre located in pix {} {}".format(16,48))
plt.xlabel("Distance")
plt.legend()
plt.savefig("pix_16_48.png")
plt.close()

plt.figure()
plt.plot(m_dat[48,16], label='data')
plt.plot(m_res[48,16], label='ROHSA')
for i in range(12):
    plt.plot(gaussian(x, res[48*64+16+i, 2], res[48*64+16+i, 3], res[48*64+16+i, 4]), label='compo {}'.format(i))
plt.title("spectre located in pix {} {}".format(48,16))
plt.xlabel("Distance")
plt.legend()
plt.savefig("pix_48_16.png")
plt.close()

plt.figure()
plt.plot(m_dat[48,48], label='data')
plt.plot(m_res[48,48], label='ROHSA')
for i in range(12):
    plt.plot(gaussian(x, res[48*64+48+i, 2], res[48*64+48+i, 3], res[48*64+48+i, 4]), label='compo {}'.format(i))
plt.title("spectre located in pix {} {}".format(48,48))
plt.xlabel("Distance")
plt.savefig("pix_48_48.png")
plt.close()

plt.figure()
plt.plot(m_dat[32,32], label='data')
plt.plot(m_res[32,32], label='ROHSA')
for i in range(12):
    plt.plot(gaussian(x, res[32*64+32+i, 2], res[32*64+32+i, 3], res[32*64+32+i, 4]), label='compo {}'.format(i))
plt.title("spectre located in pix {} {}".format(32,32))
plt.xlabel("Distance")
plt.savefig("pix_32_32.png")
plt.close()