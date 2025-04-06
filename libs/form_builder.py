class FormBuilder:
    def __init__(self):
        self.fields = []
        self.buttons = []

    def add_field(
        self,
        name,
        type,
        label,
        required=False,
        placeholder=None,
        help_text=None,
        class_name=None,
    ):
        if __debug__:
            assert name is not None, "name is required"
            assert type is not None, "type is required"
            assert label is not None, "label is required"

        self.fields.append(
            {
                "name": name,
                "type": type,
                "label": label,
                "required": required,
                "placeholder": placeholder,
                "help_text": help_text,
                "class_name": class_name,
            }
        )
        return self

    def add_button(self, name, type, label):
        if __debug__:
            assert name is not None, "name is required"
            assert type is not None, "type is required"
            assert label is not None, "label is required"

        self.buttons.append(
            {
                "name": name,
                "type": type,
                "label": label,
                "required": False,
                "placeholder": None,
                "help_text": None,
                "class_name": None,
            }
        )

    def render(self):
        _form = ""
        for field in self.fields:
            required_attr = 'required' if field['required'] else ''
            placeholder = field['placeholder'] or ''
            help_text = field['help_text'] or ''
            class_name = field['class_name'] or ''

            _form += f"""
            <div class="{class_name}">
                <label for="{field['name']}">{field['label']}</label>  
                <input type="{field['type']}" name="{field['name']}" id="{field['name']}" placeholder="{placeholder}" class="{class_name}" {required_attr}>
                <small class="form-text text-muted">{help_text}</small>   
            </div>
            """
        
        for button in self.buttons:
            _form += f"""
            <button type="{button['type']}" class="mt-3 {button['class_name']}">{button['label']}</button>
            """


        return _form
