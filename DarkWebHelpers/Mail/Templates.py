class template:
    msg1 = """مرحبا حسن لقد انتهى البحث الخاص بكلمة: [{}]
 شكرا لحسن ثقتكم في راص                    
"""
    def __repr__(self):
        return self.msg1.format("ammo")
