from django.test import TestCase
from django.urls import reverse
from .models import Note
from .forms import NoteForm

class NoteModelTests(TestCase):
    def test_create_note(self):
        note = Note.objects.create(title="Test Create", content="Hello")
        self.assertEqual(note.title, "Test Create")
        self.assertEqual(note.content, "Hello")
        self.assertIsNotNone(note.created_at)

    def test_update_note(self):
        note = Note.objects.create(title="Old", content="X")
        note.title = "New"
        note.save()
        updated = Note.objects.get(pk=note.pk)
        self.assertEqual(updated.title, "New")

    def test_delete_note(self):
        note = Note.objects.create(title="DeleteMe", content="")
        pk = note.pk
        note.delete()
        self.assertFalse(Note.objects.filter(pk=pk).exists())

class NoteFormTests(TestCase):
    def test_valid_form(self):
        form = NoteForm(data={"title": "Form title", "content": "Form content"})
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_title(self):
        form = NoteForm(data={"title": "", "content": "No title"})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

class NoteViewTests(TestCase):
    def setUp(self):
        self.note1 = Note.objects.create(title="N1", content="C1")
        self.note2 = Note.objects.create(title="N2", content="C2")

    def test_list_view_status_and_template(self):
        url = reverse("note_list")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "notes/note_list.html")
        self.assertIn("notes", resp.context)
        notes = resp.context["notes"]
        self.assertGreaterEqual(notes.count(), 2)

    def test_create_view_get_and_post(self):
        url = reverse("note_create")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "notes/note_form.html")

        resp = self.client.post(url, {"title": "Created", "content": "C"})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Note.objects.filter(title="Created").exists())

    def test_update_view_get_and_post(self):
        url = reverse("note_update", kwargs={"pk": self.note1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "notes/note_form.html")

        resp = self.client.post(url, {"title": "N1-updated", "content": "C1-upd"})
        self.assertEqual(resp.status_code, 302)
        self.note1.refresh_from_db()
        self.assertEqual(self.note1.title, "N1-updated")

    def test_delete_view_get_and_post(self):
        url = reverse("note_delete", kwargs={"pk": self.note2.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "notes/note_confirm_delete.html")

        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Note.objects.filter(pk=self.note2.pk).exists())

class NoteIntegrationTests(TestCase):
    def test_list_page_contains_note_titles(self):
        Note.objects.create(title="Alpha", content="A")
        Note.objects.create(title="Beta", content="B")
        resp = self.client.get(reverse("note_list"))
        self.assertContains(resp, "Alpha")
        self.assertContains(resp, "Beta")

