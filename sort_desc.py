'''Script that sorts converted kml files for USER scavenger hunt'''
lyr = iface.mapCanvas().currentLayer()
pr = lyr.dataProvider()
flds = lyr.fields()

def sortFeatures(ftr):
    """takes a feature, finds if desc contains points, info, bonus, and challenge,
    separates them into individual values in the corresponding fields"""
    desc = ftr.attribute('description')
    getInfo(desc, ftr)

def removeTitle(paragraph):
    """takes a paragraph of text, removes the starting """
    try:
        i = paragraph.index(':')
        paragraph = paragraph[i+1:]
    #    print("Chopped paragraph == " + paragraph[:15])
    except:
        print("Error == " + paragraph)
    return paragraph

def createSpaces(paragraph):
    """Takes a paragraph, adds spaces where they should have been. Solves issues
    surrounding isolating the title of the attribute"""
    paragraph = paragraph.replace('\xa0','')
    paragraph = paragraph.replace(':A',': A')
    paragraph = paragraph.replace(':T',': T')
    paragraph = paragraph.replace(':<',': <')
    paragraph = paragraph.replace(':N',': N')
    return paragraph

def getTitle(paragraph):
    """Takes a paragraph, isolates the first word (ie, the title of the desired 
    attribute), removes the colon, and returns the isolated title."""
    words = paragraph.split(" ")
    first_word = words[0]
    attr_name = first_word.replace(':','').lower()
    return attr_name

def getInfo(desc, ftr):
    """takes feature description, pulls out info"""
    desc = desc.replace('<br><br>','\n')
    paragraphs = desc.split('\n')
    final_lines = ""
    attr_dict = {}
    i = 0
    try:
        for paragraph in paragraphs:
            print("Processing paragraph #" + str(i))
            paragraph = createSpaces(paragraph)
            i += 1
            attr_name = getTitle(paragraph)
            paragraph = removeTitle(paragraph)
            
            attr_dict[attr_name] = paragraph
            try:
                indx = flds.indexOf(attr_name)
            except:
                indx = flds.indexOf('challenge')
            attrs = {indx: paragraph}
            pr.changeAttributeValues({ftr.id():attrs})
    except:
        print("Error on line #" + i)

def createFields(lyr):
    """takes the current layer, adds the fields needed for processing"""
    print("Creating fields")
    fld1 = QgsField("points", QVariant.String, len=100)
    fld2 = QgsField("challenge", QVariant.String, len=300)
    fld3 = QgsField("information", QVariant.String, len=300)
    fld4 = QgsField("note", QVariant.String, len=150)
    fld5 = QgsField("bonus", QVariant.String, len=150)
#    fld6 = QgsField("bonus_points", QVariant.Double, len=2)
    pr.addAttributes([fld1, fld2, fld3, fld4, fld5])
    lyr.updateFields()
    print("Fields updated")

def deleteFields(lyr):
    """takes the current layer, deletes default fields from KML conversion plugin"""
    print("Deleting unwanted fields")
    flds = ['folders', 'altitude', 'alt_mode', 'time_begin', 'time_end', 'time_when']
    i_list = []
    for fld in flds:
        i = lyr.fields().indexFromName(fld)
        i_list.append(i)
    pr.deleteAttributes(i_list)
    lyr.updateFields()
    
def main():
    """the main func of the application"""
    mc = iface.mapCanvas()
    lyr = mc.currentLayer()
    lyr.startEditing()
    createFields(lyr)
    deleteFields(lyr)
    for ftr in lyr.getFeatures():
        sortFeatures(ftr)
main()