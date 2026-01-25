"""import inkex

class MassInk(inkex.EffectExtension):
    def effect(self):
        inkex.errormsg("MassInk is running!")

if __name__ == "__main__":
    MassInk().run()
"""
"""import inkex

class MassInk(inkex.Effect):

    def effect(self):
        sel = list(self.svg.selection.values())

        inkex.utils.debug(self.options.strings)

        if sel:
            inkex.utils.debug(f"Selected type: {type(sel[0])}")

        inkex.utils.debug("Strings:")
        inkex.utils.debug(self.options.strings)

if __name__ == "__main__":
    MassInk().run()"""


import inkex

class MassInk(inkex.Effect):
    def effect(self):
        strings = self.args.get('inputstrings', '')       #example : "new game||options||exit to|desktop"

        #split correclty
        lines = strings.split("||")

        for i in range(len(lines)):
            inkex.utils.debug(lines[i])
        
if __name__ == "__main__":
    MassInk().run()