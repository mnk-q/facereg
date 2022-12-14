import os
import json
from env import HOME

def save_face(image_data):
    verify_or_create_folders()
    img_name = image_data["name"]
    img_path = image_data["image"]
    #Further data can be extracted here and added to a dict
    img_id = get_id(image_data)
    img_local_path = img_path.replace(HOME, "")[1:]
    
    image_dict = {
        "face_id": img_id,
        "person_name" : img_name,
        "headshot" : "static\\saved\\"+str(img_id)+".png"
    }
    # Save this to data.json
    with open("static\\saved\\data.json", "r") as f:
        data = json.load(f)
    temp_data = data.copy()
    try:
        
        data["face"].append(image_dict)
        
        if os.path.isfile("static\\saved\\"+str(img_id)+".png"):
            os.remove("static\\saved\\"+str(img_id)+".png")
        os.rename(img_local_path, "static\\saved\\"+str(img_id)+".png")
        with open("static\\saved\\data.json", "w") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print("Could not save face: ", e)
        with open("static\\saved\\data.json", "w") as f:
            json.dump(temp_data, f, indent=4)
        return e.__str__()
    
def verify_or_create_folders():
    if not os.path.isdir("static\\saved"):
        os.mkdir("static\\saved")
    if not os.path.isfile("static\\saved\\data.json"):
        with open("static\\saved\\data.json", "w") as f:
            json.dump({"face": []}, f, indent=4)
    if not os.path.isdir("static\\uploads"):
        os.mkdir("static\\uploads")
    if not os.path.isdir("static\\uploads\\comp"):
        os.mkdir("static\\uploads\\comp")
def get_id(image_data):
    # Temporary assigned incremental indexing, can be replaced with a hash function
    with open("static\\saved\\data.json", "r") as f:
        data = json.load(f)
    if len(data["face"]) == 0:
        return 1
    return data["face"][-1]["face_id"]+1

def flush_database():
    with open("static\\saved\\data.json", "w") as f:
        json.dump({"face": []}, f, indent=4)
    for file in os.listdir("static\\saved"):
        if file.endswith(".png") or file.endswith(".jpg"):
            os.remove("static\\saved\\"+file)
    for file in os.listdir("static\\uploads\\comp"):
        if file.endswith(".png") or file.endswith(".jpg"):
            os.remove("static\\uploads\\comp\\"+file)
    return True