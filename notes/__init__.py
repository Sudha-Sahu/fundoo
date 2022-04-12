from notes_apis import RegistrationForNotes, LoginForNotes, AddNewNote, EditNote, DeleteNote

notes_routes = [
    (LoginForNotes, '/login/notes/'),
    (RegistrationForNotes, '/registerFor/notes'),
    (AddNewNote, '/add/notes/'),
    (EditNote, '/edit/notes/'),
    (DeleteNote, '/delete/notes')
]
