from django.shortcuts import render, redirect, get_object_or_404
from .models import Note
from .forms import NoteForm

def home(request):
    notes = Note.objects.all()
    return render(request, "notes/home.html", {"notes": notes})

def add_note(request):
    form = NoteForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "notes/add_note.html", {"form": form})

def edit_note(request, id):
    note = get_object_or_404(Note, id=id)
    form = NoteForm(request.POST or None, instance=note)
    if form.is_valid():
        form.save()
        return redirect("home")
    return render(request, "notes/edit_note.html", {"form": form, "note": note})

def delete_note(request, id):
    note = get_object_or_404(Note, id=id)
    if request.method == "POST":
        note.delete()
        return redirect("home")
    return render(request, "notes/delete_confirm.html", {"note": note})
