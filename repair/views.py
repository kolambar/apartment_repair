from django.db.models import Prefetch

from .forms import FlatForm
from .models import Flat, Operation, OperationType, Worker


# Create your views here.


def flat_list(request):
    flats = Flat.objects.select_related('intOwnerId').all()

    return render(request, 'repair/flat_list.html', {'flats': flats})


def add_flat(request):
    if request.method == 'POST':
        form = FlatForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/flat_list')
    else:
        form = FlatForm()
    return render(request, 'repair/flat_form.html', {'form': form})


def flat_detail(request, pk):
    flat = get_object_or_404(Flat, pk=pk)
    operations = Operation.objects.filter(intFlatId=flat).select_related(
        'intOperationTypeId', 'intWorkerId'
    )
    return render(request, 'repair/flat_detail.html', {
        'flat': flat,
        'operations': operations
    })


from django.shortcuts import render, redirect, get_object_or_404
from .forms import OperationForm


def add_operation(request, flat_id):
    flat = get_object_or_404(Flat, pk=flat_id)

    if request.method == 'POST':
        form = OperationForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.intFlatId = flat
            operation.save()
            return redirect('repair:flat_detail', pk=flat.id)
    else:
        form = OperationForm()

    return render(request, 'repair/operation_form.html', {
        'form': form,
        'flat': flat
    })


def main_menu(request):
    operation_types = OperationType.objects.all()
    return render(request, 'repair/main_menu.html', {'operation_types': operation_types})


def report_workers(request):
    workers = Worker.objects.all().prefetch_related('operations__intFlatId', 'operations__intOperationTypeId')

    for worker in workers:
        worker.operations_summary = worker.operations.all()
        worker.operation_count = worker.operations.count()
        worker.total_cost = sum(op.intOperationTypeId.fltOperationPrice for op in worker.operations_summary)

    total_workers = workers.count()

    return render(request, 'repair/report_workers.html', {
        'workers': workers,
        'total_workers': total_workers
    })


def report_repairs(request):
    flats = Flat.objects.prefetch_related(
        Prefetch('operations', queryset=Operation.objects.select_related('intOperationTypeId', 'intWorkerId'))
    ).select_related('intOwnerId')

    # Добавим вычисление сумм для каждой квартиры
    for flat in flats:
        operation_groups = {}
        total_cost = 0
        for op in flat.operations.all():
            type_name = op.intOperationTypeId.txtOperationTypeName
            if type_name not in operation_groups:
                operation_groups[type_name] = {
                    'type_obj': op.intOperationTypeId,
                    'operations': [],
                    'count': 0
                }
            operation_groups[type_name]['operations'].append(op)
            operation_groups[type_name]['count'] += 1
            total_cost += op.intOperationTypeId.fltOperationPrice
        flat.operation_groups = operation_groups
        flat.total_cost = total_cost

    return render(request, 'repair/report_repairs.html', {'flats': flats})


def report_by_work_type(request):
    selected_type_id = request.GET.get('type_id')
    operation_type = None
    workers = []
    operations = []

    types = OperationType.objects.all()

    if selected_type_id:
        try:
            operation_type = OperationType.objects.get(pk=selected_type_id)
            operations = Operation.objects.filter(intOperationTypeId=operation_type).select_related(
                'intWorkerId', 'intFlatId'
            ).order_by('-datOperationDate')

            # Уникальные рабочие, участвовавшие в этих работах
            worker_ids = operations.values_list('intWorkerId_id', flat=True).distinct()
            workers = Worker.objects.filter(id__in=worker_ids)

        except OperationType.DoesNotExist:
            operation_type = None

    return render(request, 'repair/report_by_work_type.html', {
        'types': types,
        'selected_type_id': int(selected_type_id) if selected_type_id else None,
        'operation_type': operation_type,
        'workers': workers,
        'operations': operations
    })
