# import bpy

import bpy
import csv
# import numpy as np

from mathutils import Quaternion



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
    ("WRIST", "THUMB_CMC", "THUMB_0"),
        ("THUMB_CMC", "THUMB_MCP"),
            ("THUMB_MCP", "THUMB_IP"),
                ("THUMB_IP", "THUMB_TIP"),

    ("WRIST", "INDEX_FINGER_MCP", "INDEX_0"),
        ("INDEX_FINGER_MCP", "INDEX_FINGER_PIP"),
            ("INDEX_FINGER_PIP", "INDEX_FINGER_DIP"),
                ("INDEX_FINGER_DIP", "INDEX_FINGER_TIP"),

    ("WRIST", "MIDDLE_FINGER_MCP", "MIDDLE_0"),
        ("MIDDLE_FINGER_MCP", "MIDDLE_FINGER_PIP"),
            ("MIDDLE_FINGER_PIP", "MIDDLE_FINGER_DIP"),
                ("MIDDLE_FINGER_DIP", "MIDDLE_FINGER_TIP"),

    ("WRIST", "RING_FINGER_MCP", "RING_0"),
        ("RING_FINGER_MCP", "RING_FINGER_PIP"),
            ("RING_FINGER_PIP", "RING_FINGER_DIP"),
                ("RING_FINGER_DIP", "RING_FINGER_TIP"),

    ("WRIST", "PINKY_MCP", "PINKY_0"),
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
    ("SPINE_TOP", "LEFT_SHOULDER", "LEFT_CLAVICLE"),
    ("SPINE_TOP", "RIGHT_SHOULDER", "RIGHT_CLAVICLE"),
    ("SPINE_BOTTOM", "SPINE_TOP", "SPINE"),
    ("SPINE_BOTTOM", "RIGHT_HIP", "RIGHT_HIP"),
    ("SPINE_BOTTOM", "LEFT_HIP", "LEFT_HIP"),
    ("RIGHT_HIP", "RIGHT_KNEE", "RIGHT_LEG"),
    ("LEFT_HIP", "LEFT_KNEE", "LEFT_LEG"),
    ("RIGHT_KNEE", "RIGHT_ANKLE"),
    ("LEFT_KNEE", "LEFT_ANKLE"),
    ("RIGHT_ANKLE", "RIGHT_HEEL"),
    ("LEFT_ANKLE", "LEFT_HEEL"),
    ("RIGHT_HEEL", "RIGHT_FOOT_INDEX"),
    ("LEFT_HEEL", "LEFT_FOOT_INDEX"),


#   ("LEFT_SHOULDER", "RIGHT_SHOULDER"), # for left collar (invert all axes)
#   ("RIGHT_SHOULDER", "LEFT_SHOULDER"), # for right collar (invert all axes)

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

pose_virtual_landmarks= [
    ("SPINE_BOTTOM", "LEFT_HIP", "RIGHT_HIP"),
    ("SPINE_TOP", "LEFT_SHOULDER", "RIGHT_SHOULDER"),
]


# Mapping from Mediapipe to the point of the MetaHuman
left_hand_point_mapping_metahuman = [
    # ("WRIST", "hand"),
    ("THUMB_CMC_l", "thumb_01_l"),
    ("THUMB_MCP_l", "thumb_02_l"),
    ("THUMB_IP_l", "thumb_03_l"),
    ("INDEX_FINGER_MCP_l", "index_01_l"),
    ("INDEX_FINGER_PIP_l", "index_02_l"),
    ("INDEX_FINGER_DIP_l", "index_03_l"),
    ("MIDDLE_FINGER_MCP_l", "middle_01_l"),
    ("MIDDLE_FINGER_PIP_l", "middle_02_l"),
    ("MIDDLE_FINGER_DIP_l", "middle_03_l"),
    ("RING_FINGER_MCP_l", "ring_01_l"),
    ("RING_FINGER_PIP_l", "ring_02_l"),
    ("RING_FINGER_DIP_l", "ring_03_l"),
    ("PINKY_MCP_l", "pinky_01_l"),
    ("PINKY_PIP_l", "pinky_02_l"),
    ("PINKY_TIP_l", "pinky_03_l")
]

