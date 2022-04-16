from .notes_apis import NoteAPI, EditNotes, PinNotes, TrashNotes

notes_routes = [
    (NoteAPI, '/api/notes'),
    (EditNotes, '/editnotes/<int:note_id>'),
    (PinNotes, '/api/pinnote/<int:note_id>'),
    (TrashNotes, '/api/trashnote/<int:note_id>')
]
