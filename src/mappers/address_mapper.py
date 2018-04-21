class AddressMapper:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def model_val_assign(self, param):
        if self.view.get(param) is not None:
            setattr(self.model, param, self.view[param])

    def model_mapping(self):
        if self.view and self.model:
            self.model_val_assign('id')
            self.model_val_assign('lane')
            self.model_val_assign('landMark')
            self.model_val_assign('city')
            self.model_val_assign('state')
            self.model_val_assign('country')
            self.model_val_assign('zipcode')