right_hand_point_mapping_metahuman = [
    # ("WRIST", "hand"),
    ("THUMB_CMC_r", "thumb_01_r"),
    ("THUMB_MCP_r", "thumb_02_r"),
    ("THUMB_IP_r", "thumb_03_r"),
    ("INDEX_FINGER_MCP_r", "index_01_r"),
    ("INDEX_FINGER_PIP_r", "index_02_r"),
    ("INDEX_FINGER_DIP_r", "index_03_r"),
    ("MIDDLE_FINGER_MCP_r", "middle_01_r"),
    ("MIDDLE_FINGER_PIP_r", "middle_02_r"),
    ("MIDDLE_FINGER_DIP_r", "middle_03_r"),
    ("RING_FINGER_MCP_r", "ring_01_r"),
    ("RING_FINGER_PIP_r", "ring_02_r"),
    ("RING_FINGER_DIP_r", "ring_03_r"),
    ("PINKY_MCP_r", "pinky_01_r"),
    ("PINKY_PIP_r", "pinky_02_r"),
    ("PINKY_TIP_r", "pinky_03_r")
]

# Pose point mapping
pose_point_mapping_metahuman = [
    ("LEFT_SHOULDER", "upperarm_l"),
    ("LEFT_ELBOW", "lowerarm_l"),
    ("LEFT_WRIST", "hand_l"),
    ("RIGHT_SHOULDER", "upperarm_r"),
    ("RIGHT_ELBOW", "lowerarm_r"),
    ("RIGHT_WRIST", "hand_r")
    # ("LEFT_HIP", "thigh_l"),
    # ("LEFT_KNEE", "shin_l"),
]

# Mapping from Mediapipe to the joints of the ReadyPlayerMeCharachter
pose_point_mapping_readyplayerme = [
    ("LEFT_SHOULDER", "LeftArm"),
    ("LEFT_ELBOW", "LeftForeArm"),
    ("LEFT_WRIST", "LeftHand"),
    ("RIGHT_SHOULDER", "RightArm"),
    ("RIGHT_ELBOW", "RightForeArm"),
    ("RIGHT_WRIST", "RightHand"),
    ("RIGHT_CLAVICLE", "RightShoulder"),
    ("LEFT_CLAVICLE", "LeftShoulder"),
    ("SPINE", "Hips"),
    ("RIGHT_LEG", "RightUpLeg"),
    ("LEFT_LEG", "LeftUpLeg"),
    ("RIGHT_KNEE", "RightLeg"),
    ("LEFT_KNEE", "LeftLeg"),
    ("RIGHT_ANKLE", "RightFoot"),
    ("LEFT_ANKLE", "LeftFoot"),
    ("LEFT_WRIST", "LeftHand"),
    ("RIGHT_WRIST", "RightHand")
]

left_hand_point_mapping_readyplayerme = [
    ("THUMB_0_l", "LeftHandThumb1"),
    ("THUMB_CMC_l", "LeftHandThumb2"),
    ("THUMB_MCP_l", "LeftHandThumb3"),
    ("INDEX_FINGER_MCP_l", "LeftHandIndex1"),
    ("INDEX_FINGER_PIP_l", "LeftHandIndex2"),
    ("INDEX_FINGER_DIP_l", "LeftHandIndex3"),
    ("MIDDLE_FINGER_MCP_l", "LeftHandMiddle1"),
    ("MIDDLE_FINGER_PIP_l", "LeftHandMiddle2"),
    ("MIDDLE_FINGER_DIP_l", "LeftHandMiddle3"),
    ("RING_FINGER_MCP_l", "LeftHandRing1"),
    ("RING_FINGER_PIP_l", "LeftHandRing2"),
    ("RING_FINGER_DIP_l", "LeftHandRing3"),
    ("PINKY_MCP_l", "LeftHandPinky1"),
    ("PINKY_PIP_l", "LeftHandPinky2"),
    ("PINKY_DIP_l", "LeftHandPinky3")
]

