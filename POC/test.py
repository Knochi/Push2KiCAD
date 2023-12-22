import gitlab

gl = gitlab.Gitlab()

#get the whole kicad/libraries projects group
group = gl.groups.get(6593439)
print("Group URL:" + group.web_url)
projects = group.projects.list()

for project in projects:
    print(project.name)




