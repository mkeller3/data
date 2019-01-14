import psycopg2

#db settings
conn = psycopg2.connect("host=localhost dbname=gisdata user=postgres password=P0stgr3s")

def boundingBox(table):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT ST_SetSRID(ST_Extent("+table+".geom),4326) FROM "+table+"as geom;")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def buffer(table, distance):
    distance = distance / 68.703
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '"+table+"'")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    cols = ""
    for col in userData:
        if col[0] != "geom":
            cols = cols + " "+table+"."+col[0]+","
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT"+cols+"ST_Buffer("+table+".geom, "+str(distance)+") as geom FROM "+table)
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()  
    return len(userData)

def centerOfData(table):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT ST_Centroid(st_union("+table+".geom)) as geom FROM "+table)
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()  
    return len(userData)

def centerOfPolygons(table):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '"+table+"'")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    cols = ""
    for col in userData:
        if col[0] != "geom":
            cols = cols + " "+table+"."+col[0]+","
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT"+cols+"ST_Centroid("+table+".geom) as geom FROM "+table)
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()  
    return len(userData)

def countPointsWithinPolygons(points,polygons):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '"+polygons+"'")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    cols = ""
    for col in userData:
        if col[0] != "geom":
            cols = cols + " "+polygons+"."+col[0]+","
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("CREATE TEMP TABLE "+polygons+"_join as SELECT "+polygons+".gid, count(*) points_within FROM "+points+", "+polygons+" WHERE ST_Contains("+polygons+".geom, "+points+".geom) GROUP BY "+polygons+".gid ORDER BY points_within desc;")
    conn.commit()
    cursor.close()
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT "+cols+polygons+"_join.points_within, "+polygons+".geom FROM "+polygons+", "+polygons+"_join WHERE "+polygons+".gid = "+polygons+"_join.gid;")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()    
    conn.close()  
    return len(userData)

def dissolveByAttribute(table,column):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT counties."+column+", ST_Union(geom) FROM "+table+" GROUP BY "+column+";")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def dissolveTable(table):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT ST_Union(geom) FROM "+table+";")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def findWithinDistance(table,lat,lng,distance):
    distance = distance * 1609.34
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table+" WHERE ST_DWithin(geom, ST_MakePoint("+str(lng)+","+str(lat)+")::geography, "+str(distance)+"); ")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def selectInside(withinTable,insideTable):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '"+insideTable+"'")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    cols = ""
    for col in userData:
        if col[0] != "geom":
            cols = cols + " "+insideTable+"."+col[0]+","
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT"+cols+insideTable+".geom FROM "+withinTable+", "+insideTable+" WHERE ST_Intersects("+insideTable+".geom, "+withinTable+".geom)")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def calculateAreaLength(table):
        test = 'hi'
        return(test)

def concaveHull(table):
        cursor = conn.cursor()
        cur = conn.cursor()
        cur.execute("SELECT ST_ConcaveHull(("+table+".geom)) as geom FROM "+table)
        userData = cur.fetchall()
        conn.commit()
        cursor.close()
        conn.close()  
        return len(userData)

def pointToPointsDistance(table,lat,lng):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '"+table+"'")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    cols = ""
    for col in userData:
        if col[0] != "geom":
            cols = cols + " "+table+"."+col[0]+","
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT"+cols+"ST_Distance("+table+".geom,ref.geom)*0.000621371 As distance FROM "+table+", (SELECT ST_Point("+str(lng)+","+str(lat)+")::geography) As ref(geom)")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()  
    return len(userData)



