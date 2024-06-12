from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from django.db.models import Sum

from babel.dates import format_date
from django.utils.dateparse import parse_date
from datetime import datetime
import json
import calendar
from reportlab.pdfgen import canvas

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, PageTemplate, BaseDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from django.db.models.functions import TruncMonth

from cmp.models import Factura, PagoParcial
from caja.models import Venta, VentaDetalle
from bases.views import SinAutorizacion



class EgresosIngresosAnualesView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reportes/egresos_ingresos_anuales.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_year = int(self.request.GET.get('year')) if self.request.GET.get('year') else None

        # Obtener el año actual
        current_year = datetime.now().year

        # Generar una lista de años disponibles para mostrar en el formulario
        years = list(range(current_year - 10, current_year + 1))

        # Pasar los años y el año seleccionado al contexto
        context['years'] = years
        context['selected_year'] = selected_year

        if selected_year:

            # Filtrar ventas y facturas por el año seleccionado
            ventas = Venta.objects.filter(fecha_venta__year=selected_year)
            facturas = Factura.objects.filter(fecha_emision__year=selected_year)

            # Agrupar y sumar las ventas por mes
            ventas_mensuales = ventas.annotate(month=TruncMonth('fecha_venta')).values('month').annotate(total_ventas=Sum('total_venta')).order_by('month')

            # Agrupar y sumar los egresos (total_pagar de las facturas) por mes
            egresos_mensuales = facturas.annotate(month=TruncMonth('fecha_emision')).values('month').annotate(total_egresos=Sum('total_pagar')).order_by('month')

            # Crear diccionarios para acceder rápidamente a los montos por mes
            ventas_dict = {venta['month'].month: venta['total_ventas'] for venta in ventas_mensuales}
            egresos_dict = {egreso['month'].month: egreso['total_egresos'] for egreso in egresos_mensuales}

            # Obtener los nombres de los meses en español
            meses_espanol = [calendar.month_abbr[month] for month in range(1, 13)]

            # Preparar los datos para los gráficos
            data_ingresos = []
            data_egresos = []
            for month in range(1, 13):
                data_ingresos.append(float(ventas_dict.get(month, 0)))
                data_egresos.append(float(egresos_dict.get(month, 0)))

            # Preparar los datos para el contexto
            chart_data = {
                'labels': meses_espanol,
                'data_ingresos': data_ingresos,
                'data_egresos': data_egresos,
            }

            # Convertir los datos a JSON y pasarlos al contexto
            context['chart_data'] = json.dumps(chart_data)

        return context

class EgresosView(LoginRequiredMixin, generic.TemplateView):
    template_name = "reportes/egresos_mensuales.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Obtener el mes y año del parámetro GET
        month_year = self.request.GET.get('month')
        
        if month_year:
            try:
                # Convertir la cadena 'YYYY-MM' a una fecha
                date = parse_date(month_year + "-01")
                
                
                if date:
                    month = date.month
                    year = date.year

                    # Filtrar egresos por mes y año
                    egresos = Factura.objects.filter(fecha_emision__year=year, fecha_emision__month=month)

                    context['selected_month'] = format_date(date, 'MMMM', locale='es')
                    context['selected_year'] = year
                    
                    context['egresos'] = egresos
                    proveedores = [egreso.proveedor.__str__() for egreso in egresos]
                    totales = [egreso.total_pagar for egreso in egresos]
                    
                    context['chart_data'] = {
                        'labels': json.dumps(proveedores),
                        'data': json.dumps(totales)
                    }
                    
                else:
                    context['egresos'] = Factura.objects.none()
                    context['error'] = 'Fecha inválida proporcionada.'
            except Exception as e:
                context['egresos'] = Factura.objects.none()
                context['error'] = str(e)
        else:
            context['egresos'] = Factura.objects.none()
            context['error'] = 'No se proporcionó el parámetro de mes.'
        
        return context

