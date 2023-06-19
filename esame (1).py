class ExamException(Exception):

    pass

class CSVTimeSeriesFile:
  def __init__(self,name):
     
      self.name = name

  def get_data(self):
    
      time_series = []

      try:
          my_file = open(self.name, 'r') #leggo il file
      except:
          raise ExamException('Errore in apertura del file') #se non viene letto alzo una eccezione

      if(my_file.readline() == ''): #provo a leggere una riga del file
          raise ExamException('Il file è vuoto') #se il file è vuoto alzo una eccezione

      for line in my_file:
          elements = line.strip('\n').split(',') #divido la riga in due parti, la data e il valore dei passeggeri

          if elements[0] != 'date' : #se la prima parte è diversa da date procedo
              try: #provo a divere la data in anni e mesi e convertirli ad int, se non riesco salto la riga
                  separate_data = elements[0].split('-') 
                  separate_data[0] = int(separate_data[0])
                  separate_data[1] = int(separate_data[1])

              except:
                  continue

              if not isinstance(separate_data[0], int): #se l'anno non è un intero salto la riga
                  continue
        
              if not isinstance(separate_data[1], int): #se il mese non è un intero salto la riga
                  continue
        
              if not 1 <= separate_data[1] <= 12: #se il mese non è compreso tra 1 e 12 salto una riga
                  continue
              if len(time_series)>0 and elements[0]==time_series[-1][0]: #se ci sono date duplicate alzo un'eccezione
                 raise ExamException('Due date sono uguali')
              if len(time_series)>0 and separate_data[0] < int(time_series[-1][0].split('-')[0]): #se ci sono anni non in ordine alzo una eccezione
                 raise ExamException('Gli anni non sono in ordine')

              if len(time_series)>0 and separate_data[0]==int(time_series[-1][0].split('-')[0]) and separate_data[1]<int(time_series[-1] [0].split('-')[1]): #se ci sono mesi non in odrine alzo una eccezione
                 raise ExamException('I mesi non sono in ordine')
              
              try:
                  elements[1] = int(elements[1]) #converto il valore dei passeggeri ad intero, se non riesco salto la riga
              except:
                  continue

              if(elements[1]<=0): #salto la riga se il numero dei passeggeri è <=0
                  continue
              time_series.append(elements) #aggiungo il valore alla lista se ha passato tutti i test 
      my_file.close() #chiudo il file
      if time_series==[]: #se la lista è vuota alzo una eccezione
        raise ExamException('La lista è vuota')
      return time_series #torno la lista time_series
 
  
def compute_avg_monthly_difference(time_series, first_year, last_year):

    years=[] #inizializzo una lista vuota che verrà utilizzata per memorizzare gli anni estratti dalla serie temporale
    for line in time_series:
        date=line[0] #accedo alla prima colonna 
        year=date.split('-')[0] #viene estratto il primo elemento della lista, quindi l'anno
        years.append(year) #l'anno estratto viene aggiunto alla lista years e si ripete il processo

    if first_year not in years or last_year not in years: #controllo se first_year e last_year non sono nell'intervallo
        raise ExamException('Range non valido') #se uno dei due non è nell'intervallo alzo una eccezione
        
    
    first_year = int(first_year) #converto first_year da stringa a intero
    last_year = int(last_year) #converto last_year da string a intero
    

    if first_year > last_year: #se l'anno iniziale è piu grande di quello finale alzo una eccezione
       raise ExamException('Range non valido')
        
            
    annual_passengers = [] #inizializzo una lista vuota per memorizzare i passeggeri annuali per ciascun anno nell'intervallo richiesto
    for i in range(last_year - first_year + 1): #itero sul range last_year - first_year + 1
        annual_passengers.append([]) #si crea una nuova lista vuota che viene aggiunta come elemento alla lista vuota annual_passengers
    
    for line in time_series:
        date = line[0] #estraggo la data della riga
        passengers = line[1] #estraggo il numero di passeggeri della riga
        year, month = map(int, date.split('-')) # Utilizzo la funzione map(int, date.split('-')) per applicare la funzione int a ciascun elemento ottenuto dalla suddivisione della data
        
        if first_year <= year <= last_year: #verifico se l'anno estratto appartiene all'intervallo
            annual_passengers[year - first_year].append(int(passengers)) #year-first_year calcola l'indice corrispondente all'anno all'interno di annual_passengers poi aggiungo il numero di passeggeri alla lista corrispondente assicurandomi sia un valore intero
    
    if not any(annual_passengers): #verifico se ci sono elementi nella lista
        raise ExamException('Non ci sono dati nella lista') #se non ci sono elementi alzo una eccezione
    
    media_passeggeri = [] #inizializzo una lista vuota che conterrà le medie calcolate
    
    for i in range(12): #itero su ogni mese nell'anno e lo utilizzo per calcolare le medie delle differenze mensili dei passeggeri.
        somma = 0 #inizializzo variabile somma che conterrà la somma delle differenze mensili dei passeggeri per tutti gli anni
        
        for year in range(len(annual_passengers) - 1): #metto il -1 perchè dovendo poi fare [year+1], sforerei i limiti della lista
            somma += annual_passengers[year + 1][i] - annual_passengers[year][i] #calcolo la differenza mensile dei passeggeri tra l'anno successivo e quello corrente per il mese 'i'
          
          
        media_passeggeri.append(somma / (last_year-first_year)) #calcolo la media per il mese corrente per il numero di anni dell'intervallo
    
    return media_passeggeri #ritorno la lista


#time_series_file=CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()
#print(time_series)
#differenza_media=compute_avg_monthly_difference(time_series,"1949","1951")
#print(differenza_media)