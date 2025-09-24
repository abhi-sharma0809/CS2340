import re
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Job
from accounts.models import Profile

def _skill_tokens(text: str):
    if not text:
        return []
    # split on commas/newlines and non-alphanumerics; lower-case; dedupe
    raw = re.split(r"[,\n]+", text)
    tokens = []
    for chunk in raw:
        for t in re.findall(r"[A-Za-z0-9+#\.]+", chunk.lower()):
            if len(t) >= 2:
                tokens.append(t)
    return list(dict.fromkeys(tokens))  # preserve order, remove dups

@login_required
def recommended_jobs(request):
    profile = Profile.objects.filter(user=request.user).first()
    skills = _skill_tokens(profile.skills if profile else "")
    qs = Job.objects.all()

    # quick shortlist: any job that matches at least one skill in title or description
    q_filter = Q()
    for s in skills:
        q_filter |= Q(title__icontains=s) | Q(description__icontains=s)
    shortlisted = qs.filter(q_filter) if skills else qs.none()

    # score & sort in Python (simple, transparent)
    def score(job):
        text = (job.title + " " + job.description).lower()
        return sum(text.count(s) for s in skills)

    ranked = sorted(shortlisted, key=score, reverse=True)
    return render(request, "jobs/recommended.html", {
        "skills": skills,
        "jobs": ranked[:25],  # top 25
    })

def job_list(request):
    qs = Job.objects.all()
    q = request.GET.get
    if q("title"): qs = qs.filter(title__icontains=q("title"))
    if q("location"): qs = qs.filter(location__icontains=q("location"))
    if q("remote") == "1": qs = qs.filter(is_remote=True)
    if q("visa") == "1": qs = qs.filter(visa_sponsorship=True)
    if q("salary_min"): qs = qs.filter(salary_min__gte=q("salary_min"))
    if q("salary_max"): qs = qs.filter(salary_max__lte=q("salary_max"))
    return render(request, "jobs/job_list.html", {"jobs": qs, "filters": request.GET})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    return render(request, "jobs/job_detail.html", {"job": job})
