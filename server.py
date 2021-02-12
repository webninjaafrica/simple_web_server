import socket
import os
import datetime
# simple http web server using TCP/IP
# coded by KELVIN MWANGI MAGOCHI / admin@webninjaafrica.com / +254111560417
# web/ python / php developer
# This is an application to demonstrate use of http with python inbuilt library -sockets
# the server comprises of two classes namely http and web_server classes

class http:
    def __init__(self,http_code="200",status_text="ok",http_version="HTTP/1.0"):
        self.http_code=http_code
        self.status_text=status_text
        self.http_version=http_version
        self.filesize=0
        self.header_text=str(self.http_version)+" "+str(self.http_code)+" "+str(self.status_text)+"\r\n"
    def add_header(self,name,value):
        self.header_text+=str(name)+": "+str(value)+"\r\n"
        return self.header_text
    def end_header(self,connection="close"):
        self.header_text+="connection: "+str(connection)+"\r\n\r\n"
        return self.header_text.encode()
    def add_html(self,html):
        self.header_text+=str(html)
        return self.header_text.encode()
    def redirect(location):
        app=http("302","Moved")
        app.add_header("Location",str(location))
        return (app.end_header()).encode()

class web_server(http):
    def __init__(self):
        super().__init__()
        self.app=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.app.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        self.clients_in_wait=10
        self.data=""

    def contentType(self,file):
        cont="text/html"
        if file.endswith("jpg"):
            cont="image/jpg"
        elif file.endswith("JPG"):
            cont="image/jpg"
        elif file.endswith("png"):
            cont="image/png"
        elif file.endswith("gif"):
            cont="image/gif"
        elif file.endswith("mp4"):
            cont="video/mp4"
        elif file.endswith("3gp"):
            cont="video/3gp"
        elif file.endswith("json"):
            cont="application/json"
        elif file.endswith("xml"):
            cont="application/xml"
        else:
            cont="text/html"
        return cont
    def file_content(self,filepath):
        try:
            w=open(filepath,"rb")
            data=w.read()
            w.close()
        except Exception as e:
            data=str(e)
        self.filesize=len(data)
        return data
    
    def file_exists(self,filepath):
        try:
            w=open(filepath,"rb")
            data=1
            w.close()
        except Exception as e:
            data=0
        return data
    def request(self,reqq,fomart="utf8"):
        req=reqq.decode(fomart)
        meta={"REQUEST_METHOD":"","FILENAME":"","GET":[],"POST":[],"COOKIE":[],"SESSION":[],"FILES":[]}
        get_meta=req.split("\r\n")[0].split(" ")
        meta["REQUEST_METHOD"]=get_meta[0]
        fn=""
        if get_meta[1]=="/" or get_meta[1]==" " or get_meta[1]=="":
           meta["FILENAME"]="index.html"
        else:
            meta["FILENAME"]=get_meta[1].lstrip("/")
        
        if "?" in meta["FILENAME"]:
                striped_file=get_meta[1].lstrip("/").split("?")
                meta["FILENAME"]=striped_file[0]
                if meta["FILENAME"]=="/" or meta["FILENAME"]==" " or meta["FILENAME"]=="":
                   meta["FILENAME"]="index.html"
                meta["GET"]={}
                if(len(striped_file) >1):
                    s=striped_file[1].split("&")
                    for chip in s:
                        hay=chip.split("=")
                        if len(hay) >1:
                            key=hay[0]
                            value=hay[1]
                        else:
                            key=hay[0]
                            value=""
                        meta["GET"][key]=value
        if get_meta[0]=="POST":
            raw_post=req.split("\r\n\r\n")
            if len(raw_post) >1:
                meta["POST"]={}
                data=raw_post[1].split("&")
                for chip2 in data:
                    hay=chip2.split("=")
                    key=hay[0]
                    value=""
                    if len(hay)>1:
                        value=hay[1]
                    meta["POST"][key]=value

        other_info=req.split("\r\n")
        for raw in range(len(other_info)):
            haystack=other_info[raw].split(":")
            
            if len(haystack)>1:
                #print("\n")
                #print(haystack)
                #print("\n")
                try:
                    meta[str(haystack[0]).strip()]=str(haystack[1]).strip()
                except:
                    pass
            else:
                 pass
            
        print(meta)
        print("\n")
        return meta
    def deploy(self,host='0.0.0.0',port=3030):
        self.app.bind((str(host),port))
        self.app.listen(self.clients_in_wait)
        print("eagle server v 1.0 started\nlistening....")
        while 1:
                cs,addr=self.app.accept()
                
                recv=cs.recv(1024*1000)
                if recv:
                    req=self.request(recv)
                    
                    if self.file_exists(req["FILENAME"]):
                        self.http_code="200"
                        self.status_text="ok"
                        self.add_header("Content-Type",self.contentType(req["FILENAME"]))
                        self.end_header()
                        content=self.add_html(self.file_content(req["FILENAME"]))
                        
                    else:
                        self.http_code="404"
                        self.status_text="NOT FOUND"
                        self.add_header("Content-Type","text/html")
                        self.end_header()
                        content=self.add_html("<html><head><title>ERROR 404</title></head><body>404 FILE NOT FOUND!</body></html>")
                        
                    cs.sendall(content)
                    print(str(datetime.datetime.now())+"/ "+req["FILENAME"]+" | GOT CONNECTION FROM: "+str(addr[0])+" @"+str(addr[1]))
                else:
                    pass
                
                
        self.app.close()
        
s=web_server()
s.deploy("localhost",2000)
