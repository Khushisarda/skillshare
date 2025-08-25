from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Academics


def resource_list_view(request, resource_type, page_title):
    """Generic view for listing resources (notes, pyqs, books) with filters"""
    department = request.GET.get('department')
    year = request.GET.get('year')
    search = request.GET.get('search', '')

    # Base queryset
    resources = Academics.objects.filter(resource_type=resource_type, is_active=True)

    # Filters
    if department:
        resources = resources.filter(department=department)
    if year:
        resources = resources.filter(year=year)
    if search:
        resources = resources.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(subject_name__icontains=search) |
            Q(subject_code__icontains=search) |
            Q(tags__icontains=search)
        )

    # All filter options
    all_departments = Academics.DEPARTMENTS
    all_years = Academics.YEARS

    # Dynamic years
    if department:
        available_years = Academics.objects.filter(
            department=department,
            resource_type=resource_type,
            is_active=True
        ).values_list('year', flat=True).distinct().order_by('year')
    else:
        available_years = [y[0] for y in all_years]

    # Pagination
    paginator = Paginator(resources, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'resources': page_obj,
        'all_departments': all_departments,
        'all_years': all_years,
        'selected_department': department,
        'selected_year': year,
        'search_query': search,
        'available_years': available_years,
        'resource_type': resource_type,
        'page_title': page_title,
    }
    return render(request, 'academics/resource_list.html', context)


# Now you only need thin wrappers:
def notes_view(request):
    return resource_list_view(request, 'notes', 'Study Notes')

def pyqs_view(request):
    return resource_list_view(request, 'pyqs', 'Previous Year Questions')

def books_view(request):
    return resource_list_view(request, 'books', 'Reference Books')


def get_years_by_department(request):
    """AJAX: Get available years for department"""
    department = request.GET.get('department')
    resource_type = request.GET.get('resource_type', 'notes')
    years = []

    if department:
        years_qs = Academics.objects.filter(
            department=department,
            resource_type=resource_type,
            is_active=True
        ).values_list('year', flat=True).distinct().order_by('year')
        years = [{'value': y, 'label': f'Year {y}'} for y in years_qs]

    return JsonResponse({'years': years})


def get_subjects_by_department_year(request):
    """AJAX: Get unique subjects for department + year"""
    department = request.GET.get('department')
    year = request.GET.get('year')
    resource_type = request.GET.get('resource_type', 'notes')
    subjects = []

    if department and year:
        subjects = list(
            Academics.objects.filter(
                department=department, year=year,
                resource_type=resource_type, is_active=True
            ).values('subject_name', 'subject_code')
             .distinct().order_by('subject_name')
        )

    return JsonResponse({'subjects': subjects})


def resource_detail_view(request, pk):
    resource = get_object_or_404(Academics, pk=pk, is_active=True)
    resource.increment_views()
    
    # if file exists, open it
    if resource.file:
        return redirect(resource.file.url)
    
    # if external link exists, open it
    if resource.external_link:
        return redirect(resource.external_link)
    
    # fallback: stay on dashboard (or raise 404)
    return redirect('academics:dashboard')


def dashboard_view(request):
    """Dashboard with statistics"""
    stats = {
        'total_notes': Academics.objects.filter(resource_type='notes', is_active=True).count(),
        'total_pyqs': Academics.objects.filter(resource_type='pyqs', is_active=True).count(),
        'total_books': Academics.objects.filter(resource_type='books', is_active=True).count(),
        'departments': len(Academics.DEPARTMENTS),
        'total_views': sum(Academics.objects.filter(is_active=True).values_list('views', flat=True)) or 0,
    }

    recent = Academics.objects.filter(is_active=True).order_by('-uploaded_at')[:8]
    popular = Academics.objects.filter(is_active=True).order_by('-views')[:8]

    dept_stats = [
        {'code': d, 'name': n, 'count': Academics.objects.filter(department=d, is_active=True).count()}
        for d, n in Academics.DEPARTMENTS
        if Academics.objects.filter(department=d, is_active=True).exists()
    ]

    return render(request, 'academics/dashboard.html', {
        'stats': stats,
        'recent_resources': recent,
        'popular_resources': popular,
        'dept_stats': dept_stats,
    })