class IngresosView(LoginRequiredMixin, generic.TemplateView):
    template_name = "reportes/ingresos_mensuales.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        month_year = self.request.GET.get('month')
        
        if month_year:
            try:
                # Convertir la cadena 'YYYY-MM' a una fecha
                date = parse_date(month_year + "-01")
                
                if date:
                    month = date.month
                    year = date.year

                    # Filtrar ingresos por mes y año
                    ingresos = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=month)
                    detalles_ventas = []

                    for venta in ingresos:
                        detalles = VentaDetalle.objects.filter(venta=venta)
                        for detalle in detalles:
                            producto = {
                                'producto': detalle.producto,
                                'precio_unitario': detalle.precio_unitario,
                                'cantidad': detalle.cantidad,
                                'subtotal': detalle.subtotal,
                            }
                            detalles_ventas.append(producto)

                    context['selected_month'] = format_date(date, 'MMMM', locale='es')
                    context['selected_year'] = year
                    context['ingresos'] = ingresos
                    context['detalles_ventas'] = detalles_ventas
                    
                    # Prepare data for the area chart
                    days_in_month = calendar.monthrange(year, month)[1]
                    daily_totals = [0] * days_in_month
                    for venta in ingresos:
                        day = venta.fecha_venta.day
                        daily_totals[day - 1] += float(venta.total_venta)
                    
                    context['chart_data'] = {
                        'labels': json.dumps(list(range(1, days_in_month + 1))),
                        'data': json.dumps(daily_totals)
                    }
                    
                    # Prepare data for the bar chart (top 10 sold products)
                    top_products = VentaDetalle.objects.filter(venta__fecha_venta__year=year, venta__fecha_venta__month=month)\
                        .values('producto')\
                        .annotate(total_vendido=Sum('cantidad'))\
                        .order_by('-total_vendido')
                        
                    
                    bar_labels = [item['producto'] for item in top_products]
                    bar_data = [item['total_vendido'] for item in top_products]

                    context['bar_chart_data'] = {
                        'labels': json.dumps(bar_labels),
                        'data': json.dumps(bar_data)
                    }
                else:
                    context['ingresos'] = Venta.objects.none()
                    context['error'] = 'Fecha inválida proporcionada.'
            except Exception as e:
                context['ingresos'] = Venta.objects.none()
                context['error'] = str(e)
        else:
            context['ingresos'] = Venta.objects.none()
            context['error'] = 'No se proporcionó el parámetro de mes.'
        
        return context

class IngresoDiarioView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'reportes/ingreso_diario.html'
    
    def get_context_data(self, **kwars):
        context = super().get_context_data(**kwars)
        date = self.request.GET.get('date') 
        
        if date:
            try:
                parsed_date = parse_date(date)
                if parsed_date:
                    year = parsed_date.year
                    month = parsed_date.month
                    day = parsed_date.day
                    
                    ingresos = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=month, fecha_venta__day=day)
                    
                    detalles_ventas = {}
                    for venta in ingresos:
                        detalles_ventas[venta.id] = VentaDetalle.objects.filter(venta=venta)
                    
                    context['date'] = date
                    context['fecha'] = parsed_date
                    context['ingresos'] = ingresos
                    context['detalles_ventas'] = detalles_ventas
                else:
                    context['ingresos'] = Venta.objects.none()
                    context['detalles_ventas'] = {}
                    context['error'] = 'Fecha inválida proporcionada.'
            except Exception as e:
                context['ingresos'] = Venta.objects.none()
                context['detalles_ventas'] = {}
                context['error'] = str(e)
        else:
            context['ingresos'] = Venta.objects.none()
            context['detalles_ventas'] = {}
            context['error'] = 'No se proporcionó el parámetro de la fecha.'
        return context

# PDF functions

