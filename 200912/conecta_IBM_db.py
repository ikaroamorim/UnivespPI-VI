import ibm_db


class conecta: 
    
    def __init__(self,id,nome,compra,preco):
        self.id=id
        self.nome=nome
        self.compra=compra
        self.preco=preco
    
    
        #Replace the placeholder values with your actual Db2 hostname, username, and password:
        dsn_hostname = "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net" # e.g.: "dashdb-txn-sbox-yp-dal09-04.services.dal.bluemix.net"
        dsn_uid = "mxb40007"        # e.g. "abc12345"
        dsn_pwd = "z887bnjptc6sd^p0"      # e.g. "7dBZ3wWt9XN6$o0J"
        
        dsn_driver = "{IBM DB2 ODBC DRIVER}"
        dsn_database = "BLUDB"            # e.g. "BLUDB"
        dsn_port = "50000"                # e.g. "50000" 
        dsn_protocol = "TCPIP"            # i.e. "TCPIP"
        
        dsn = (
            "DRIVER={0};"
            "DATABASE={1};"
            "HOSTNAME={2};"
            "PORT={3};"
            "PROTOCOL={4};"
            "UID={5};"
            "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)
        
        #print the connection string to check correct values are specified
        print(dsn)
        
        #DO NOT MODIFY THIS CELL. Just RUN it with Shift + Enter
        #Create database connection
        
        try:
            conn = ibm_db.connect(dsn, "", "")
            print ("Connected to database: ", dsn_database, "as user: ", dsn_uid, "on host: ", dsn_hostname)
        
        except:
            print ("Unable to connect: ", ibm_db.conn_errormsg() )
        
    
       
        #Apaga a tabela PI_7sem
        #dropQuery = "drop table PI_7sem"
            
        #Executa o statement
        #ibm_db.exec_immediate(conn, dropQuery)
    
    
        #Construindo a tabela. Caso haja mudanças na tabela é aqui que que deve-se alterar
        #createQuery = "create table PI_7sem(ID VARCHAR(40) NOT NULL, Nome VARCHAR(20),Compra VARCHAR(20), Valor DOUBLE)"
        #Não está como PRIMARY KEY    
        
        #ibm_db.exec_immediate(conn,createQuery)
        
        
        
        data =  (self.id, self.nome, self.compra, self.preco)
              
        format_str = "insert into PI_7sem values ('{id_pi}', '{name}', '{comp}', '{value}')"
        insertQuery = format_str.format(id_pi=data[0], name=data[1], comp=data[2],  value = data[3])
                                            
        ibm_db.exec_immediate(conn, insertQuery)
        
                
        
        selectStmt = ibm_db.exec_immediate(conn, "SELECT * FROM PI_7sem")
        
        slct=ibm_db.fetch_tuple(selectStmt)
        
           
        
        n=0
        selecao=[]
        while( slct ):
           
            selecao.append(slct)
            slct = ibm_db.fetch_tuple(selectStmt)
            n=n+1
        
        
        self.selecao=selecao
        
        ibm_db.close(conn)  
        
  
        












