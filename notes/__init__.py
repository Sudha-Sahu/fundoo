from .notes_apis import NoteAPI, EditNotes

notes_routes = [
    (NoteAPI, '/api/notes'),
    (EditNotes, '/editnotes/<int:note_id>')
]
