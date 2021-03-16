class User():
    def __init__(self, user_id):
        self.genuine_signatures = []
        self.forgeries = []


    def get_gen_signature(self, sign_id):
        signature = [x[1] for x in self.genuine_signatures if int(x[0]) == int(sign_id)]
        signature = signature[0]
        return signature

    def get_for_signature(self, sign_id):
        signature = [x[1] for x in self.forgeries if int(x[0]) == int(sign_id)]
        signature = signature[0]
        return signature

    