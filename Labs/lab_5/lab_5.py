import arcpy


class Toolbox(object):
    def __init__(self):
        self.label = "lab5_Toolbox.pyt"
        self.alias = ""
        self.tools = [tool]







class tool(object):
    def __init__(self):
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

def getParameterInfo(self):
    
    param0 = arcpy.Parameter(
        displayName="GDB Folder",
        name="GDBFolder",
        datatype="DEFolder",
        parameterType="Required",
        direction="Input"
    )
    param1 = arcpy.Parameter(
        displayName="GDB Name",
        name="GDBName",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
    )
    param2 = arcpy.Parameter(
        displayName="Garage CSV File",
        name="GarageCSVFile",
        datatype="DEFile",
        parameterType="Required",
        direction="Input"
    )
    param3 = arcpy.Parameter(
        displayName="Garage Layer Name",
        name="GarageLayerName",
        datatype="GPString",
        parameterType="Required",
        direction="Input"
    )
    param4 = arcpy.Parameter(
        displayName="Campus GDB",
        name="Campus GDB",
        datatype="DEType",
        parameterType="Required",
        direction="Input"
    )
    param5 = arcpy.Parameter(
        displayName="Buffer Distance",
        name="BufferDistance",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input"
    )
    params = [param0, param1, param2, param3, param4, param5]
    return params

def isLicensed(self):

    return True

def updateParameters(self, parameters):



    return

def updateMessages(self, parameters):


    return

def execute(self, parameters, messages):

    folder_path = parameters[0].valueAsText
    gdb_name = parameters[1].valueAsText
    gdb_path = folder_path + '\\' + gdb_name
    arcpy.CreateFileGDB_management(folder_path, gdb_name)

    csv_path = parameters[2].valueAsText
    garage_layer_name = parameters[3].valueAsText
    garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)

    input_layer = garages
    arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
    garage_points = gdb_path + '\\' + garage_layer_name

    campus = parameters[4].valueAsText
    buildings_campus = campus + '\Structures'
    buildings = gdb_path + '\\' + 'Buildings'

    arcpy.Copy_management(buildings_campus, buildings)


    spatial_ref = arcpy.Describe(buildings).spatialReference
    arcpy.Project_management(garage_points, gdb_path + '\Garage_Points_reprojected', spatial_ref)

    buffer_distance = int(parameters[5].value)
    garageBuffered = arcpy.Buffer_analysis(gdb_path + '\Garage_Points_reprojected', gdb_path + '\Garage_Points_buffererd', 150)

    arcpy.Intersect_analysis([garageBuffered, buildings], gdb_path + '\Garage_Buildings_Intersection', 'ALL')

    arcpy.TableToTable_conversion(gdb_path + '\Garage_Buildings_Intersection.dbf', r'C:\Users\ckb010\bruns-online-GEOG676-spring2025\Labs\lab_5\lab_5_ArcPro','nearbyBuildings.csv')

    return None
