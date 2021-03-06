from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Contato
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

def index(request):

    contatos = Contato.objects.all()
    paginator = Paginator(contatos, 2)

    page = request.GET.get('p') #paginação
    contatos = paginator.get_page(page)

    return render(request, 'contatos/index.html', {
        'contatos': contatos
    }) #retorna os contatos na tela

def ver_contato(request, contato_id):
    #contato = Contato.objects.get(id=contato_id)
    contato = get_object_or_404(Contato, id=contato_id)

    if not contato.mostrar:
        raise Http404

    return render(request, 'contatos/ver_contato.html', {
        'contato': contato
    })

def busca(request):
    termo = request.GET.get('termo')

    if termo is None or not termo:
        messages.add_message(
            request, 
            messages.ERROR,
            'Campo termo não pode ficar vazio'
        )
        return redirect('index')
    contatos = Contato.objects.order_by('-id').filter(
        Q(nome__icontains = termo) | Q(sobrenome__icontains = termo),
        mostrar = True
    )
    paginator = Paginator(contatos, 2)

    page = request.GET.get('p') #paginação
    contatos = paginator.get_page(page)

    return render(request, 'contatos/busca.html', {
        'contatos': contatos
    })
