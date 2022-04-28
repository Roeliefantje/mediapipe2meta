# import bpy

import bpy
import csv
# import numpy as np



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

hand_bone_structure_mp = [
    ("WRIST", "THUMB_MCP"),
        ("THUMB_MCP", "THUMB_IP"),
            ("THUMB_IP", "THUMB_TIP"),

    ("WRIST", "INDEX_FINGER_MCP"),
        ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"),
            ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
                ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP"),

    ("WRIST", "MIDDLE_FINGER_MCP"),
        ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"),
            ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
                ("MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"),

    ("WRIST", "RING_FINGER_MCP"),
        ("RING_FINGER_MCP", "RING_FINGER_PIP"),
            ("RING_FINGER_PIP", "RING_FINGER_DIP"),
                ("RING_FINGER_DIP", "RING_FINGER_TIP"),

    ("WRIST", "PINKY_MCP"),
        ("PINKY_MCP", "PINKY_PIP"),
            ("PINKY_PIP", "PINKY_DIP"),
                ("PINKY_DIP", "PINKY_TIP")
]

pose_bone_structure_mp = [
  ("LEFT_SHOULDER", "LEFT_ELBOW"),
  ("LEFT_ELBOW", "LEFT_WRIST"),
  ("RIGHT_SHOULDER", "RIGHT_ELBOW"),
  ("RIGHT_ELBOW", "RIGHT_WRIST"),

  ("RIGHT_WRIST", "RIGHT_INDEX"), # hand bone right
  ("LEFT_WRIST", "LEFT_INDEX"), # hand bone left

  ("LEFT_SHOULDER", "RIGHT_SHOULDER"), # for left collar (invert all axes)
  ("RIGHT_SHOULDER", "LEFT_SHOULDER"), # for right collar (invert all axes)

#   ("152", "0", "NECK"), # below jaw to lip upper middle to simulate neck bone
#   ("0", "6", "HEAD"), # lip upper middle to mid nose bridge to simulate head bone
#   ("152", "10", "HEAD_NECK") # below jaw to highest face point
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

# https://google.github.io/mediapipe/solutions/pose.html
pose_media_pipe_index = [
    ("NOSE", 0),
    ("LEFT_EYE_INNER", 1),
    ("LEFT_EYE", 2),
    ("LEFT_EYE_OUTER", 3),
    ("RIGHT_EYE_INNER", 4),
    ("RIGHT_EYE", 5),
    ("RIGHT_EYE_OUTER", 6),
    ("LEFT_EAR", 7),
    ("RIGHT_EAR", 8),
    ("MOUTH_LEFT", 9),
    ("MOUTH_RIGHT", 10),
    ("LEFT_SHOULDER", 11),
    ("RIGHT_SHOULDER", 12),
    ("LEFT_ELBOW", 13),
    ("RIGHT_ELBOW", 14),
    ("LEFT_WRIST", 15),
    ("RIGHT_WRIST", 16),
    ("LEFT_PINKY", 17),
    ("RIGHT_PINKY", 18),
    ("LEFT_INDEX", 19),
    ("RIGHT_INDEX", 20),
    ("LEFT_THUMB", 21),
    ("RIGHT_THUMB", 22),
    ("LEFT_HIP", 23),
    ("RIGHT_HIP", 24),
    ("LEFT_KNEE", 25),
    ("RIGHT_KNEE", 26),
    ("LEFT_ANKLE", 27),
    ("RIGHT_ANKLE", 28),
    ("LEFT_HEEL", 29),
    ("RIGHT_HEEL", 30),
    ("LEFT_FOOT_INDEX", 31),
    ("RIGHT_FOOT_INDEX", 32)
]


# Mapping from Mediapipe to the point of the MetaHuman
hand_point_mapping = [
    ("WRIST", "hand"),
    ("THUMB_CMC", "thumb_01"),
    ("THUMB_MCP", "thumb_02"),
    ("THUMB_IP", "thumb_03"),
    ("INDEX_FINGER_MCP", "index_01"),
    ("INDEX_FINGER_PIP", "index_02"),
    ("INDEX_FINGER_DIP", "index_03"),
    ("MIDDLE_FINGER_MCP", "middle_01"),
    ("MIDDLE_FINGER_PIP", "middle_02"),
    ("MIDDLE_FINGER_DIP", "middle_03"),
    ("RING_FINGER_MCP", "ring_01_r"),
    ("RING_FINGER_PIP", "ring_02_r"),
    ("RING_FINGER_DIP", "ring_03_r"),
    ("PINKY_MCP", "pinky_01_r"),
    ("PINKY_PIP", "pinky_02_r"),
    ("PINKY_TIP", "pinky_03_r")
]

# Pose point mapping
pose_point_mapping = [
    ("LEFT_SHOULDER", "upperarm_l"),
    ("LEFT_ELBOW", "lowerarm_l"),
    ("LEFT_WRIST", "hand_l"),
    ("RIGHT_SHOULDER", "upperarm_r"),
    ("RIGHT_ELBOW", "lowerarm_r"),
    ("RIGHT_WRIST", "hand_r")
    # ("LEFT_HIP", "thigh_l"),
    # ("LEFT_KNEE", "shin_l"),
]

unreal_mapping = hand_point_mapping + pose_point_mapping

def isObjectInScene(name):
    for o in bpy.context.scene.objects:
        if o.name == name:
            return True

    return False

def create_landmarks(data, last_char = ""):
    for tupl in data:
        name, locations = tupl

        for tup in unreal_mapping:
            if tup[0] == name:
                name = tup[1]
                break

        name = name + last_char

        if(isObjectInScene(name) != True):
            bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, radius=0.1)
            bpy.context.object.name = name

        for idx, location in enumerate(locations):
            if(location[0] != 0.0):
                x = location[0] * 20
                y = location[1] * 20
                z = location[2] * 20

                obj = bpy.context.scene.objects[name]
                obj.location = [x, y, z]
                obj.keyframe_insert(data_path='location', frame=idx)