def generar_pdf_egresos_ingresos_mensuales(request):
    # Obtener los datos para el libro mayor
    month = request.GET.get('month')
    year = int(month.split('-')[0])
    month = int(month.split('-')[1])
    
    ingresos = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=month)
    egresos = Factura.objects.filter(fecha_emision__year=year, fecha_emision__month=month)

    # Calcular las sumas
    total_debe = sum(float(ingreso.total_venta) for ingreso in ingresos)
    total_haber = sum(float(egreso.total_pagar) for egreso in egresos)
    
    # Crear la tabla con los datos y añadir la fila de sumas
    data = [['#', 'Detalle', 'Debe', 'Haber']] + \
            [[i+1, f'Venta N°: {ingreso.id} - Fecha: {ingreso.fecha_venta.strftime("%d/%m/%Y")}', ingreso.total_venta, ''] for i, ingreso in enumerate(ingresos)] + \
            [[i+1, f'Factura N°: {egreso.id} - Fecha: {egreso.fecha_emision.strftime("%d/%m/%Y")} - Proveedor: {egreso.proveedor}', '', egreso.total_pagar] for i, egreso in enumerate(egresos)] + \
            [['', 'Total', f'{total_debe:.2f}', f'{total_haber:.2f}']]

    # Fecha de impresión
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Definir nombres de meses en español
    meses_espanol = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
    }

    # Obtener el nombre del mes abreviado en español
    abrev_mes = meses_espanol[month]

    # Crear un objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    file_name = f'Reporte_Ventas_Gastos_{abrev_mes}/{year}.pdf'
    response['Content-Disposition'] = "attachment; filename="+file_name

    # Crear el PDF a partir del HTML renderizado
    doc = BaseDocTemplate(response, pagesize=letter)
    
    # Estilo del párrafo
    styles = getSampleStyleSheet()
    style_left = styles["Normal"]
    style_left.alignment = TA_CENTER
    
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Encabezado
    encabezado = Paragraph(f'<font size="18"><b>Reporte Ventas y Gastos {abrev_mes}/{year}</b></font><br/><br/>', style_left)

    # Pie de página
    def pie_pagina(canvas, doc):
        numero_pagina = canvas.getPageNumber()
        texto = f"Página {numero_pagina} - Fecha: {fecha_impresion}"
        canvas.drawRightString(7.25 * inch, 0.75 * inch, texto) 

    # Tabla
    table = Table(data)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (1, 1), (1, -2), colors.lightgreen), # Color para columna "Debe"
        ('BACKGROUND', (2, 1), (2, -2), colors.lightyellow), # Color para columna "Haber"
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), # Color para la fila de totales
    ])

    table.setStyle(style)

    # Añadir el encabezado y pie de página a todas las páginas
    doc.addPageTemplates([PageTemplate(id='encabezado', 
                                        frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), 
                                        onPage=pie_pagina), 
                                        PageTemplate(id='tabla', frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), onPage=pie_pagina)])

    # Añadir la tabla al documento PDF
    doc.build([encabezado, table])

    return response

def generar_pdf_egresos_mensual(request):
    month = request.GET.get('month')
    year = int(month.split('-')[0])
    month = int(month.split('-')[1])
    
    egresos = Factura.objects.filter(fecha_emision__year=year, fecha_emision__month=month)
    total_haber = sum(float(egreso.total_pagar) for egreso in egresos)
    
    
    # Crear la tabla con los datos y añadir la fila de sumas
    data = [['#', 'Detalle', 'Monto']] + \
            [[i+1, f'Factura N°: {egreso.id} - Fecha: {egreso.fecha_emision.strftime("%d/%m/%Y")} - Proveedor: {egreso.proveedor}', egreso.total_pagar] for i, egreso in enumerate(egresos)] + \
            [['','Total: ',f'{total_haber:.2f}']]
    # Fecha de impresión
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Definir nombres de meses en español
    meses_espanol = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
    }

    # Obtener el nombre del mes abreviado en español
    abrev_mes = meses_espanol[month]

    # Crear un objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    file_name = f'Reporte_Gastos_{abrev_mes}/{year}.pdf'
    response['Content-Disposition'] = "attachment; filename="+file_name

    # Crear el PDF a partir del HTML renderizado
    doc = BaseDocTemplate(response, pagesize=letter)
    
    # Estilo del párrafo
    styles = getSampleStyleSheet()
    style_left = styles["Normal"]
    style_left.alignment = TA_CENTER
    
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Encabezado
    encabezado = Paragraph(f'<font size="18"><b>Reporte Gastos {abrev_mes}/{year}</b></font><br/><br/>', style_left)

    # Pie de página
    def pie_pagina(canvas, doc):
        numero_pagina = canvas.getPageNumber()
        texto = f"Página {numero_pagina} - Fecha: {fecha_impresion}"
        canvas.drawRightString(7.25 * inch, 0.75 * inch, texto) 

    # Tabla
    table = Table(data)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (1, 1), (1, -2), colors.lightgreen), # Color para columna "Debe"
        ('BACKGROUND', (2, 1), (2, -2), colors.lightyellow), # Color para columna "Haber"
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), # Color para la fila de totales
    ])

    table.setStyle(style)

    # Añadir el encabezado y pie de página a todas las páginas
    doc.addPageTemplates([PageTemplate(id='encabezado', 
                                        frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), 
                                        onPage=pie_pagina), 
                                        PageTemplate(id='tabla', frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), onPage=pie_pagina)])

    # Añadir la tabla al documento PDF
    doc.build([encabezado, table])

    return response

