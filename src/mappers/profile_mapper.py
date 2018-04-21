class ProfileMapper:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def model_val_assign(self, param):
        print(param, ':', self.view.get(param))
        if self.view.get(param) is not None:
            setattr(self.model, param, self.view[param])

    def model_mapping(self):
        if self.view and self.model:
            self.model_val_assign('id')
            self.model_val_assign('name')
            self.model_val_assign('phone')
            self.model_val_assign('mobile')
            self.model_val_assign('email')
            self.model_val_assign('aadhar')
            self.model_val_assign('password')
            self.model_val_assign('token')
            self.model_val_assign('role')
            self.model_val_assign('active')
            self.model_val_assign('vid')



