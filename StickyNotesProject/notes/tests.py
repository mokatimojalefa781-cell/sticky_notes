from django.test import TestCase
from django.urls import reverse
from .models import Note

class NoteModelTests(TestCase):
    def test_create_note(self):
        note = Note.objects.create(title="Test", content="Content")
        self.assertEqual(note.title, "Test")
        self.assertEqual(note.content, "Content")

    def test_read_notes(self):
        Note.objects.create(title="A", content="One")
        Note.objects.create(title="B", content="Two")
        self.assertEqual(Note.objects.count(), 2)

    def test_update_note(self):
        note = Note.objects.create(title="Old", content="Old content")
        note.title = "New"
        note.save()
        self.assertEqual(Note.objects.first().title, "New")

    def test_delete_note(self):
        note = Note.objects.create(title="Delete", content="Remove")
        pk = note.pk
        note.delete()
        self.assertFalse(Note.objects.filter(pk=pk).exists())