def generar_pdf_venta_dia(request):
    date = request.GET.get('date')
    year = int(date.split('-')[0])
    month = int(date.split('-')[1])
    day = int(date.split('-')[2])
    
    ingresos = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=month, fecha_venta__day=day)
    
    detalles_ventas = {}
    for venta in ingresos:
        detalles_ventas[venta.id] = VentaDetalle.objects.filter(venta=venta)
    
    data = [['#', 'Producto', 'Cantidad', '$/Un.', 'Subtotal']]
    i = 1
    total_ventas = 0
    for venta_id, detalles in detalles_ventas.items():
        for detalle in detalles:
            data.append([i, detalle.producto, detalle.cantidad, detalle.precio_unitario, detalle.subtotal])
            total_ventas += detalle.subtotal
            i += 1
    
    # Añadir la fila de total
    data.append(['', '', '', 'Total', total_ventas])
    
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Definir nombres de meses en español
    meses_espanol = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
    }

    # Obtener el nombre del mes abreviado en español
    abrev_mes = meses_espanol[month]

    # Crear un objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    file_name = f'Reporte_Ventas_{day}/{abrev_mes}/{year}.pdf'
    response['Content-Disposition'] = "attachment; filename="+file_name

    # Crear el PDF a partir del HTML renderizado
    doc = BaseDocTemplate(response, pagesize=letter)
    
    # Estilo del párrafo
    styles = getSampleStyleSheet()
    style_left = styles["Normal"]
    style_left.alignment = TA_CENTER
    
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Encabezado
    encabezado = Paragraph(f'<font size="18"><b>Reporte Ventas {day}/{abrev_mes}/{year}</b></font><br/><br/>', style_left)

    # Pie de página
    def pie_pagina(canvas, doc):
        numero_pagina = canvas.getPageNumber()
        texto = f"Página {numero_pagina} - Fecha: {fecha_impresion}"
        canvas.drawRightString(7.25 * inch, 0.75 * inch, texto) 

    # Tabla
    table = Table(data)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (1, 1), (1, -2), colors.lightgreen), # Color para columna "Debe"
        ('BACKGROUND', (2, 1), (2, -2), colors.lightyellow), # Color para columna "Haber"
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), # Color para la fila de totales
    ])

    table.setStyle(style)

    # Añadir el encabezado y pie de página a todas las páginas
    doc.addPageTemplates([PageTemplate(id='encabezado', 
                                        frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), 
                                        onPage=pie_pagina), 
                                        PageTemplate(id='tabla', frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), onPage=pie_pagina)])

    # Añadir la tabla al documento PDF
    doc.build([encabezado, table])

    return response