def create_armature(name = "", last_char = "", target="hand"):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    armature.name = name + last_char
    armature.pose.bones["Bone"].name = armature.pose.bones["Bone"].name + last_char

    array = hand_bone_structure_mp
    if(target == "pose"):
        array = pose_bone_structure_mp

    for tuple in array:
        parent, child = tuple
        for tup in unreal_mapping:
            if tup[0] == child:
                child = tup[1]
            if tup[0] == parent:
                parent = tup[1]

        child_name = child + last_char
        parent_name = parent + last_char

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.bone_primitive_add(name=child_name)

        bpy.ops.object.mode_set(mode='POSE')
        bone_constraint = armature.pose.bones[child_name].constraints.new('COPY_LOCATION')
        bone_constraint.target = bpy.data.objects[child_name]

        bone_constraint = armature.pose.bones[child_name].constraints.new('STRETCH_TO')
        bone_constraint.target = bpy.data.objects[parent_name]
        bone_constraint.rest_length = 1.0
        bone_constraint.volume = 'NO_VOLUME'
        # bone_constraint = armature.pose.bones[child_name].constraints.new('CHILD_OF')
        # bone_constraint.target = bpy.data.objects[parent_name]




# Outputs list of tuple with bone name and array of locations
def csv_to_arrays(csv_file, target="hand"):
    landmarks = 21
    if(target == "pose"):
        landmarks = 33
    lines = []
    output = []

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        lines = list(reader)

    array = hand_media_pipe_index
    if(target == "pose"):
        array = pose_media_pipe_index

    for tuple in array:
        name, i = tuple
        keyframes = []
        for n in range(i, len(lines), landmarks):
            frame = lines[n]
            x = float(frame[0])
            y = float(frame[1])
            z = float(frame[2])
            # if(x > 0.001 and x < 1 and y > 0.001 and y < 1):
            if(x > 0.001 and y > 0.001):
                # print(f"{name}: x, y, z: {x}, {y}, {z}")
                keyframes.append((x, y, z))
            else:
                # print(f"{name}: x, y, z: 0.0, 0.0, 0.0")
                keyframes.append((0.0, 0.0, 0.0))
        output.append((name, keyframes))

    return output




# create_armature(name="hand", last_char="_r")
# input_data = csv_to_arrays("mediapipe_data/LEFT_HandLandmarks.csv")
input_data = csv_to_arrays("mediapipe_data/POSELandmarks.csv", target="pose")
# print(input_data[0])
create_landmarks(input_data, last_char="")
create_armature(name="pose", last_char="_l")