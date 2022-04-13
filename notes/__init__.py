from .notes_apis import Note, EditNotes

notes_routes = [
    (Note, '/notes/'),
    (EditNotes, '/editnotes/<int:id>')
]
