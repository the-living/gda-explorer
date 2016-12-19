import rhinoscriptsyntax as rs

# GH Python component for saving generative plan layouts as
# SVG for display on web-based design explorer

# GH INPUTS
# "fp": (String) Directory location for output
# "uid": (Int) Unique Design ID index for file naming
# "rotate": (Boolean) Toggle to rotate plan 90deg
# "pad": (Int) Edge padding around SVG contents
# "base_crv": (Curve List) Boundary & column curves (0,1: Boundary curves / 2,n: Column Curves)
# "nbhd_crv": (Curve List) Neighborhood boundary curves
# "amen_crv": (Curve List) Amenity bar boundary curves
# "desk_crv": (Curve List) Desk boundary curves

def getOrigin(r, c):
    bb = rs.BoundingBox(c)
    if r:
        return bb[2]
    else:
        return bb[3]

def getRelDim(o,p,r):
    #print p
    if r:
        #print (o.Y - p.Y, o.X - p.X)
        return (o.Y - p.Y, o.X - p.X)
    else:
        #print (p.X-o.X, o.Y-p.Y)
        return (p.X-o.X, o.Y-p.Y)

def makePolygon(crv, domClass, o, stroke, fill):
    #polgons are generated as SVG paths
    #<path d="M 0 0 L 100 0 L 100 100 L 0 100 Z"></path>
    #polygon points are formatted as a single string under the attribute "d"
    #M precedes the first coordinate
    #L precedes following coordinates (using a lower-case "l" denotes relative position (not absolute) to first coordinate)
    #Z ends polygon
    pts = rs.CurvePoints(crv)
    pts = [ getRelDim(o,p,rotate) for p in pts ]
    pts = [ "%f %f"%(p[0]+pad, p[1]+pad) for p in pts ]
    pt_str = " L ".join(pts)
    return "<path d=\"M %s\" stroke=\"%s\" fill=\"%s\" stroke-width=\"1px\"></path>" %(pt_str,stroke,fill)

def makeGroup(id_name):
    return "<g id=\"%s\">" %(id_name)

def closeGroup():
    return "</g>"

def getBounds( r, c ):
    bb = rs.BoundingBox(c)
    w = abs(bb[0].X - bb[1].X)
    h = abs(bb[0].Y - bb[2].Y)
    if r:
        return "width=\"%f\" height=\"%f\"" %(h + pad*2,w + pad*2)
    else:
        return "width=\"%f\" height=\"%f\"" %(w + pad*2,h + pad*2)

fileout = "%sd_%d.svg" %(fp,uid)
lines = []
with open(fileout, mode='wb') as f:
    size = getBounds(rotate,base_crv)
    origin = getOrigin(rotate,base_crv)
    #create SVG file contents with sizing and namespace links
    lines.append( "<svg %s xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" version=\"1.1\">" %(size) )

    #add background mask
    lines.append(makeGroup("crv-background"))
    for c in base_crv[:2]:
        lines.append(makePolygon(c, "plan-bg", origin, "none","white"))
    lines.append(closeGroup())

    #add nbhd curves
    lines.append(makeGroup("crv-nbhd"))
    for n in nbhd_crv:
        lines.append(makePolygon(n,"plan-nbhd", origin, "#DD2222","none"))
    lines.append(closeGroup())

    #add amen polygons
    lines.append(makeGroup("crv-amen"))
    for a in amen_crv:
        lines.append(makePolygon(a,"plan-amen",origin,"none","#2288CC"))
    lines.append(closeGroup())

    #add desk polygons
    lines.append(makeGroup("crv-desk"))
    for d in desk_crv:
        lines.append(makePolygon(d,"plan-desk",origin,"gray","white"))
    lines.append(closeGroup())

    #add boundary curves
    lines.append(makeGroup("crv-base"))
    for c in base_crv[:2]:
        lines.append(makePolygon(c, "plan-bound", origin, "black","none"))
    for c in base_crv[2:]:
        lines.append(makePolygon(c, "plan-col", origin, "black", "white"))
    lines.append(closeGroup())

    #close svg tag
    lines.append("</svg>")
    #write to file
    f.writelines(lines)

f.close()
