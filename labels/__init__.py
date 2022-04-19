from .label_apis import LabelAPI, EditLabel

label_routes = [
    (LabelAPI, '/api/label'),
    (EditLabel, '/api/editlabel/<int:label_id>')
]
