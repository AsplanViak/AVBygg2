# -*- coding: utf-8 -*-

from pyrevit import DB, revit
from pyrevit import forms
from pyrevit import script

__title__ = 'Hvem har...'
__doc__ = "Vis meg editeringslogg for valgte objekter."

outwindu = script.get_output()
# revitinstans = _HostApplication(__revit__)
dokument = revit.doc

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
    active_view = revit.activeview
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
