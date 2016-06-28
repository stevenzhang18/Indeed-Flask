
import codecs, csv

################################################################
################################################################

# Is this the Production Version?
ProductionVersion = True

################################################################
################################################################

if ProductionVersion:
    CityNamesFN =      'APP_DATA/CityData.csv'
    NeutWordsFN =      'APP_DATA/TopWords215.csv'
    CityFolderPrefix = 'APP_DATA/CITY_DATA/'

else:
    CityNamesFN =      'DATA/CityData.csv'
    NeutWordsFN =      'DATA/TopWords215.csv'
    CityFolderPrefix = 'DATA/CITY_VS2/'

################################################################
################################################################

def readcsv(filepath):
    data = []
    OF = codecs.open(filepath,'r', 'cp1252')
    for row in csv.reader(OF, dialect='excel', skipinitialspace=True):
        row = [str(a).strip() for a in row]
        data.append(row)
    return data

# A Counter mechanism to keep track of
# all incidences of a vote.
class Tabulator2:
    def __init__(self):
        self.tab = {}
        self.SUM = 0

    # Adds multiple counts of one name to the tabulator:
    def add(self,name,Num=1.0):
        self.SUM += Num
        if name in self.tab: self.tab[name]+= Num
        else:                self.tab[name] = Num

    # Returns the number of counted instances of 'name':
    def num(self,name):
        if name in self.tab: number = self.tab[name]
        else:                number = 0
        return number

    # Returns the name of the item with the highest count:
    def best(self):
        name = 0
        topV = 0
        for a in self.tab:
            val = self.tab[a]
            if val > topV:
                topV = val
                name = a
        return name

    # Returns list of accounts sorted by
    # highest count to lowest.
    def results(self,Min=None):
        Results = []
        for a in self.tab:
            val = self.tab[a]
            Results.append([val,a])
        Results.sort()
        Results.reverse()
        if Min: Results = [a for a in Results if a >= [Min,'']]
        return Results

    # Returns all account names:
    def accounts(self):
        return sorted([a for a in self.tab])

    # Returns List of names of top N accounts:
    def topN(self,N=3):
        tops = nlargest(N, list(self.tab.items()), key=itemgetter(1))
        return [a[0] for a in tops]

    def export(self,filename,Min=None):
        Results = self.results(Min)
        writecsv(filename,Results)


################################################################
################################################################


def SimpleLocation(location):
    L = [a for a in location if a.isalpha()]
    return ''.join(L)

def FormatWords(Lines):
    Words = []
    for line in Lines:
        if len(line)<1: continue
        words = line.replace('\\n',' ').replace('\n',' ').replace('\t',' ').split(' ')
        for word in words:
            if len(word)<1 or len(word)>20: continue
            if len(word)==1:
                if word in 'Rr': Words.append('R')
                else: continue
            try: x = float(word)
            except:
                word=word.upper()
                if word in NeutralList: continue
                Words.append(word)
    Words = sorted(set(Words))
    return Words


def RankCities(words):
    Results = []
    for city in TDict:
        T = TDict[city]
        scores = []
        for word in words:
            score = T.num(word)
            scores.append(score)
        city_score = sum(scores)/float(len(scores))
        Results.append([city_score,city])
    Results.sort()
    Results.reverse()
    return Results


# Input a single string of text.
# Outputs a dictionary of top ten cities:
def MasterFunc(text):
    global TDict
    words = FormatWords([text])
    Top10 = RankCities(words)[:10]
    Results = {}

##    rank=0
##    for r in Top10:
##        rank+=1
##        simple = r[1]
##        CityName = NameDict[simple]
##        Results[rank] = CityName

    Results = ['']+[a[1] for a in Top10]
    return Results


################################################################
################################################################

#print 'The data is loading...'

fn   = NeutWordsFN
data = readcsv(fn)
NeutralList = [a[0] for a in data]

fn   = CityNamesFN
data = readcsv(fn)
locations = sorted([r[1] for r in data[1:]])

Simples = []
NameDict= {}
for loc in locations:
    simple = SimpleLocation(loc)
    Simples.append(simple)
    NameDict[simple]=loc
    NameDict[loc]=simple

TDict = {}
for name1 in Simples:
    fn = CityFolderPrefix+name1+' vs MASTER.csv'
    try: data = readcsv(fn)
    except: continue
    T=Tabulator2()
    for r in data[25:-25]:
        value = float(r[0])
        word = r[1]
        T.add(word,value)
    TDict[name1] = T


################################################################
################################################################

#print 'The calculation is begining.'

if not ProductionVersion:

    text = 'Python \n java \t science data'
    results = MasterFunc(text)
    Keys = sorted(results)
    for Key in Keys:
        cityname = results[Key]
        print Key,':',cityname

#print 'Program Done.'


################################################################
################################################################
