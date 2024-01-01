import os.path
import gitlab
from base64 import b64encode
from pathlib import Path


"""
To generate private access token go to gitlab.com, login and  
- select "edit profile" on the left sidebar
- select access Tokens and generate new Token
- copy the whole content into the following line
"""

print("Enter private access token for Gitlab.com")
privToken=input()
print("Enter Part Name, e.g. 'Relay_SPDT_Omron_G5V-1'")
partName="Relay_JY" #input()
print("Enter Part Library Name, e.g. 'Relay_THT'")
print("Enter Branch Name, e.g. 'OmronG5V'")
branchName="TestBranch" #input()
gl = gitlab.Gitlab(private_token=privToken)
#check authentication
gl.auth()


#--- Files ---
# get script directory
script_dir = Path(__file__).resolve().parent

#TODO check for blanks. No whitespace characters allowed!
#TODO search for all needed files with partname in the same directory
"""
    source: <partName>.fCStd
    3dModel: .wrl, .step
    footprint: .kicad_mod
    symbol: .kicad_sym
"""

#look for 3D source file
if os.path.exists(str(script_dir) +"/"+ partName + ".FCStd"):
    sourceFileName=partName + ".FCStd"
    sourceFilePath=str(script_dir) + "/" + partName + ".FCStd"
else:
    sourceFileName=None
    sourceFilePath=None

# --- Gitlab ---
#get the whole kicad/libraries projects group
group = gl.groups.get(6593439)
kiCADprojects = group.projects.list()

#get owned projects
userProjects = gl.projects.list(owned=True)

for project in userProjects:
    print(project.name)

    try:
        forkedFrom=project.forked_from_project['path_with_namespace']
    except:
        forkedFrom=None

#check if there is already a fork for each project we need in user namespace
    # --- 3D source ---
    if (forkedFrom=="kicad/libraries/kicad-packages3D-source"):
        fork3DSourceID=project.id

        branch=project.branches.get("master")
        #TODO: update fork to upstream if needed 
        try:
            project.branches.create({'branch': branchName,
                                        'ref': "master"})
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            #TODO: handle different excpetions
            print("Branch already exists use? (Y/n)")
            use = input()
            if use=="n":
                exit()

        # -- create a new files
        # TODO handle binary files 
        #https://stackoverflow.com/questions/69829411/upload-binary-files-using-python-gitlab-api
        with open(sourceFilePath, 'rb') as f:
            bin_content = f.read()
            b64_content = b64encode(bin_content).decode('utf-8')

        f = project.files.create({'file_path': sourceFileName,
                          'branch': branchName,
                          'content': b64_content,
                          'encoding': 'base64', #important! (really)
                          'commit_message': 'Source files for' + partName})
    else:
        # TODO: create a new fork from kicad repo
        print("no fork found in user namespace")


        