right_hand_point_mapping_readyplayerme = [
    ("THUMB_0_r", "RightHandThumb1"),
    ("THUMB_CMC_r", "RightHandThumb2"),
    ("THUMB_MCP_r", "RightHandThumb3"),
    ("INDEX_FINGER_MCP_r", "RightHandIndex1"),
    ("INDEX_FINGER_PIP_r", "RightHandIndex2"),
    ("INDEX_FINGER_DIP_r", "RightHandIndex3"),
    ("MIDDLE_FINGER_MCP_r", "RightHandMiddle1"),
    ("MIDDLE_FINGER_PIP_r", "RightHandMiddle2"),
    ("MIDDLE_FINGER_DIP_r", "RightHandMiddle3"),
    ("RING_FINGER_MCP_r", "RightHandRing1"),
    ("RING_FINGER_PIP_r", "RightHandRing2"),
    ("RING_FINGER_DIP_r", "RightHandRing3"),
    ("PINKY_MCP_r", "RightHandPinky1"),
    ("PINKY_PIP_r", "RightHandPinky2"),
    ("PINKY_DIP_r", "RightHandPinky3")
]


# unreal_mapping = hand_point_mapping_metahuman + pose_point_mapping_metahuman
readyplayerme_mapping = pose_point_mapping_readyplayerme + left_hand_point_mapping_readyplayerme


def map_rotation(source_armature="motion_capture_armature", target_rig="Armature", mapping=pose_point_mapping_readyplayerme):


    for map in mapping:
        rotation_copy_constr = bpy.data.objects[target_rig].pose.bones[map[1]].constraints.new(type='TRANSFORM')
        # rotation_copy_constr = bpy.data.objects[target_rig].children[1].pose.bones[map[1]].constraints.new(type='COPY_ROTATION')
        # The target of the copy rotation is the armature of the motion capture
        rotation_copy_constr.target = bpy.data.objects[source_armature]
        # This is set just by a string value of the subtargets name
        rotation_copy_constr.subtarget = map[0]


        rotation_copy_constr.target_space = 'WORLD'
        rotation_copy_constr.map_from = 'ROTATION'
        rotation_copy_constr.from_rotation_mode = 'XYZ'
        rotation_copy_constr.from_min_x_rot = -6.283185307179586
        rotation_copy_constr.from_max_x_rot = 6.283185307179586
        rotation_copy_constr.from_min_y_rot = -6.283185307179586
        rotation_copy_constr.from_max_y_rot = 6.283185307179586
        rotation_copy_constr.from_min_z_rot = -6.283185307179586
        rotation_copy_constr.from_max_z_rot = 6.283185307179586

        rotation_copy_constr.map_to = 'ROTATION'
        rotation_copy_constr.to_euler_order = 'XYZ'
        rotation_copy_constr.to_min_x_rot = -6.283185307179586
        rotation_copy_constr.to_max_x_rot = 6.283185307179586
        rotation_copy_constr.to_min_y_rot = -6.283185307179586
        rotation_copy_constr.to_max_y_rot = 6.283185307179586
        rotation_copy_constr.to_min_z_rot = -6.283185307179586
        rotation_copy_constr.to_max_z_rot = 6.283185307179586
        rotation_copy_constr.mix_mode_rot = 'REPLACE'




def isObjectInScene(name):
    for o in bpy.context.scene.objects:
        if o.name == name:
            return True

    return False

def create_landmarks(data, last_char = "", sample_rate=1):
    for tupl in data:
        name, locations = tupl

        name = name + last_char

        if(isObjectInScene(name) != True):
            bpy.ops.mesh.primitive_ico_sphere_add(enter_editmode=False, radius=0.01)
            bpy.context.object.name = name

        # Have the counter start one before the sample rate,
        # this way it will always animate the first frame.
        counter = sample_rate - 1
        for idx, location in enumerate(locations):

            if(sample_rate > 1):
                counter += 1
                if counter == sample_rate:
                    counter = 0
                else:
                    continue

            if(location[0] != 0.0):
                x = location[0] * 5
                y = location[1] * 5
                z = location[2] * 5

                obj = bpy.context.scene.objects[name]
                obj.location = [x, y, z]
                obj.keyframe_insert(data_path='location', frame=idx)

# Create virtual landmark data for spine locations
def create_virtual_landmark_data(data, target="pose"):
    if target != "pose":
        return

    for tupl in pose_virtual_landmarks:
        name, landmark1, landmark2 = tupl

        points_landmark1 = []
        points_landmark2 = []
        for values in data:
            landmark_name, locations = values
            if landmark_name == landmark1:
                points_landmark1 = locations
            if landmark_name == landmark2:
                points_landmark2 = locations

        new_locations = []
        for idx, location in enumerate(points_landmark1):
            new_location_x = (location[0] + points_landmark2[idx][0]) / 2
            new_location_y = (location[1] + points_landmark2[idx][1]) / 2
            new_location_z = (location[2] + points_landmark2[idx][2]) / 2
            new_locations.append([new_location_x, new_location_y, new_location_z])
        data.append((name, new_locations))

    return data







