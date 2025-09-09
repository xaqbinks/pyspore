import pygame
import numpy as np

SAMPLE_RATE = 44100

def generate_sound(wave_type='sine', frequency=440, duration=0.5, volume=0.5, attack_s=0.01, decay_s=0.01):
    """
    Generates a sound with a specified wave type and a simple AD envelope.
    :param wave_type: 'sine', 'square', 'sawtooth', 'noise'
    :param frequency: Frequency in Hz.
    :param duration: Duration in seconds.
    :param volume: Volume from 0.0 to 1.0.
    :param attack_s: Attack time in seconds.
    :param decay_s: Decay time in seconds.
    :return: A pygame.Sound object.
    """
    num_samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0., duration, num_samples, endpoint=False)

    # Generate wave
    if wave_type == 'sine':
        wave = np.sin(2. * np.pi * frequency * t)
    elif wave_type == 'square':
        wave = np.sign(np.sin(2. * np.pi * frequency * t))
    elif wave_type == 'sawtooth':
        wave = 2 * (t * frequency - np.floor(0.5 + t * frequency))
    elif wave_type == 'noise':
        wave = np.random.uniform(-1, 1, num_samples)
    else:
        wave = np.zeros(num_samples)

    # Apply simple Attack-Decay envelope
    attack_samples = int(SAMPLE_RATE * attack_s)
    decay_samples = int(SAMPLE_RATE * decay_s)

    if attack_samples > 0:
        attack_envelope = np.linspace(0, 1, attack_samples)
        wave[:attack_samples] *= attack_envelope

    if decay_samples > 0:
        decay_envelope = np.linspace(1, 0, decay_samples)
        wave[-decay_samples:] *= decay_envelope

    # Scale to 16-bit and create stereo
    wave = (wave * (2**15 - 1) * volume).astype(np.int16)
    stereo_wave = np.repeat(wave.reshape(num_samples, 1), 2, axis=1)

    return pygame.sndarray.make_sound(stereo_wave)
