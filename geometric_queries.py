import psycopg2

#db settings
conn = psycopg2.connect("host=localhost dbname=gisdata user=postgres password=P0stgr3s")

def geometricSelection(table, geometricData):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table+" WHERE ST_Intersects("+table+".geom, ST_SetSRID(ST_GeomFromText('POLYGON(("+geometricData+"))'),4326));")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def textSelection(table, whereClause):
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table+" WHERE "+whereClause)
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)

def geometricAndTextSelection(table,geometricData,whereClause)
    cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table+" WHERE ST_Intersects("+table+".geom, ST_SetSRID(ST_GeomFromText('POLYGON(("+geometricData+"))'),4326)) AND "+whereClause+";")
    userData = cur.fetchall()
    conn.commit()
    cursor.close()
    conn.close()   
    return len(userData)


#print textSelection('states',"state_name = 'Texas'")    
#print geometricSelection('counties','-102.81006 35.44277, -100.67871 35.38905, -100.70068 33.52308, -102.83203 33.59632, -102.81006 35.44277')    
