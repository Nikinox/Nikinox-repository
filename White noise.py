#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Mini terminale per rumore bianco in Python.

Funzionalità:
- Verifica/installa librerie necessarie (numpy, scipy, sounddevice, matplotlib) usando subprocess.
- Genera rumore bianco (gaussiano) con numpy.
- Riproduce il rumore bianco con sounddevice.
- Salva il rumore bianco in un file WAV con scipy.
- Visualizza il segnale e lo spettro con matplotlib.
- Interfaccia testuale semplice per eseguire le operazioni.

Nota: Esegui questo script con Python 3.6+.
"""

import sys
import subprocess
import importlib
import shutil
from typing import List, Tuple


# -----------------------------
# Sezione: gestione dipendenze
# -----------------------------

def pip_available() -> bool:
    """
    Controlla se 'pip' è disponibile tramite 'python -m pip'.
    Usiamo sys.executable per puntare allo stesso interprete che esegue lo script.
    """
    try:
        # 'python -m pip --version' per verificare l'invocazione senza installare nulla.
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False


def install_packages(packages: List[str]) -> List[Tuple[str, bool, str]]:
    """
    Installa i pacchetti richiesti usando 'python -m pip install <package>'.
    Ritorna una lista di tuple (package, success, message).
    """
    results = []
    for pkg in packages:
        print(f"\n[INFO] Installazione di '{pkg}'...")
        try:
            proc = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", pkg],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )
            success = proc.returncode == 0
            message = proc.stdout if success else proc.stderr
            print(message)
            results.append((pkg, success, message))
        except Exception as e:
            msg = f"Errore durante l'installazione di {pkg}: {e}"
            print(msg)
            results.append((pkg, False, msg))
    return results


def ensure_import(module_name: str) -> bool:
    """
    Prova ad importare un modulo. Se fallisce, ritorna False.
    """
    try:
        importlib.import_module(module_name)
        return True
    except Exception:
        return False


def ensure_dependencies() -> None:
    """
    Verifica e installa tutte le dipendenze necessarie.
    Pacchetti scelti:
    - numpy: generazione del rumore bianco (random gaussiani).
    - scipy: salvataggio WAV (scipy.io.wavfile).
    - sounddevice: riproduzione audio cross-platform.
    - matplotlib: visualizzazione del segnale e dello spettro.
    """
    required = ["numpy", "scipy", "sounddevice", "matplotlib"]

    print("[INFO] Verifica disponibilità di pip...")
    if not pip_available():
        print("[ERRORE] 'pip' non è disponibile tramite 'python -m pip'.")
        print("Prova ad aggiornare Python o a installare pip. Interrompo.")
        sys.exit(1)

    # Controllo rapido: se tutti i moduli sono già importabili, saltiamo l'installazione
    missing = [m for m in required if not ensure_import(m)]
    if not missing:
        print("[OK] Tutte le dipendenze sono già presenti.")
        return

    print(f"[INFO] Mancano i seguenti pacchetti: {', '.join(missing)}")
    results = install_packages(missing)

    # Riprova import dopo installazione
    still_missing = [pkg for pkg, success, _ in results if not success or not ensure_import(pkg)]
    if still_missing:
        print(f"[ERRORE] Non sono riuscito a rendere disponibili: {', '.join(still_missing)}")
        print("Controlla gli errori mostrati sopra. Interrompo.")
        sys.exit(1)
    else:
        print("[OK] Dipendenze installate e importabili.")


# ---------------------------------
# Sezione: logica rumore e utilità
# ---------------------------------

def generate_white_noise(duration_sec: float = 2.0, sample_rate: int = 48000, amplitude: float = 0.2):
    """
    Genera rumore bianco gaussiano:
    - duration_sec: durata in secondi.
    - sample_rate: campioni al secondo (Hz).
    - amplitude: livello di uscita (0..1 circa), attenzione al clipping.

    Ritorna un array numpy di float32 shape (n_samples,).
    """
    import numpy as np

    # Numero di campioni totali = durata * frequenza di campionamento
    n_samples = int(duration_sec * sample_rate)

    # Rumore bianco: distribuzione normale media 0, varianza 1
    noise = np.random.normal(loc=0.0, scale=1.0, size=n_samples).astype(np.float32)

    # Ridimensioniamo l'ampiezza per evitare clipping in riproduzione
    noise *= amplitude
    return noise


def play_audio(buffer, sample_rate: int = 48000):
    """
    Riproduce un array audio mono con 'sounddevice'.
    """
    import sounddevice as sd

    # Attenzione al volume di sistema: riproduciamo in blocking mode
    print("[INFO] Riproduzione audio in corso...")
    sd.play(buffer, samplerate=sample_rate, blocking=True)
    print("[OK] Riproduzione terminata.")


def save_wav(buffer, sample_rate: int = 48000, filename: str = "white_noise.wav"):
    """
    Salva l'audio in un file WAV usando scipy.io.wavfile.
    Il formato WAV standard atteso è int16, quindi convertiamo con scaling.
    """
    import numpy as np
    from scipy.io import wavfile

    # Conversione float32 [-1,1] ~> int16 [-32768,32767]
    # Nota: Se l'ampiezza è troppo alta, si verifica clipping.
    max_int16 = np.iinfo(np.int16).max
    wav_int16 = (buffer * max_int16).clip(-max_int16, max_int16).astype(np.int16)

    wavfile.write(filename, sample_rate, wav_int16)
    print(f"[OK] File WAV salvato: {filename}")


def plot_signal_and_spectrum(buffer, sample_rate: int = 48000):
    """
    Visualizza il segnale nel tempo e lo spettro di ampiezza con matplotlib.
    """
    import numpy as np
    import matplotlib.pyplot as plt

    # Tempo in secondi per asse x del segnale
    t = np.arange(buffer.shape[0]) / sample_rate

    # FFT per spettro (modulo)
    fft = np.fft.rfft(buffer)
    freqs = np.fft.rfftfreq(buffer.shape[0], d=1.0 / sample_rate)
    magnitude = np.abs(fft)

    # Plot in due sottografici
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title("Segnale nel tempo (rumore bianco)")
    plt.plot(t, buffer, color="tab:blue", linewidth=0.8)
    plt.xlabel("Tempo [s]")
    plt.ylabel("Ampiezza")

    plt.subplot(1, 2, 2)
    plt.title("Spettro di ampiezza")
    plt.semilogx(freqs, magnitude, color="tab:orange", linewidth=0.8)
    plt.xlabel("Frequenza [Hz] (scala log)")
    plt.ylabel("Ampiezza")
    plt.tight_layout()
    plt.show()


# -----------------------------
# Sezione: interfaccia testuale
# -----------------------------

def print_menu():
    """
    Stampa il menu delle operazioni disponibili.
    """
    print("\n=== Mini Terminale Rumore Bianco ===")
    print("1. Verifica/installa dipendenze")
    print("2. Genera rumore bianco")
    print("3. Riproduci rumore bianco")
    print("4. Salva rumore bianco in WAV")
    print("5. Visualizza segnale e spettro")
    print("6. Esci")
    print("====================================")


def main():
    """
    Punto di ingresso del mini terminale.
    Mantiene un buffer audio in memoria per evitare rigenerazioni continue.
    """
    # Buffer audio corrente (None finché non generato)
    current_buffer = None
    current_sr = 48000

    # Prima cosa: offriamo l'installazione dipendenze
    print("[INFO] Avvio mini terminale. Passo 1: dipendenze.")
    ensure_dependencies()

    while True:
        print_menu()
        choice = input("Seleziona un'opzione (1-6): ").strip()

        if choice == "1":
            # Utente vuole rieseguire la verifica (utile se si cambia ambiente)
            ensure_dependencies()

        elif choice == "2":
            # Parametri personalizzabili dall'utente
            try:
                dur = float(input("Durata in secondi (es. 2.0): ").strip() or "2.0")
                sr = int(input("Sample rate in Hz (es. 48000): ").strip() or "48000")
                amp = float(input("Ampiezza (0.0-1.0, es. 0.2): ").strip() or "0.2")
            except ValueError:
                print("[ERRORE] Parametri non validi. Riprova.")
                continue

            current_buffer = generate_white_noise(duration_sec=dur, sample_rate=sr, amplitude=amp)
            current_sr = sr
            print(f"[OK] Rumore bianco generato: {len(current_buffer)} campioni @ {current_sr} Hz.")

        elif choice == "3":
            if current_buffer is None:
                print("[ATTENZIONE] Nessun buffer generato. Seleziona '2' per generarlo prima.")
                continue
            play_audio(current_buffer, sample_rate=current_sr)

        elif choice == "4":
            if current_buffer is None:
                print("[ATTENZIONE] Nessun buffer generato. Seleziona '2' per generarlo prima.")
                continue

            filename = input("Nome file WAV (es. white_noise.wav): ").strip() or "white_noise.wav"
            save_wav(current_buffer, sample_rate=current_sr, filename=filename)

        elif choice == "5":
            if current_buffer is None:
                print("[ATTENZIONE] Nessun buffer generato. Seleziona '2' per generarlo prima.")
                continue
            plot_signal_and_spectrum(current_buffer, sample_rate=current_sr)

        elif choice == "6":
            print("[INFO] Uscita dal mini terminale. A presto!")
            break

        else:
            print("[ERRORE] Scelta non valida. Inserisci un numero tra 1 e 6.")


if __name__ == "__main__":
    # Esegui solo se invocato direttamente: avvia il mini terminale.
    main()
