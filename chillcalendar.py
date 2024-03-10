import calendar
from datetime import date
import random
import collections
import csv
import pandas
from random import shuffle
import sys
    
inputarguments = sys.argv

inputyear = int(inputarguments[1])
inputmonth = int(inputarguments[2])
inputguides = list(inputarguments[3:])

# define classe tourmonth
class tourmonth():
    def __init__(self, year, month, listguides, language):
        self.language = language
        self.year = year
        self.month = month
        self.daysinmonth = calendar.monthrange(self.year, self.month)[1]
        self.howmanyguides = len(listguides)
        self.averagetours = self.daysinmonth * 2 // self.howmanyguides
        shuffle(listguides)
        self.minimumtours = 0
        
        while self.minimumtours < self.averagetours:

            self.guides = {"listguides" : listguides, "daysinarow" : [], "alreadyonthisday" : [],
                           "usedinwhilemakemonth" : []}
            for _ in range(0, self.howmanyguides):
                self.guides["daysinarow"].append(0) 
                self.guides["alreadyonthisday"].append(False)
                self.guides["usedinwhilemakemonth"].append(False)
    
            # equality counter for: tours, mornings, afternoons, mondays, tuesdays, ..., sundays
            self.guidescount = pandas.DataFrame({guide: 10 * [0] for guide in self.guides["listguides"]},
                                                index = ['Tours', 'Morning', 'Afternoon', 'Monday', 'Tuesday',
                                                         'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
            
            self.tours = {"daysofmonth" : [], "weekday" : [], "morningafternoon" : [], "guidefortour" : []}
            for day in range(1, self.daysinmonth+1):
                self.tours["daysofmonth"].append(day)
                self.tours["daysofmonth"].append('')

                # day of the week plus 2: so monday is 2 and sunday is 8
                self.tours["weekday"].append(date(year, month, day).weekday()+2)
                self.tours["weekday"].append('')
                self.tours["morningafternoon"].append("am")
                self.tours["morningafternoon"].append("pm")
    
            for day in range(0,len(self.tours["daysofmonth"]),2):
                self.guides["alreadyonthisday"] = [False] * self.howmanyguides
                for ampm in range (0,2):

                    guidefound = False
                    counter = 0
                    while not guidefound and counter < 500:
                        counter += 1
                        randomguide = random.randrange(0,self.howmanyguides,1)

                        guidescountcuttours = self.guidescount.loc['Tours']
                        if ampm == 0:
                            guidescountcutampm = self.guidescount.loc['Morning']
                        else:
                            guidescountcutampm = self.guidescount.loc['Afternoon']

                        minguidepretours = guidescountcuttours[guidescountcuttours == guidescountcuttours.min()].dropna(0)
                        guidescountcutampm = guidescountcutampm[guidescountcutampm == guidescountcutampm.min()].dropna(0)
                        minguide = list(minguidepretours.keys()) + list(guidescountcutampm.keys())
   
                        if not self.guides["alreadyonthisday"][randomguide] and self.guides["daysinarow"][randomguide] <= 3 and self.guidescount[self.guides["listguides"][randomguide]][0] <= self.averagetours and self.guides["listguides"][randomguide] in minguide:# and not self.guides["usedinwhilemakemonth"][randomguide]:

                            #add guide to tour
                            self.tours["guidefortour"].append(self.guides["listguides"][randomguide])
                            
                            #guide has already been used for today? true/false
                            self.guides["alreadyonthisday"][randomguide] = True
                                                       
                            #how many days in a row?
                            self.guides["daysinarow"][randomguide] += 1
                            
#                            #already used in this while iteration?
#                            self.guides["usedinwhilemakemonth"][randomguide] = True
                            
                            #counting: tours, morning or afternoon and weekdays for each guide
                            self.guidescount[self.guides["listguides"][randomguide]][0] += 1
                            self.guidescount[self.guides["listguides"][randomguide]][1+ampm] += 1
                            self.guidescount[self.guides["listguides"][randomguide]][self.tours["weekday"][day]+1] += 1
                            
                            guidefound = True
                        
                        elif self.guides["daysinarow"][randomguide] > 3:
                            self.guides["daysinarow"][randomguide] = 0
                            
            
            self.minimumtours = self.guidescount.min(1)[0]

        print(self.year,self.month)
        print(pandas.DataFrame(self.guidescount))#,'\n',dict(collections.Counter(self.tours["guidefortour"])))
         
    def addguidetotour(self, guide, day, ampm):
        self.tours["guidefortour"][day * 2 - ampm] = guide # ampm = 2 if morning and 1 if afternoon

    def gettours(self):
        return self.tours

    def getguides(self):
        return self.guides

    def gettourguides(self):
        return self.tours["guidefortour"]

    def info(self):
        print([self.language, self.year, self.month, self.tours])
        print("\n",self.year, self.month, "\n")
        for i in range(0,len(self.tours["daysofmonth"])):
            if (i % 2 == 0):
                print("-"*40,"\r", sep ="")
                print(self.tours["daysofmonth"][i], self.tours["weekday"][i], self.tours["morningafternoon"][i], self.tours["guidefortour"][i], sep = "\t")
            else:
                print(" ", " ", self.tours["morningafternoon"][i], self.tours["guidefortour"][i], sep = "\t")
    
 
    def count(self):

        return dict(collections.Counter(self.tours["guidefortour"]))

    def exportmonthcsv(self, filename):

        self.filename = str(filename)

        with open(self.filename, 'w', newline='') as myfile:

            myfile.write('"' + str(self.year) + '","' + str(self.month) + '"\n')
            wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
            wr.writerow(self.tours["daysofmonth"])
            wr.writerow(self.tours["weekday"])
            wr.writerow(self.tours["morningafternoon"])
            wr.writerow(self.tours["guidefortour"])

        with open(self.filename[:-4] + "table.csv", "w", newline="") as myfile:

            guidescountDF = pandas.DataFrame(self.guidescount)
            guidescountDF.to_csv(myfile)

    def exportmonthcsv2(self, filename):

        weekdaystart = (self.tours["weekday"][0] - 2)
        
# for testing
#        weekdaystart = 0
#        self.tours["guidefortour"] = [format(x,'02d') for x in list(range(1,self.daysinmonth*2+1,1))]
         
        oddevenday = (weekdaystart // 2) * 2

        self.filename = str(filename)
        with open(self.filename, 'w', newline = '') as calendarcsvfile:
            calendarcsvfile.write(str(self.year) + "/" + str(self.month) + ",Seg,Ter,Qua,Qui,Sex,Sab,Dom" + "\n")
            
            calendarcsvfile.write(" ," + weekdaystart * " ," + ",".join(map(str,self.tours["daysofmonth"][0:13-oddevenday-weekdaystart:2])) +  "\n")
            calendarcsvfile.write("AM," + weekdaystart * " ," + ",".join(self.tours["guidefortour"][0:13-oddevenday-weekdaystart:2]) +  "\n")
            calendarcsvfile.write("PM," + weekdaystart * " ," + ",".join(self.tours["guidefortour"][1:13+1-oddevenday-weekdaystart:2]) +  "\n")
            
            for day in range((7-weekdaystart)*2,2*self.daysinmonth+1,14):
                calendarcsvfile.write(" ," + ",".join(map(str,self.tours["daysofmonth"][day:day+14:2])) +  "\n")
                calendarcsvfile.write("AM," + ",".join(self.tours["guidefortour"][day:day+14:2]) +  "\n")
                calendarcsvfile.write("PM," + ",".join(self.tours["guidefortour"][day+1:day+1+14:2]) +  "\n")
            
        calendardf = pandas.read_csv(self.filename)
        with open('calendar.html', 'w', newline = '') as calendarhtmlfile:
            calendarhtmlfile.write(calendardf.fillna(' ').to_html(justify="center",border=1,index=False,col_space=12))

#inputyear = 2018
#inputmonth = 3
#inputguides = ['Jose','Miguel','Rafael','Rafa','Nuno','Gabi','Pedro','Luis','Ines','Ana']

toursmonth = tourmonth(inputyear, inputmonth, inputguides, 'en')
toursmonth.exportmonthcsv('tourslist_flat.csv')
toursmonth.exportmonthcsv2('tourslist.csv')


#m201804 = tourmonth(2018, 4, guias, 'en')
#m201804.exportmonthcsv2('m2018.csv')
#
#m201803 = tourmonth(2018, 5, guias, 'en')
#m201803.exportmonthcsv2('m2018.csv')
#
#m201804 = tourmonth(2018, 6, guias, 'en')
#m201804.exportmonthcsv2('m2018.csv')
#
#m201803 = tourmonth(2018, 7, guias, 'en')
#m201803.exportmonthcsv2('m2018.csv')
#
#m201804 = tourmonth(2018, 8, guias, 'en')
#m201804.exportmonthcsv2('m2018.csv')
#
#m201803 = tourmonth(2018, 9, guias, 'en')
#m201803.exportmonthcsv2('m2018.csv')
#
#m201804 = tourmonth(2018, 10, guias, 'en')
#m201804.exportmonthcsv2('m2018.csv')
#
#m201803 = tourmonth(2018, 11, guias, 'en')
#m201803.exportmonthcsv2('m2018.csv')
#
#m201804 = tourmonth(2018, 12, guias, 'en')
#m201804.exportmonthcsv2('m2018.csv')