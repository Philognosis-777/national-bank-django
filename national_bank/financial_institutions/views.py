from django.http import JsonResponse
from django.views import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils import timezone

from .models import InstitutionType, FinancialInstitution, Branch
from .mixins import AdminRequiredMixin


class InstitutionTypeListView(AdminRequiredMixin, View):
    def get(self, request):
        qs = InstitutionType.objects.all().order_by('name')
        data = [{'id': t.pk, 'name': t.name, 'description': t.description} for t in qs]
        return JsonResponse({'results': data})


class InstitutionTypeCreateView(AdminRequiredMixin, View):
    def post(self, request):
        data = request.POST
        t = InstitutionType.objects.create(name=data.get('name'), description=data.get('description', ''))
        return JsonResponse({'id': t.pk, 'created': True})


class InstitutionTypeUpdateView(AdminRequiredMixin, View):
    def post(self, request, pk):
        t = get_object_or_404(InstitutionType, pk=pk)
        data = request.POST
        t.name = data.get('name', t.name)
        t.description = data.get('description', t.description)
        t.save()
        return JsonResponse({'id': t.pk, 'updated': True})


class InstitutionTypeDeleteView(AdminRequiredMixin, View):
    def post(self, request, pk):
        t = get_object_or_404(InstitutionType, pk=pk)
        t.delete()
        return JsonResponse({'id': pk, 'deleted': True})


class InstitutionListView(View):
    def get(self, request):
        qs = FinancialInstitution.objects.all().order_by('name')

        # public: only active
        user = request.user
        if not (user.is_authenticated and (getattr(user, 'role', None) == 'admin' or user.is_superuser)):
            qs = qs.filter(status=FinancialInstitution.STATUS_ACTIVE)

        # filtering
        q = request.GET.get('q')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(license_number__icontains=q))
        inst_type = request.GET.get('type')
        if inst_type:
            qs = qs.filter(institution_type__name__iexact=inst_type)
        status = request.GET.get('status')
        if status:
            qs = qs.filter(status__iexact=status)

        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 25))
        paginator = Paginator(qs, per_page)
        try:
            page_obj = paginator.page(page)
        except EmptyPage:
            return JsonResponse({'results': [], 'count': paginator.count})

        results = [
            {
                'name': i.name,
                'slug': i.slug,
                'license_number': i.license_number,
                'institution_type': i.institution_type.name,
                'status': i.status,
                'is_supervised': i.is_supervised,
            }
            for i in page_obj.object_list
        ]

        return JsonResponse({'results': results, 'count': paginator.count, 'num_pages': paginator.num_pages})


class InstitutionDetailView(View):
    def get(self, request, slug):
        inst = get_object_or_404(FinancialInstitution, slug=slug)
        if inst.status != FinancialInstitution.STATUS_ACTIVE:
            user = request.user
            if not (user.is_authenticated and (getattr(user, 'role', None) == 'admin' or user.is_superuser)):
                return JsonResponse({'error': 'Not found'}, status=404)

        data = {
            'name': inst.name,
            'slug': inst.slug,
            'license_number': inst.license_number,
            'institution_type': inst.institution_type.name,
            'established_date': inst.established_date.isoformat() if inst.established_date else None,
            'head_office_address': inst.head_office_address,
            'contact_email': inst.contact_email,
            'contact_phone': inst.contact_phone,
            'website': inst.website,
            'capital_amount': str(inst.capital_amount),
            'status': inst.status,
            'is_supervised': inst.is_supervised,
        }
        return JsonResponse(data)


class InstitutionCreateView(AdminRequiredMixin, View):
    def post(self, request):
        d = request.POST
        inst = FinancialInstitution.objects.create(
            name=d.get('name'),
            institution_type_id=d.get('institution_type'),
            license_number=d.get('license_number'),
            established_date=d.get('established_date') or None,
            head_office_address=d.get('head_office_address', ''),
            contact_email=d.get('contact_email', ''),
            contact_phone=d.get('contact_phone', ''),
            website=d.get('website', ''),
            capital_amount=d.get('capital_amount') or 0,
            status=d.get('status') or FinancialInstitution.STATUS_ACTIVE,
            is_supervised=d.get('is_supervised', True),
        )
        return JsonResponse({'id': inst.pk, 'created': True})


