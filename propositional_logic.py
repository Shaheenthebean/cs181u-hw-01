TABWIDTH = 2

class BoolExpression(object):
    def __init__(self):
        super()
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        return self.__class__.__name__ + "(" + ", ".join([str(v) for v in self.__dict__.values()]) + ")"
    def __repr__(self):
        return str(self)
    def __hash__(self):
        return(hash(str(self)))
    def getVars(self):
        return []
    def eval(self, interp):
        return BoolConst(False)
    def truthTable(self):
        vars = self.getVars()
        interps = allInterpretations(vars)
        truthValues = []
        for i in interps:
            truthValues.append(self.eval(i))
        return TruthTable(vars, interps, truthValues)
    def indented(self, d):
        return ''
    def treeView(self):
        print(self.indented(0))
    def isLiteral(self):
        return False
    def isAtom(self):
        return False
    def removeImplications(self):
        return self
    def NNF(self):
        return self
    def isNNF(self):
        return False

class TruthTable(object):
    def __init__(self, vars, interps, truthValues):
        self.vars = vars
        self.interps = interps
        self.truthValues = truthValues
    def __repr__(self):
        return str(self)
    def __str__(self):
        tableString = '\n'
        for v in self.vars:
            tableString += v.name + '\t'
        tableString += '|\n'
        tableString += '----'*len(tableString) + '\n'
        for i in range(len(self.truthValues)):
            for v in self.vars:
                tableString += self.interps[i][v].format() + '\t'
            tableString += '|\t' + self.truthValues[i].format() + '\n'
        return tableString

class BoolConst(BoolExpression):
    def __init__(self, val):
        self.val = val
    def format(self):
        return "T" if self.val else "F"
    def tex(self):
        return self.format()
    def eval(self, interp):
        return self
    def NNF(self):
        return self
    def getVars(self):
        return []
    def simplify(self):
        return self
    def indented(self,d):
        return TABWIDTH*d*' ' + str(self.val)
    def removeImplications(self):
        return self
    def isLiteral(self):
        return True
    def isAtom(self):
        return True
    def isNNF(self):
        return True

class BoolVar(BoolExpression):
    def __init__(self, name):
        self.name = name
    def format(self):
        return str(self.name)
    def tex(self):
        return self.format()
    def eval(self, interp):
        return interp[self]
    def NNF(self):
        return self
    def getVars(self):
        return [self]
    def simplify(self):
        return self
    def indented(self,d):
        return TABWIDTH*d*' ' + str(self.name)
    def removeImplications(self):
        return self
    def isAtom(self):
        return True
    def isLiteral(self):
        return True
    def isNNF(self):
        return True


class Not(BoolExpression):
    def __init__(self, exp):
        self.exp = exp
    def format(self):
        return "~" + self.exp.format()
    def tex(self):
        return '\\neg ' + self.exp.tex()
    def eval(self, interp):
        return BoolConst(not self.exp.eval(interp).val)
    def NNF(self):
        temp = self.removeImplications()
        if temp.isNNF():
            return temp
        elif (isinstance(temp.exp, Or)):
            return And(Not(temp.exp.exp1), Not(temp.exp.exp2)).NNF()
        elif (isinstance(temp.exp, And)):
            return Or(Not(temp.exp.exp1), Not(temp.exp.exp2)).NNF()
        elif (isinstance(temp.exp, Not)):
            return temp.exp.exp.NNF()

    def getVars(self):
        return self.exp.getVars()
    def simplify(self):
        temp = self.exp.simplify()
        if isinstance(temp, BoolConst):
            return BoolConst(not temp.val)
        elif isinstance(temp, Not):
            return temp.exp.simplify()
        else:
            return Not(temp)

    def indented(self,d):
        return TABWIDTH*d*' ' + "Not\n" + self.exp.indented(d + 1) + "\n"
    def removeImplications(self):
        return Not(self.exp.removeImplications())

    def isLiteral(self):
        return self.exp.isAtom()
    def isNNF(self):
        return self.exp.isAtom()


class And(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " & " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\land " + self.exp2.tex() + ")"
    def eval(self, interp):
        return BoolConst(self.exp1.eval(interp).val and self.exp2.eval(interp).val)

    def NNF(self):
        temp = self.removeImplications()
        return And(temp.exp1.NNF(), temp.exp2.NNF())

    def getVars(self):
        return list(set(self.exp1.getVars() + self.exp2.getVars()))
    def simplify(self):
        temp1 = self.exp1.simplify()
        temp2 = self.exp2.simplify()
        if isinstance(temp1, BoolConst):
            if temp1.val == True:
                return temp2.simplify()
            else:
                return BoolConst(False)

        elif isinstance(temp2, BoolConst):
            if temp2.val == True:
                return temp1.simplify()
            else:
                return BoolConst(False)
        elif temp1 == temp2:
            return temp1.simplify()

        else:
            return And(temp1, temp2)

    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "And\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        return And(self.exp1.removeImplications(), self.exp2.removeImplications())

    def isNNF(self):
        return self.exp1.isNNF() and self.exp2.isNNF()


