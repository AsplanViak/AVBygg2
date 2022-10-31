# -*- coding: utf-8 -*-

from pyrevit import DB, revit
from pyrevit import forms
from pyrevit import script

# Start MÅ ha
__title__ = 'testHvemhar'  # Denne overstyrer navnet på scriptfilen
__author__ = 'Asplan Viak'  # Dette kommer opp som navnet på utvikler av knappen
__doc__ = "Alt-klikk denne knappen og utforsk kildekoden for å lage egne knapper."  # Dette blir hjelp teksten som kommer opp når man holder musepekeren over knappen.
# End MÅ ha

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

def who_created_selection():
    selection = revit.get_selection()
    if revit.doc.IsWorkshared:
        if selection and len(selection) == 1:
            wti = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, selection.first.Id)
            forms.alert('Creator: {0}\n'
                        'Current Owner: {1}\n'
                        'Last Changed By: {2}'.format(wti.Creator, wti.Owner, wti.LastChangedBy))
        else:
            forms.alert('Exactly one element must be selected.')
    else:
        forms.alert('Model is not workshared.')


def who_created_activeview():
    active_view = revit.active_view
    view_id = active_view.Id.ToString()
    view_name = active_view.Name
    view_creator = \
        DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, active_view.Id).Creator
    forms.alert('{}\n{}\n{}'
                .format("Creator of the current view: " + view_name,
                        "with the id: " + view_id,
                        "is: " + view_creator))


def _print_Element_Historikk(element):
    if revit.doc.IsWorkshared:
        if element:
            WorkShInfo = DB.WorksharingUtils.GetWorksharingTooltipInfo(revit.doc, element.Id)
            WorkShInfo
            # ElementInfo
            print "Objektinfo:\n"
            # Worksharing info
            print "Editeringsinfo:\n"
            print unicode('Først opprettet av: {0}\n' + 'Sjekket ut av: {1}\n' + 'Sist endret av: {2}\n').format(WorkShInfo.Creator, WorkShInfo.Owner, WorkShInfo.LastChangedBy)
            outwindu.next_page()
            print "Disse personene ønsker at du gir de tillatelse til å redigere dette objektet:\n"
            requestliste = WorkShInfo.GetRequesters()
            if len(requestliste) > 0:
                for person in requestliste:
                    print person
            else:
                print "Ingen editeringsforsøk på objekt akkurat nå!"
            print "\n"
        else:
            forms.alert('Ingen objekter valgt...')
    else:
        forms.alert('Model er ikke en "Workshared" modell, altså ikke en modell med "Worksets".')


# options = {'Who Created Active View?': who_created_activeview, 'Who Created Selected Element?': who_created_selection, 'Who Reloaded Keynotes Last?': who_reloaded_keynotes}


generellInfo = "Du kan velge objekter og zoome inn på et objekt ved å klikke på elementId'en"
valgteObjekter = revit.get_selection()
antallSider = len(list(valgteObjekter))
outwindu.add_style('body { color: black; }')
outwindu.set_title(generellInfo)
print "Antall objekter valgt: " + str(antallSider), "\n"
outwindu.next_page()
for elem in valgteObjekter:
    _print_Element_Historikk(elem)
    outwindu.insert_divider()
    outwindu.next_page()
outwindu.next_page()

if len(list(valgteObjekter)) < 1:
    outwindu.add_style('body { color: red; }')
    print "Du må velge noen objekter i brukergrensesnittet til Revit først!"
else:
    print "Antall objekter valgt: " + str(antallSider)
    print generellInfo