class InstitutionUpdateView(AdminRequiredMixin, View):
    def post(self, request, slug):
        inst = get_object_or_404(FinancialInstitution, slug=slug)
        d = request.POST
        inst.name = d.get('name', inst.name)
        if d.get('institution_type'):
            inst.institution_type_id = d.get('institution_type')
        inst.license_number = d.get('license_number', inst.license_number)
        inst.established_date = d.get('established_date') or inst.established_date
        inst.head_office_address = d.get('head_office_address', inst.head_office_address)
        inst.contact_email = d.get('contact_email', inst.contact_email)
        inst.contact_phone = d.get('contact_phone', inst.contact_phone)
        inst.website = d.get('website', inst.website)
        inst.capital_amount = d.get('capital_amount', inst.capital_amount)
        inst.status = d.get('status', inst.status)
        inst.is_supervised = d.get('is_supervised', inst.is_supervised)
        inst.save()
        return JsonResponse({'id': inst.pk, 'updated': True})


class InstitutionDeleteView(AdminRequiredMixin, View):
    def post(self, request, slug):
        inst = get_object_or_404(FinancialInstitution, slug=slug)
        inst.delete()
        return JsonResponse({'slug': slug, 'deleted': True})


class BranchListView(View):
    def get(self, request, institution_slug):
        inst = get_object_or_404(FinancialInstitution, slug=institution_slug)
        qs = inst.branches.all().order_by('branch_name')
        data = [{'id': b.pk, 'branch_name': b.branch_name, 'city': b.city, 'region': b.region, 'is_active': b.is_active} for b in qs]
        return JsonResponse({'results': data})


class BranchCreateView(AdminRequiredMixin, View):
    def post(self, request, institution_slug):
        inst = get_object_or_404(FinancialInstitution, slug=institution_slug)
        d = request.POST
        b = inst.branches.create(
            branch_name=d.get('branch_name'),
            region=d.get('region', ''),
            city=d.get('city', ''),
            address=d.get('address', ''),
            is_active=d.get('is_active', True),
        )
        return JsonResponse({'id': b.pk, 'created': True})


class BranchUpdateView(AdminRequiredMixin, View):
    def post(self, request, institution_slug, pk):
        inst = get_object_or_404(FinancialInstitution, slug=institution_slug)
        b = get_object_or_404(Branch, pk=pk, institution=inst)
        d = request.POST
        b.branch_name = d.get('branch_name', b.branch_name)
        b.region = d.get('region', b.region)
        b.city = d.get('city', b.city)
        b.address = d.get('address', b.address)
        b.is_active = d.get('is_active', b.is_active)
        b.save()
        return JsonResponse({'id': b.pk, 'updated': True})


class BranchDeleteView(AdminRequiredMixin, View):
    def post(self, request, institution_slug, pk):
        inst = get_object_or_404(FinancialInstitution, slug=institution_slug)
        b = get_object_or_404(Branch, pk=pk, institution=inst)
        b.delete()
        return JsonResponse({'id': pk, 'deleted': True})

class InstitutionDashboardView(AdminRequiredMixin, View):
    def get(self, request, slug):
        inst = get_object_or_404(FinancialInstitution, slug=slug)
        data = {
            'name': inst.name,
            'license_number': inst.license_number,
            'institution_type': inst.institution_type.name,
            'established_date': inst.established_date.isoformat() if inst.established_date else None,
            'head_office_address': inst.head_office_address,
            'contact_email': inst.contact_email,
            'contact_phone': inst.contact_phone,
            'website': inst.website,
            'capital_amount': str(inst.capital_amount),
            'status': inst.status,
            'is_supervised': inst.is_supervised,
            'branches_count': inst.branches.count(),
        }
        return JsonResponse(data)