class Or(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " | " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\lor " + self.exp2.tex() + ")"
    def eval(self, interp):
        return BoolConst(self.exp1.eval(interp).val or self.exp2.eval(interp).val)

    def NNF(self):
        temp = self.removeImplications()
        return Or(temp.exp1.NNF(), temp.exp2.NNF())

    def getVars(self):
        return list(set(self.exp1.getVars() + self.exp2.getVars()))

    def simplify(self):
        temp1 = self.exp1.simplify()
        temp2 = self.exp2.simplify()
        if isinstance(temp1, BoolConst):
            if temp1.val == True:
                return BoolConst(True)
            else:
                return temp2.simplify()

        elif isinstance(temp2, BoolConst):
            if temp2.val == True:
                return BoolConst(True)
            else:
                return temp1.simplify()
        elif temp1 == temp2:
            return self.exp1.simplify()

        else:
            return Or(temp1, temp2)
    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Or\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result
    def removeImplications(self):
        return Or(self.exp1.removeImplications(), self.exp2.removeImplications())

    def isNNF(self):
        return self.exp1.isNNF() and self.exp2.isNNF()

class Implies(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " => " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\Rightarrow " + self.exp2.tex() + ")"
    def eval(self, interp):
        return self.removeImplications().eval(interp)

    def NNF(self):
        temp = self.removeImplications()
        return temp.NNF()

    def getVars(self):
        return list(set(self.exp1.getVars() + self.exp2.getVars()))

    def simplify(self):
        e1 = self.exp1.simplify()
        e2 = self.exp2.simplify()
        if e1 == BoolConst(True):
            return e2
        elif e1 == BoolConst(False):
            return BoolConst(True)
        elif e1 == e2:
            return BoolConst(True)
        elif e2 == BoolConst(True):
            return e2
        elif e2 == BoolConst(False):
            return Not(e1)
        else:
            return Implies(e1, e2)


    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Implies\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1) + "\n"
        return result

    def removeImplications(self):
        x = Or(Not(self.exp1).removeImplications(), self.exp2.removeImplications())
        return x

    def isNNF(self):
        return False

class Iff(BoolExpression):
    def __init__(self, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
    def format(self):
        return "(" + self.exp1.format() + " <=> " + self.exp2.format() + ")"
    def tex(self):
        return "(" + self.exp1.tex() + " \\Leftrightarrow " + self.exp2.tex() + ")"
    def eval(self, interp):
        val1 = self.exp1.eval(interp)
        val2 = self.exp2.eval(interp)
        return BoolConst(val1.val == val2.val)
    def NNF(self):
        return self.removeImplications().NNF()
    def getVars(self):
        return list(set(self.exp1.getVars() + self.exp2.getVars()))
    def simplify(self):
        e1 = self.exp1.simplify()
        e2 = self.exp2.simplify()
        if e1 == BoolConst(True):
            return e2
        elif e2 == BoolConst(True):
            return e1
        elif e1 == BoolConst(False):
            return Not(e2)
        elif e2 == BoolConst(False):
            return Not(e1)
        elif e1 == e2:
            return BoolConst(True)
        else:
            return Iff(e1, e2)


    def indented(self,d):
        result = TABWIDTH*d*' '
        result += "Iff\n"
        result += self.exp1.indented(d + 1) + "\n"
        result += self.exp2.indented(d + 1)
        return result

    def removeImplications(self):
        return And(Implies(self.exp1, self.exp2).removeImplications(), Implies(self.exp2, self.exp1).removeImplications())

    def isNNF(self):
        return False



def dictUnite(d1, d2):
    return dict(list(d1.items()) + list(d2.items()))

def dictListProduct(dl1, dl2):
    return [dictUnite(d1,d2) for d1 in dl1 for d2 in dl2]

def allInterpretations(varList):
    if varList == []:
        return [{}]
    else:
        v = varList[0]
        v_interps = [{v : BoolConst(False)}, {v : BoolConst(True)}]
        return dictListProduct(v_interps, allInterpretations(varList[1:]))
