# import bpy

import bpy
import csv



# In metahuman these end with _r or _l
# Left is parent, right is child
# Each tuple represents a bone
hand_bone_structure = [
    ("Bone", "hand"),
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
]

# Index of every bone in the mediapipe representation of hand
hand_media_pipe_index = [
    ("WRIST", 0),
    ("THUMB_CMC", 1),
    ("THUMB_MCP", 2),
    ("THUMB_IP", 3),
    ("THUMB_TIP", 4),
    ("INDEX_FINGER_MCP", 5),
    ("INDEX_FINGER_PIP", 6),
    ("INDEX_FINGER_DIP", 7),
    ("INDEX_FINGER_TIP", 8),
    ("MIDDLE_FINGER_MCP", 9),
    ("MIDDLE_FINGER_PIP", 10),
    ("MIDDLE_FINGER_DIP", 11),
    ("MIDDLE_FINGER_TIP", 12),
    ("RING_FINGER_MCP", 13),
    ("RING_FINGER_PIP", 14),
    ("RING_FINGER_DIP", 15),
    ("RING_FINGER_TIP", 16),
    ("PINKY_MCP", 17),
    ("PINKY_PIP", 18),
    ("PINKY_DIP", 19),
    ("PINKY_TIP", 20)
]

# Mapping from Mediapipe to the point of the MetaHuman
hand_point_mapping = [
    ("WRIST", "hand"),
    # TODO rest...
]


def create_armature(name = "", last_char = ""):
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    armature.name = name + last_char
    armature.pose.bones["Bone"].name = armature.pose.bones["Bone"].name + last_char

    for tuple in hand_bone_structure:
        parent, child = tuple
        child_name = child + last_char
        parent_name = parent + last_char

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.bone_primitive_add(name=child)

        bpy.ops.object.mode_st(mode='POSE')
        bone_constraint = armature.pose.bones[child_name].constraints.new('COPY_LOCATION')
        bone_constraint.target = bpy.data.objects(child_name)

        bone_constraint = armature.pose.bones[child_name].constraints.new('COPY_LOCATION')
        bone_constraint.target = bpy.data.objects(parent_name)




# Outputs list of tuple with bone name and array of locations
def csv_to_arrays(csv_file):
    hand_landmarks = 21
    lines = []
    output = []

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)

    for tuple in hand_media_pipe_index:
        name, i = tuple
        keyframes = []
        for n in range(i, len(lines), hand_landmarks):
            frame = lines[n]
            x = float(frame[0])
            y = float(frame[1])
            z = float(frame[2])
            if(x > 0.001 and x < 1 and y > 0.001 and y < 1 and z > 0.001 and z < 1):
                # print(f"{name}: x, y, z: {x}, {y}, {z}")
                keyframes.append((x, y, z))
            else:
                # print(f"{name}: x, y, z: 0.0, 0.0, 0.0")
                keyframes.append((0.0, 0.0, 0.0))
        output.append((name, keyframes))

    return output




create_armature(name="hand", last_char="_r")
input_data = csv_to_arrays("mediapipe_data/LEFT_HandLandmarks.csv")