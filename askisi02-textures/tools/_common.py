"""Κοινές ρυθμίσεις για τα scripts παραγωγής υφών.

Κρατά δύο πράγματα που εξαρτώνται από το μηχάνημα:
  - πού γράφονται οι υφές (OUT)
  - ποια γραμματοσειρά χρησιμοποιείται (font)

Και τα δύο υπολογίζονται δυναμικά, ώστε τα scripts να τρέχουν σε
Windows, macOS και Linux χωρίς αλλαγή.
"""
import os
import sys

from PIL import ImageFont

# Ο κατάλογος assets βρίσκεται δίπλα στον tools/, μέσα στην ίδια άσκηση:
#   askisi02-textures/tools/_common.py  ->  askisi02-textures/assets/
_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(_HERE, os.pardir, "assets"))
os.makedirs(OUT, exist_ok=True)


# Υποψήφιες γραμματοσειρές ανά λειτουργικό, κατά σειρά προτίμησης.
# Όλες έχουν ελληνικούς χαρακτήρες — χρειάζονται για τις πινακίδες και τις αφίσες.
_CANDIDATES = {
    "darwin": {
        False: ["/System/Library/Fonts/Supplemental/Arial.ttf",
                "/System/Library/Fonts/Supplemental/Verdana.ttf",
                "/Library/Fonts/Arial Unicode.ttf"],
        True:  ["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/System/Library/Fonts/Supplemental/Verdana Bold.ttf",
                "/Library/Fonts/Arial Unicode.ttf"],
    },
    "win32": {
        False: [r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf"],
        True:  [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\segoeuib.ttf"],
    },
    "linux": {
        False: ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
        True:  ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    },
}


def _platform_key():
    if sys.platform.startswith("win"):
        return "win32"
    if sys.platform == "darwin":
        return "darwin"
    return "linux"


def _find(bold):
    """Πρώτη γραμματοσειρά που υπάρχει όντως στο σύστημα."""
    key = _platform_key()
    # Δοκιμάζει πρώτα το τρέχον λειτουργικό και μετά όλα τα υπόλοιπα,
    # για την περίπτωση μη τυπικής εγκατάστασης.
    order = [key] + [k for k in _CANDIDATES if k != key]
    for k in order:
        for path in _CANDIDATES[k][bold]:
            if os.path.exists(path):
                return path
    return None


_CACHE = {}


def font(size, bold=False):
    """Γραμματοσειρά στο ζητούμενο μέγεθος, ανεξάρτητα από λειτουργικό."""
    path = _CACHE.get(bold)
    if path is None:
        path = _find(bold)
        if path is None:
            raise SystemExit(
                "Δεν βρέθηκε κατάλληλη γραμματοσειρά TrueType στο σύστημα.\n"
                "Δώσε μια διαδρομή .ttf στο _CANDIDATES του tools/_common.py."
            )
        _CACHE[bold] = path
    return ImageFont.truetype(path, size)
