class Singleton:
    IsSingleton = None
    current_userid=0
    amazonid=""
    def __new__(cls, *args, **kwargs):
        if not cls.IsSingleton:

            cls.IsSingleton= super(Singleton, cls).__new__(cls)
        return cls.IsSingleton

    def get_internal_userid(self):
        return Singleton.current_userid

    def set_internal_userid(self,userid):
        Singleton.current_userid=userid

    def set_amazon_userid(self,amazonuserid):
        Singleton.amazonid=amazonuserid

    def get_amaozn_userid(self):
        return Singleton.amazonid