def create_armature(name = "motion_capture_armature", last_char = "", target="hand"):
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.armature_add()
    armature = bpy.context.active_object
    armature.name = name + last_char
    armature.pose.bones["Bone"].name = armature.pose.bones["Bone"].name + last_char

    array = hand_bone_structure_mp
    if(target == "pose"):
        array = pose_bone_structure_mp

    for tuple in array:
        parent_name = tuple[0] + last_char
        child_name = tuple[1] + last_char

        # If bone_name is specified use that name instead.
        bone_name = parent_name
        if len(tuple) == 3:
            bone_name = tuple[2] + last_char

        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.armature.bone_primitive_add(name=bone_name)

        bpy.ops.object.mode_set(mode='POSE')

        if(target == "hand"):
            armature.pose.bones[bone_name].scale[0] = 0.1
            armature.pose.bones[bone_name].scale[1] = 0.1
            armature.pose.bones[bone_name].scale[2] = 0.1


        bone_constraint = armature.pose.bones[bone_name].constraints.new('COPY_LOCATION')
        bone_constraint.target = bpy.data.objects[parent_name]

        bone_constraint = armature.pose.bones[bone_name].constraints.new('STRETCH_TO')
        bone_constraint.target = bpy.data.objects[child_name]
        bone_constraint.rest_length = 1.0
        bone_constraint.volume = 'NO_VOLUME'
        bone_constraint.keep_axis = 'PLANE_Z'
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
            # Translate to blender coords

            frame = lines[n]
            x = float(frame[0]) # left-right
            y = float(frame[2]) # depth
            z = 1 - float(frame[1]) # height
            # if(x > 0.001 and x < 1 and y > 0.001 and y < 1):
            if target == "hand":
                if(x > 0.001 and x < 1):
                    keyframes.append((x, y, z))
                else:
                    keyframes.append((0, 0, 0))
            else:
                if(x > 0.001):
                    # print(f"{name}: x, y, z: {x}, {y}, {z}")
                    keyframes.append((x, y, z))
                else:
                    # print(f"{name}: x, y, z: 0.0, 0.0, 0.0")
                    keyframes.append((0.0, 0.0, 0.0))
        output.append((name, keyframes))

    return output

def rotate_bvh_armatures(armature="f_med_nrw_body"):
    bpy.data.objects[armature].rotation_euler[0] = -3.66519 # -210d



# create_armature(name="hand", last_char="_r")
input_data = csv_to_arrays("mediapipe_data/LEFT_HandLandmarks.csv")
# Maak de landmarks in de scene
create_landmarks(input_data, last_char="_l", sample_rate=1)

input_data = csv_to_arrays("mediapipe_data/RIGHT_HandLandmarks.csv")
create_landmarks(input_data, last_char="_r", sample_rate=1)

# Maak arrays van de csv data
input_data = csv_to_arrays("mediapipe_data/POSELandmarks.csv", target="pose")
input_data = create_virtual_landmark_data(input_data, target="pose")
create_landmarks(input_data, sample_rate=3)


# Maak de bone structure die bij de punten hoort.
create_armature(target="hand", last_char="_l")
create_armature(target="hand", last_char="_r")
create_armature(target="pose")

# map_rotation(mapping=pose_point_mapping_readyplayerme, source_armature="motion_capture_armature")
# map_rotation(mapping=left_hand_point_mapping_readyplayerme, source_armature="motion_capture_armature_l")
# map_rotation(mapping=right_hand_point_mapping_readyplayerme, source_armature="motion_capture_armature_r")
map_rotation(mapping=pose_point_mapping_metahuman, source_armature="motion_capture_armature", target_rig="f_med_nrw_body")
map_rotation(mapping=left_hand_point_mapping_metahuman2, source_armature="motion_capture_armature_l", target_rig="f_med_nrw_body")
map_rotation(mapping=right_hand_point_mapping_metahuman2, source_armature="motion_capture_armature_r", target_rig="f_med_nrw_body")