def generar_pdf_ingresos_mensual(request):
    month = request.GET.get('month')
    year = int(month.split('-')[0])
    month = int(month.split('-')[1])
    
    ingresos = Venta.objects.filter(fecha_venta__year=year, fecha_venta__month=month)
    total_debe = sum(float(ingreso.total_venta) for ingreso in ingresos)
    
    
    # Crear la tabla con los datos y añadir la fila de sumas
    data = [['#', 'Detalle', 'Monto']] + \
            [[i+1, f'Venta N°: {ingreso.id} - Fecha: {ingreso.fecha_venta.strftime("%d/%m/%Y")}', ingreso.total_venta] for i, ingreso in enumerate(ingresos)] +\
            [['','Total: ',f'{total_debe:.2f}']]
    # Fecha de impresión
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Definir nombres de meses en español
    meses_espanol = {
        1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr",
        5: "May", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"
    }

    # Obtener el nombre del mes abreviado en español
    abrev_mes = meses_espanol[month]

    # Crear un objeto PDF con ReportLab
    response = HttpResponse(content_type='application/pdf')
    file_name = f'Reporte_Ventas_{abrev_mes}/{year}.pdf'
    response['Content-Disposition'] = "attachment; filename="+file_name

    # Crear el PDF a partir del HTML renderizado
    doc = BaseDocTemplate(response, pagesize=letter)
    
    # Estilo del párrafo
    styles = getSampleStyleSheet()
    style_left = styles["Normal"]
    style_left.alignment = TA_CENTER
    
    fecha_impresion = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Encabezado
    encabezado = Paragraph(f'<font size="18"><b>Reporte Ventas {abrev_mes}/{year}</b></font><br/><br/>', style_left)

    # Pie de página
    def pie_pagina(canvas, doc):
        numero_pagina = canvas.getPageNumber()
        texto = f"Página {numero_pagina} - Fecha: {fecha_impresion}"
        canvas.drawRightString(7.25 * inch, 0.75 * inch, texto) 

    # Tabla
    table = Table(data)

    # Estilo de la tabla
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (1, 1), (1, -2), colors.lightgreen), # Color para columna "Debe"
        ('BACKGROUND', (2, 1), (2, -2), colors.lightyellow), # Color para columna "Haber"
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey), # Color para la fila de totales
    ])

    table.setStyle(style)

    # Añadir el encabezado y pie de página a todas las páginas
    doc.addPageTemplates([PageTemplate(id='encabezado', 
                                        frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), 
                                        onPage=pie_pagina), 
                                        PageTemplate(id='tabla', frames=Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height), onPage=pie_pagina)])

    # Añadir la tabla al documento PDF
    doc.build([encabezado, table])

    return response

def generar_pdf_factura(request, factura_id):
    # Obtener la factura de la base de datos
    factura = Factura.objects.get(id=factura_id)
    pagos = PagoParcial.objects.filter(factura=factura_id) 

    # Calcular la suma total de los pagos parciales
    suma_pagos_parciales = pagos.aggregate(Sum('monto'))['monto__sum'] or 0

    # Crear el objeto HttpResponse con las cabeceras PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="factura_{factura.numero_factura}_{factura.proveedor}.pdf"'

    # Crear el PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Establecer estilos
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.darkblue)

    # Escribir los datos en el PDF
    p.drawString(100, height - 100, f"Factura N°: {factura.numero_factura}")
    
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, height - 120, f"Proveedor: {factura.proveedor}")
    p.drawString(100, height - 140, f"Fecha de emisión: {factura.fecha_emision.strftime('%d/%m/%Y')}")
    p.drawString(100, height - 160, f"Notas: {factura.notas or 'N/A'}")
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.red)
    p.drawString(100, height - 180, f"Total a pagar: {factura.total_pagar}")
    
    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    p.drawString(100, height - 200, f"Estado: {factura.estado_factura}")
    p.drawString(100, height - 220, f"Fecha de vencimiento: {factura.fecha_vencimiento.strftime('%d/%m/%Y')}")
    p.drawString(100, height - 240, f"Fecha de pago: {factura.fecha_pago.strftime('%d/%m/%Y') if factura.fecha_pago else '--------'}")

    # Agregar información de los pagos parciales
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.darkblue)
    p.drawString(100, height - 260, "Pagos Parciales:")

    p.setFont("Helvetica", 12)
    p.setFillColor(colors.black)
    y_position = height - 280
    for pago in pagos:
        p.drawString(100, y_position, f"Fecha: {pago.fecha_pago.strftime('%d/%m/%Y')}, Monto: {pago.monto}")
        y_position -= 20  # Espacio entre líneas

    # Agregar la suma total de los pagos parciales
    y_position -= 20  # Espacio adicional antes de la suma total
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.darkblue)
    p.drawString(100, y_position, f"Suma Total de Pagos Parciales: {suma_pagos_parciales}")

    # Finalizar el PDF
    p.showPage()
    p.save()

    return response

