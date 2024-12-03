from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StickyNote
from .forms import StickyNoteForm

@login_required
def sticky_notes_list(request):
    notes = StickyNote.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notes/sticky_notes_list.html', {'notes': notes})

@login_required
def sticky_note_create(request):
    if request.method == 'POST':
        form = StickyNoteForm(request.POST, request.FILES)
        if form.is_valid():
            sticky_note = form.save(commit=False)
            sticky_note.user = request.user
            sticky_note.save()
            messages.success(request, 'Sticky Note created successfully!')
            return redirect('sticky_notes_list')
    else:
        form = StickyNoteForm()
    return render(request, 'notes/sticky_note_form.html', {'form': form})

@login_required
def sticky_note_edit(request, pk):
    note = get_object_or_404(StickyNote, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StickyNoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sticky Note updated successfully!')
            return redirect('sticky_notes_list')
    else:
        form = StickyNoteForm(instance=note)
    return render(request, 'notes/sticky_note_form.html', {'form': form})

@login_required
def sticky_note_delete(request, pk):
    note = get_object_or_404(StickyNote, pk=pk, user=request.user)
    if request.method == 'POST':
        note.delete()
        messages.success(request, 'Sticky Note deleted successfully!')
        return redirect('sticky_notes_list')
    return render(request, 'notes/sticky_note_confirm_delete.html', {'note': note})
