# import bpy


print("Hello World")

# In metahuman these end with _r or _l
# Left is parent, right is child
hand_bone_mapping = {
    ("hand", "index_metacarpal"),
        ("index_metacarpal", "index_01"),
            ("index_01", "index_02"),
                ("index_02", "index_03"),

    ("hand", "middle_metacarpal"),
        ("middle_metacarpal", "middle_01"),
            ("middle_01", "middle_02"),
                ("middle_02", "middle_03"),

    ("hand", "pinky_metacarpal"),
        ("pinky_metacarpal", "pinky_01"),
            ("pinky_01", "pinky_02"),
                ("pinky_02", "pinky_03"),


    ("hand", "ring_metacarpal"),
        ("ring_metacarpal", "ring_01"),
            ("ring_01", "ring_02"),
                ("ring_02", "ring_03"),


    ("hand", "thumb_01"),
        ("thumb_01", "thumb_02"),
            ("thumb_02", "thumb_03"),


    ("hand", "wrist_inner"),
    ("hand", "wrist_outer")
}