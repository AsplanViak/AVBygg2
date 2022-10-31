# -*- coding: utf-8 -*-

from pyrevit import DB, revit
from pyrevit import forms
from pyrevit import script

__title__ = 'Hvem har...(test)'
__doc__ = "Vis meg editeringslogg for valgte objekter."

outwindu = script.get_output()
# revitinstans = _HostApplication(__revit__)
dokument = revit.doc

# Kan sløyfes
__cleanengine__ = True  # Dette forteller tolkeren at den skal sette opp en ny ironpython motor for denne knappen, slik at den ikke kommer i konflikt med andre funksjoner, settes nesten alltid til FALSE, TRUE når du jobber med knappen.
__fullframeengine__ = False  # Denne er nødvendig for å få tilgang til noen moduler, denne gjør knappen vesentrlig tregere i oppstart hvis den står som TRUE
__context__ = "zerodoc"  # Denne forteller tolkeren at knappen skal kunne brukes selv om et Revit dokument ikke er åpent.
__helpurl__ = "google.no"  # Hjelp URL når bruker trykker F1 over knapp.
__min_revit_ver__ = 2010  # knapp deaktivert hvis klient bruker lavere versjon
__max_revit_ver__ = 2032  # Skjønner?
__beta__ = False  # Knapp deaktivert hos brukere som ikke har spesifikt aktivert betaknapper
