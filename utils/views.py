# -*- coding: UTF-8 -*- #
from datetime import date, datetime
import os
from subprocess import Popen
from django.views.generic import TemplateView, RedirectView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.utils.encoding import force_unicode
from django.contrib.sessions.models import Session
from FUTFactory.fut.models import FUT, Domain, Phase, Step
from FUTFactory.lib.xlwt import *
from FUTFactory.settings import PHASE_COLORS, BASE_DIR
from FUTFactory.fut.filters import FUTFilterSet

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context.update({
            'futs_list': FUT.objects.filter(state__phase__name='En cours')[:10]
        })
        return context

class ReportView(TemplateView):
    def post(self, request):
        futs_ids = self.request.POST.getlist('futs')
        futs_list = []
        for fut_id in futs_ids:
            futs_list.append(FUT.objects.get(id=fut_id))
        self.request.session['futs_for_report'] = futs_list
        return HttpResponseRedirect('/report/choice/')
    
    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        f = FUTFilterSet(self.request.GET, queryset=FUT.objects.all())
        context.update({
            'filter': f
        })
        if 'futs_for_report' in self.request.session:
            context.update({
                'futs_for_report': self.request.session['futs_for_report']
            })   
        return context

class ReportChoiceView(TemplateView):
    def post(self, request):
        futs_ids = self.request.POST['futs']
        futs_list = []
        for fut_id in futs_ids:
            futs_list.append(FUT.objects.get(id=fut_id))
        self.request.session['futs_for_report'] = futs_list
        return HttpResponseRedirect('/report/choice/')
    
    def get(self, request, *args, **kwargs):
        if not 'futs_for_report' in self.request.session:
            messages.warning(self.request, u'Vous devez d\'abord sélectionner des FUTs à inclure dans la synthèse')
            return HttpResponseRedirect('/report/')
        else:
            return TemplateView.get(self, request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(ReportChoiceView, self).get_context_data(**kwargs)           
        context.update({
            'nb_futs': len(self.request.session['futs_for_report']),
            'futs_list': self.request.session['futs_for_report']
        })
        return context

class ReportGenerationView(TemplateView):
    def render_report_table_as_html(self, request):
        ids = []
        for f in request.session['futs_for_report']:
            ids.append(f.id) 
        report_table = '<table id="report_table" cellspacing="0" border="1">'
        report_table += '<tr>' + '<th class="report_title" colspan="4" rowspan="2">Synthèse Activités FUT Factory</th>' + '<th class="report_header" colspan="' + str(Domain.objects.all().count() * 3) + '" >Domaines</th>' + '</tr>'
        report_table += '<tr>'
        for domain in Domain.objects.all():
            report_table += '<th class="report_header orange" colspan="3">' + str(domain.name) + '</th>'
        report_table += '</tr>'
        report_table += '<tr><th class="report_header orange" colspan="2">Phase</th><th class="report_header orange" colspan="2">Etape</th>'
        for domain in Domain.objects.all():
            report_table += '<th class="report_header">Nb</th><th class="report_header">FUTs</th><th class="report_header">RM</th>'
        report_table += '</tr>'
        print_total = 1
        for phase in Phase.objects.order_by('rank', 'processing'):
            if not phase.processing and print_total == 1:
                report_table += '<tr>' + '<th class="report_title" colspan="3">TOTAL des FUTs pris en charge/traités</th><th>' + str(len(ids)) + '</th>'
                for domain in Domain.objects.all():
                    report_table += '<th colspan="3">' + str(FUT.objects.filter(id__in=ids, domain=domain).count()) + '</th>'
                report_table += '</tr>'
                print_total = 0   
            report_table += '<tr>'
            report_table += '<td class="bold" rowspan="' + str(Step.objects.filter(phase=phase).count()) + '" style="background-color: '
            for p in PHASE_COLORS:
                if phase.name == p[0]:
                    report_table += p[2]
            report_table += ';">' + str(phase) + '</td><td class="orange bold" rowspan="' + str(Step.objects.filter(phase=phase).count()) + '">' + str(FUT.objects.filter(id__in=ids, state__phase=phase).count()) + '</td>'
            step_count = 0
            for step in Step.objects.filter(phase=phase):
                step_count += 1
                if step_count > 1:
                    report_table += '<tr>'
                report_table += '<td class="step_name">' + str(step) + '</td><td class="bold">' + str(FUT.objects.filter(id__in=ids, state=step).count()) + '</td>'
                for domain in Domain.objects.all():
                    domain_str = ''
                    rm_str = ''
                    domain_count_max = FUT.objects.filter(id__in=ids, state=step, domain=domain).count()
                    domain_count = 0
                    for fut in FUT.objects.filter(id__in=ids, state=step, domain=domain):
                        domain_count += 1
                        domain_str += str(fut.name)
                        if fut.release_manager:
                            rm_str += str(fut.release_manager)
                        else:
                            rm_str += '-'
                        if domain_count < domain_count_max:
                            domain_str += '\n'
                            rm_str += '\n'
                    report_table += '<td class="bold orange">' + str(domain_count_max) + '</td><td>' + domain_str + '</td><td>' + rm_str + '</td>'
                report_table += '</tr>'
        report_table += '</table>'
        return force_unicode(report_table)

    def get_context_data(self, **kwargs):
        context = super(ReportGenerationView, self).get_context_data(**kwargs)
        if not 'futs_for_report' in self.request.session:
            messages.warning(self.request, u'Vous devez d\'abord sélectionner des FUTs à inclure dans la synthèse')
            return HttpResponseRedirect('/report/')
        else:
            context.update({
                'report_table': self.render_report_table_as_html(self.request)
            })
            return context

class ReportDownloadView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(ReportDownloadView, self).get_context_data(**kwargs)
        context.update({
            'download_file': self.request.session['download_file']
        })
        return context

def flush_selection_view(request):
        del request.session['futs_for_report']
        messages.info(request, u'La sélection a été vidée !')
        return HttpResponseRedirect('/report/')
    
def report_to_excel(request):
    d = date.today()
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename="Synthèse_' + str(d) + '.xls"'
    ezxf = easyxf
    wb = Workbook(encoding='utf-8')
    ws = wb.add_sheet(u'Synthèse')
    for i in range(0, 14):
        ws.write(0, i, '')
    ws.write_merge(r1=1, c1=0, r2=2, c2=3, label=u'Synthèse Activités FUT Factory 2011', style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
    a, b = 2, 4
    domains = []
    for domain in Domain.objects.all():
        ws.write_merge(r1=a, c1=b, r2=a, c2=b+1, label=domain.name, style=ezxf('font: bold on, colour_index orange; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
        domains.append([domain,b])
        b += 2
    ws.write_merge(r1=1, c1=4, r2=1, c2=b-1, label=u'Domaines', style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium; pattern: pattern solid, fore_colour gray25'))
    ws.col(0).width = 2500
    ws.col(1).width = 1500
    ws.col(2).width = 6000
    for h in range(0, 4):
        ws.row(h).height = 255 * 2
    cursor = (3, 0)
    last_row = 3
    count_processing = 0
    print_total = 1
    for phase in Phase.objects.order_by('rank', 'processing'):
        if not phase.processing and print_total == 1:
            ws.write_merge(r1=cursor[0], c1=cursor[1], r2=cursor[0], c2=cursor[1] + 2, label=u'TOTAL des FUTs pris en charge/traités', style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
            ws.write(cursor[0], cursor[1] + 3, count_processing, style=ezxf('font: bold on, colour_index orange; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
            j = 4
            while j < b:
                ws.col(j).width = 1500
                ws.col(j+1).width = 6000
                for dom in domains:
                    if j == dom[1]:
                        sum_count = 0
                        for i in range(2, len(dom)):
                            sum_count += dom[i] 
                        ws.write_merge(r1=cursor[0], c1=j, r2=cursor[0], c2=j + 1, label=sum_count, style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left medium, right medium'))
                j += 2
            ws.row(cursor[0]).height = 255 * 3
            cursor = (cursor[0] + 1, cursor[1])
            last_row = cursor[0]
            print_total = 0
        count_phase = 0
        for step in Step.objects.filter(phase=phase).order_by('id'):
            count_step = 0
            border_top = 'thin'
            border_bottom = 'thin'
            if step == Step.objects.filter(phase=phase).order_by('id')[0]:
                border_top = 'medium'
            if step == Step.objects.filter(phase=phase).order_by('id').reverse()[0]:
                border_bottom = 'medium'
            ws.write(cursor[0], cursor[1]+2, step.name, style=ezxf('align: wrap on, vert center, horiz left; borders: top ' + border_top + ', bottom ' + border_bottom + ', left thin, right thin'))
            highest_count_dom = 0
            for dom in domains:
                count_dom = 0
                str_dom = ''
                max_str = FUT.objects.filter(state=step, domain=dom[0]).count() 
                for fut in FUT.objects.filter(state=step, domain=dom[0]):
                    count_dom += 1
                    str_dom += '* ' + fut.name
                    if fut.release_manager:
                        str_dom += ' : ' + fut.release_manager.__unicode__()
                    if count_dom < max_str:
                        str_dom += '\n'
                ws.write(cursor[0], dom[1], count_dom, style=ezxf('font: bold on, colour_index orange;align: wrap on, vert center, horiz center; borders: top ' + border_top + ', bottom ' + border_bottom + ', left medium, right thin'))
                ws.write(cursor[0], dom[1] + 1, str_dom, style=ezxf('align: wrap on, vert center, horiz left; borders: top ' + border_top + ', bottom ' + border_bottom + ', left thin, right medium'))
                count_step += count_dom
                dom.append(count_dom)
                if highest_count_dom < count_dom:
                    highest_count_dom = count_dom
            ws.write(cursor[0], cursor[1]+3, count_step, style=ezxf('font: bold on; align: wrap on, vert center, horiz center; borders: top ' + border_top + ', bottom ' + border_bottom + ', left thin, right medium'))
            count_phase += count_step
            ws.row(cursor[0]).height = 255 * 2
            if highest_count_dom > 0 and highest_count_dom > 2:
                ws.row(cursor[0]).height = 255 * highest_count_dom
            if phase.name == 'A venir' and highest_count_dom < 4:
                ws.row(cursor[0]).height = 255 * 4 
            cursor = (cursor[0] + 1, cursor[1])            
        ws.write_merge(r1=last_row, c1=cursor[1] + 1, r2=cursor[0] - 1, c2=cursor[1] + 1, label=count_phase, style=ezxf('font: bold on, colour_index orange; align: wrap on, vert center, horiz center; borders: top medium, bottom medium, left thin, right thin'))
        pattern = ''
        for p in PHASE_COLORS:
            if phase.name == p[0]:
                pattern = '; pattern: pattern solid, fore_colour ' + p[1]
        ws.write_merge(r1=last_row, c1=cursor[1], r2=cursor[0] - 1, c2=cursor[1], label=phase.name.upper(), style=ezxf('font: bold on, colour_index black; align: wrap on, vert center, horiz center, rota 90; borders: top medium, bottom medium, left medium, right thin' + pattern))
        last_row = cursor[0]
        count_processing += count_phase
    wb.save(response)
    return response

def rasterize_info(request):
    id_session = request.GET.get('id')
    session = Session.objects.get(session_key=id_session)
    request.session['futs_for_report'] = session.get_decoded()['futs_for_report']
    print request.session['futs_for_report']
    return HttpResponseRedirect('/report/export/')

def rasterize(request):
    d = datetime.now().strftime('%d-%m-%y_%HH%M')
    rasterize_file = os.path.join(BASE_DIR, 'lib/phantomjs/rasterize.js')
    phantomjs_file = os.path.join(BASE_DIR, 'lib/phantomjs/phantomjs')
    Popen(['mkdir', '-p', os.path.join(BASE_DIR, 'public/img/generated/' + str(request.user.id))])
    output = os.path.join(BASE_DIR, 'public/img/generated/' + str(request.user.id) + '/synthese_' + str(d) + '.png')
    url = 'http://' + request.META['SERVER_NAME'] + ':' + request.META['SERVER_PORT'] + "/report/rasterize/?id=" + request.COOKIES['sessionid']
    Popen(['touch', output])
    Popen([phantomjs_file, '--load-images=yes', rasterize_file, url, output])
    request.session['download_file'] = 'img/generated/' + str(request.user.id) + '/synthese_' + str(d) + '.png'
    Popen(['chmod', '777', output])
    return HttpResponseRedirect('/report/download/')
    
