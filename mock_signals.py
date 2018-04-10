import numpy as np
import nifty4 as ift


def mock_signal_energy_time(t_pix, t_volume, e_pix, e_volume):

    time_domain = ift.RGSpace(t_pix, distances=t_volume / t_pix)
    energy_domain = ift.RGSpace(e_pix, distances=e_volume / e_pix)
    domain = ift.DomainTuple.make((time_domain, energy_domain))
    s = ift.Field(domain, val=np.ones((t_pix, e_pix), dtype=np.float64) * 100)

    # apply some distribution to make signal look more realistic
    #s = ift.Field(x1, val=np.random.poisson(s.val))
    return s


def mock_signal_time(npix):

    total_volume = 127.  # total length, here about 350s

    # setting signal parameters
    lambda_s = .5  # signal correlation length
    sigma_s = 1.5  # signal variance

    # calculating parameters
    k_0 = 4. / (2 * np.pi * lambda_s)
    a_s = sigma_s ** 2. * lambda_s * total_volume

    # creation of spaces
    x1 = ift.RGSpace(npix, distances=total_volume / npix)
    k1 = x1.get_default_codomain()

    # # creating power_field with given spectrum
    spec = (lambda k: a_s / (1 + (k / k_0) ** 2) ** 2)
    S = ift.create_power_operator(k1, power_spectrum=spec)

    # creating FFT-Operator and Response-Operator with Gaussian convolution
    HTOp = ift.HarmonicTransformOperator(domain=k1, target=x1)

    # drawing a random field
    sk = S.draw_sample()
    s = HTOp(sk)

    # apply some distribution to make signal look more realistic
    s = ift.Field(x1, val=np.random.poisson(s.val), dtype=np.float64)

    #ift.plot(s, name='./trash/mock_signal_time.png')

    return s


if __name__ == "__main__":
    mock_signal_time()


def mock_signal_energy(npix):
    # setting spaces
    total_volume = 127.  # total length, here about 350s
    x1 = ift.RGSpace(npix, distances=total_volume / npix)
    s = ift.Field(x1, val=np.ones(npix, dtype=np.float64) * 100)
    # apply some distribution to make signal look more realistic
    s = ift.Field(x1, val=np.random.poisson(s.val))
    return s
