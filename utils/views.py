# -*- coding: UTF-8 -*- #
from datetime import date
from django.views.generic import TemplateView
from django.http import HttpResponse
from FUTFactory.fut.models import FUT, Domain, Phase, Step
from FUTFactory.lib.xlwt import *

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'futs_list': FUT.objects.filter(state__phase__name='En cours')[:10]
        })
        return context

def tool_excel_export(request):
    d = date.today()
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="Synthèse_' + str(d) + '.xls"'
    
    ezxf = easyxf
    
    wb = Workbook(encoding='utf-8')
    
    ws = wb.add_sheet(u'Synthèse')
    for i in range(0, 14):
        ws.write(0, i, '')
    ws.write_merge(r1=1, c1=0, r2=2, c2=3, label=u'Synthèse Activités FUTFactory 2011', style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
    a, b = 2, 4
    domains = []
    for domain in Domain.objects.all():
        ws.write_merge(r1=a, c1=b, r2=a, c2=b+1, label=domain.name, style=ezxf('font: bold on, colour_index orange; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
        domains.append((domain,b))
        b += 2
    ws.write_merge(r1=1, c1=4, r2=1, c2=b-1, label=u'Domaines', style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium; pattern: pattern solid, fore_colour gray25'))
    ws.col(0).width = 2500
    ws.col(1).width = 1500
    ws.col(2).width = 5000
    j = 4
    while j < b:
        ws.col(j).width = 1500
        ws.col(j+1).width = 5900
        j += 2
    for h in range(0, 4):
        ws.row(h).height = 255 * 2
    cursor = (3, 0)
    last_row = 3
    for phase in Phase.objects.all():
        count_phase = 0            
        for step in Step.objects.filter(phase=phase):
            count_step = 0
            ws.write(cursor[0], cursor[1]+2, step.name, style=ezxf('align: wrap on, vert center, horiz center; borders: top thin, bottom thin, left thin, right thin'))
            highest_count_dom = 0
            for dom in domains:
                count_dom = 0
                str_dom = ''
                max_str = FUT.objects.filter(state=step, domain=dom[0]).count() 
                for fut in FUT.objects.filter(state=step, domain=dom[0]):
                    count_dom += 1
                    str_dom += fut.name
                    if count_dom < max_str:
                        str_dom += '\n'
                ws.write(cursor[0], dom[1], count_dom, style=ezxf('align: wrap on, vert center, horiz center; borders: top thin, bottom thin, left thin, right thin'))
                ws.write(cursor[0], dom[1] + 1, str_dom, style=ezxf('align: wrap on, vert center, horiz center; borders: top thin, bottom thin, left thin, right thin'))
                count_step += count_dom
                if highest_count_dom < count_dom:
                    highest_count_dom = count_dom
            ws.write(cursor[0], cursor[1]+3, count_step, style=ezxf('align: wrap on, vert center, horiz center; borders: top thin, bottom thin, left thin, right thin'))
            count_phase += count_step
            ws.row(cursor[0]).height = 255 * 2
            if highest_count_dom > 0 and highest_count_dom > 2:
                ws.row(cursor[0]).height = 255 * highest_count_dom
            cursor = (cursor[0] + 1, cursor[1])            
        ws.write_merge(r1=last_row, c1=cursor[1] + 1, r2=cursor[0] - 1, c2=cursor[1] + 1, label=count_phase, style=ezxf('align: wrap on, vert center, horiz center; borders: top thin, bottom thin, left thin, right thin'))
        ws.write_merge(r1=last_row, c1=cursor[1], r2=cursor[0] - 1, c2=cursor[1], label=phase.name.upper(), style=ezxf('font: bold on, colour_index orange; align: wrap on, vert center, horiz center, rota 90; borders: top medium, bottom medium, left medium, right medium'))
        last_row = cursor[0]
    
    ws2 = wb.add_sheet(u'Planning')
    ws2.write_merge(r1=0, c1=0, r2=3, c2=9, label="A FAIRE", style=ezxf('font: bold on; align: wrap on, vert centre, horiz center'))

    wb.save(response)
    return response