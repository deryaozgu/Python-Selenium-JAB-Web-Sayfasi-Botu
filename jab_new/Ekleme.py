class EEkleme:

    def __init__(self,Article,Brand,Number,Colour_Variations,Quality,Material,Instructions,Width_Length,Design,images):
        self.Article=Article
        self.Brand=Brand
        self.Number=Number
        self.Colour_Variations=Colour_Variations
        self.Quality=Quality
        self.Material=Material
        self.Instructions=Instructions
        self.Width_Length=Width_Length
        self.Design=Design
        self.images=images
    def printDetay(self):
        for key in self.__dict__:
            print(key,":",self.__dict__[key])